from flask import Flask, request, jsonify, session, redirect, send_from_directory
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import os
from datetime import datetime
import pickle
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
CORS(app, supports_credentials=True)

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '')
# Default to localhost for development, but use environment variable for production
DEFAULT_REDIRECT_URI = 'http://127.0.0.1:5000/api/callback'
SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', DEFAULT_REDIRECT_URI)

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-recently-played user-top-read user-library-read playlist-read-private user-read-private streaming"
)

class SongRecommender:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=10)
        self.user_profile = None
        self.tracks_features = pd.DataFrame()
        
    def extract_audio_features(self, tracks, sp):
        """Extract audio features for a list of tracks"""
        try:
            track_ids = [track['id'] for track in tracks if track and track.get('id')]
            logger.info(f"Extracting features for {len(track_ids)} tracks")
            
            if not track_ids:
                logger.warning("No valid track IDs found")
                return pd.DataFrame()
                
            # Get audio features in batches of 100
            features_list = []
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i+100]
                try:
                    logger.info(f"Getting features for batch {i//100 + 1}, {len(batch)} tracks")
                    features = sp.audio_features(batch)
                    if features:
                        valid_features = [f for f in features if f is not None]
                        features_list.extend(valid_features)
                        logger.info(f"Got {len(valid_features)} valid features from batch")
                    else:
                        logger.warning(f"No features returned for batch {i//100 + 1}")
                except Exception as batch_error:
                    logger.error(f"Error getting features for batch {i//100 + 1}: {batch_error}")
                    continue
            
            if not features_list:
                logger.error("No audio features could be retrieved")
                return pd.DataFrame()
                
            logger.info(f"Total features retrieved: {len(features_list)}")
            
            # Convert to DataFrame
            df = pd.DataFrame(features_list)
            logger.info(f"DataFrame created with shape: {df.shape}")
            
            # Select relevant features for ML
            feature_cols = [
                'danceability', 'energy', 'key', 'loudness', 'mode',
                'speechiness', 'acousticness', 'instrumentalness',
                'liveness', 'valence', 'tempo', 'time_signature'
            ]
            
            # Check which columns are available
            available_cols = [col for col in feature_cols if col in df.columns]
            missing_cols = [col for col in feature_cols if col not in df.columns]
            
            if missing_cols:
                logger.warning(f"Missing columns: {missing_cols}")
            
            if not available_cols:
                logger.error("No required feature columns found in audio features")
                return pd.DataFrame()
            
            result_df = df[available_cols].fillna(0)
            logger.info(f"Final feature DataFrame shape: {result_df.shape}")
            return result_df
            
        except Exception as e:
            logger.error(f"Error in extract_audio_features: {e}")
            return pd.DataFrame()
    
    def create_user_profile(self, user_tracks_features):
        """Create user profile based on listening history"""
        if user_tracks_features.empty:
            return None
            
        # Calculate mean preferences
        user_profile = user_tracks_features.mean()
        
        # Apply PCA for dimensionality reduction
        scaled_features = self.scaler.fit_transform(user_tracks_features)
        pca_features = self.pca.fit_transform(scaled_features)
        
        return {
            'preferences': user_profile.to_dict(),
            'pca_profile': np.mean(pca_features, axis=0)
        }
    
    def get_recommendations(self, sp, user_profile, seed_tracks=None, num_recommendations=10):
        """Get song recommendations based on user profile"""
        try:
            # If in fallback mode or seed tracks provided, use Spotify's recommendation API
            if user_profile.get('fallback_mode', False) or seed_tracks:
                return self.get_spotify_recommendations(sp, seed_tracks, num_recommendations)
            
            # Original ML-based approach
            # Get popular tracks from various genres
            genres = ['pop', 'rock', 'hip-hop', 'electronic', 'indie', 'alternative']
            candidate_tracks = []
            
            for genre in genres:
                try:
                    # Search for tracks in each genre
                    results = sp.search(q=f'genre:{genre}', type='track', limit=50)
                    candidate_tracks.extend(results['tracks']['items'])
                except Exception as e:
                    logger.warning(f"Error searching genre {genre}: {e}")
                    continue
            
            if not candidate_tracks:
                # Fallback: get featured playlists
                playlists = sp.featured_playlists(limit=5)
                for playlist in playlists['playlists']['items']:
                    try:
                        tracks = sp.playlist_tracks(playlist['id'], limit=20)
                        candidate_tracks.extend([item['track'] for item in tracks['items'] if item['track']])
                    except Exception as e:
                        logger.warning(f"Error getting playlist tracks: {e}")
                        continue
            
            # Remove duplicates
            seen_ids = set()
            unique_tracks = []
            for track in candidate_tracks:
                if track and track.get('id') and track['id'] not in seen_ids:
                    seen_ids.add(track['id'])
                    unique_tracks.append(track)
            
            if not unique_tracks:
                return []
            
            # Extract features for candidate tracks
            candidate_features = self.extract_audio_features(unique_tracks, sp)
            
            if candidate_features.empty:
                return unique_tracks[:num_recommendations]
            
            # Scale candidate features
            scaled_candidates = self.scaler.transform(candidate_features)
            candidate_pca = self.pca.transform(scaled_candidates)
            
            # Calculate similarity with user profile
            user_pca_profile = user_profile['pca_profile'].reshape(1, -1)
            similarities = cosine_similarity(user_pca_profile, candidate_pca)[0]
            
            # Get top recommendations
            top_indices = np.argsort(similarities)[-num_recommendations:][::-1]
            recommendations = [unique_tracks[i] for i in top_indices]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in get_recommendations: {e}")
            return self.get_spotify_recommendations(sp, seed_tracks, num_recommendations)
    
    def get_spotify_recommendations(self, sp, seed_tracks=None, num_recommendations=10):
        """Get recommendations using Spotify's built-in recommendation system"""
        try:
            logger.info("Using Spotify's built-in recommendation system")
            
            if not seed_tracks:
                # Get some popular tracks as seeds
                results = sp.search(q='year:2023-2024', type='track', limit=5)
                seed_tracks = [track['id'] for track in results['tracks']['items']]
            
            # Ensure seed_tracks is a list, not a string
            if isinstance(seed_tracks, str):
                seed_tracks = seed_tracks.split(',')
            
            # Use only up to 5 seed tracks (Spotify API limit)
            seed_tracks = seed_tracks[:5]
            
            logger.info(f"Using seed tracks: {seed_tracks}")
            
            # Try different recommendation approaches
            try:
                # First try: Use seed tracks
                recommendations = sp.recommendations(
                    seed_tracks=seed_tracks,
                    limit=num_recommendations
                )
                logger.info(f"Got {len(recommendations['tracks'])} recommendations using seed tracks")
                return recommendations['tracks']
                
            except Exception as seed_error:
                logger.warning(f"Seed tracks failed: {seed_error}")
                
                # Second try: Use genres as seeds
                try:
                    available_genres = sp.recommendation_genre_seeds()['genres']
                    selected_genres = available_genres[:3]  # Use first 3 genres
                    logger.info(f"Trying with genres: {selected_genres}")
                    
                    recommendations = sp.recommendations(
                        seed_genres=selected_genres,
                        limit=num_recommendations
                    )
                    logger.info(f"Got {len(recommendations['tracks'])} recommendations using genres")
                    return recommendations['tracks']
                    
                except Exception as genre_error:
                    logger.warning(f"Genre recommendations failed: {genre_error}")
                    
                    # Third try: Get popular playlists
                    return self.get_playlist_tracks(sp, num_recommendations)
            
        except Exception as e:
            logger.error(f"Error getting Spotify recommendations: {e}")
            return self.get_playlist_tracks(sp, num_recommendations)
    
    def get_playlist_tracks(self, sp, num_recommendations=10):
        """Fallback: Get tracks using search (works with basic Spotify app permissions)"""
        try:
            logger.info("Falling back to search-based recommendations")
            tracks = []
            
            # Search for popular music using different terms
            search_terms = [
                'year:2023-2024',
                'genre:pop',
                'genre:rock', 
                'genre:electronic',
                'playlist:top hits',
                'artist:taylor swift',
                'artist:the weeknd',
                'artist:dua lipa',
                'track:popular'
            ]
            
            for term in search_terms:
                if len(tracks) >= num_recommendations:
                    break
                    
                try:
                    logger.info(f"Searching for: {term}")
                    results = sp.search(q=term, type='track', limit=5)
                    
                    for track in results['tracks']['items']:
                        if track and len(tracks) < num_recommendations:
                            # Avoid duplicates
                            if not any(t['id'] == track['id'] for t in tracks):
                                tracks.append(track)
                                
                except Exception as search_error:
                    logger.warning(f"Search failed for '{term}': {search_error}")
                    continue
            
            logger.info(f"Got {len(tracks)} tracks from search")
            return tracks[:num_recommendations]
            
        except Exception as e:
            logger.error(f"Error getting search tracks: {e}")
            return []

# Initialize recommender
recommender = SongRecommender()

@app.route('/api')
def api_info():
    return jsonify({"message": "Spotify Song Recommender API"})

@app.route('/api/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return jsonify({"auth_url": auth_url})

def handle_spotify_callback():
    """Common callback logic for both /api/callback and /callback routes"""
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        
        # Determine the correct frontend URL for redirect
        # In production, use the app domain; in development, use localhost:3000
        frontend_url = os.environ.get('FRONTEND_URL')
        if not frontend_url:
            # Auto-detect based on request host
            host = request.headers.get('Host', 'localhost:5000')
            if 'localhost' in host or '127.0.0.1' in host:
                frontend_url = 'http://localhost:3000'  # Development React app
            else:
                frontend_url = f"https://{host}"  # Production (served by Flask)
        
        dashboard_url = f"{frontend_url}/dashboard"
        logger.info(f"Redirecting to: {dashboard_url}")
        return redirect(dashboard_url)
    return jsonify({"error": "Authorization failed"}), 400

@app.route('/api/callback')
def callback():
    """Primary callback route for Spotify OAuth"""
    return handle_spotify_callback()

@app.route('/callback')
def callback_fallback():
    """Fallback callback route for older Spotify app configurations"""
    logger.info("Using fallback callback route - consider updating your Spotify app redirect URI to /api/callback")
    return handle_spotify_callback()

@app.route('/api/user-profile')
def get_user_profile():
    token_info = session.get('token_info', None)
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user = sp.current_user()
        return jsonify({
            "id": user['id'],
            "display_name": user['display_name'],
            "followers": user['followers']['total'],
            "images": user['images']
        })
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        return jsonify({"error": "Failed to get user profile"}), 500

@app.route('/api/analyze-listening-habits')
def analyze_listening_habits():
    token_info = session.get('token_info', None)
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Test API access first
        try:
            user = sp.current_user()
            logger.info(f"Successfully authenticated user: {user['id']}")
        except Exception as auth_error:
            logger.error(f"Authentication test failed: {auth_error}")
            return jsonify({"error": "Authentication failed. Please log in again."}), 401
        
        # Get user's data with better error handling
        all_tracks = []
        
        try:
            # Get top tracks (these are more likely to exist)
            logger.info("Fetching top tracks...")
            top_tracks_short = sp.current_user_top_tracks(limit=20, time_range='short_term')
            top_tracks_medium = sp.current_user_top_tracks(limit=20, time_range='medium_term')
            top_tracks_long = sp.current_user_top_tracks(limit=20, time_range='long_term')
            
            all_tracks.extend(top_tracks_short['items'])
            all_tracks.extend(top_tracks_medium['items']) 
            all_tracks.extend(top_tracks_long['items'])
            logger.info(f"Found {len(all_tracks)} top tracks")
            
        except Exception as top_tracks_error:
            logger.warning(f"Error getting top tracks: {top_tracks_error}")
        
        try:
            # Get recently played tracks
            logger.info("Fetching recently played tracks...")
            recent_tracks = sp.current_user_recently_played(limit=50)
            recent_track_items = [item['track'] for item in recent_tracks['items'] if item['track']]
            all_tracks.extend(recent_track_items)
            logger.info(f"Found {len(recent_track_items)} recent tracks")
            
        except Exception as recent_error:
            logger.warning(f"Error getting recent tracks: {recent_error}")
        
        # If still no tracks, try saved tracks
        if len(all_tracks) < 5:
            try:
                logger.info("Trying saved tracks...")
                saved_tracks = sp.current_user_saved_tracks(limit=50)
                saved_track_items = [item['track'] for item in saved_tracks['items'] if item['track']]
                all_tracks.extend(saved_track_items)
                logger.info(f"Found {len(saved_track_items)} saved tracks")
            except Exception as saved_error:
                logger.warning(f"Error getting saved tracks: {saved_error}")
        
        if not all_tracks:
            return jsonify({
                "error": "No listening history found. Please listen to some music on Spotify first, then try again."
            }), 400
        
        # Remove duplicates
        seen_ids = set()
        unique_tracks = []
        for track in all_tracks:
            if track and track.get('id') and track['id'] not in seen_ids:
                seen_ids.add(track['id'])
                unique_tracks.append(track)
        
        logger.info(f"Found {len(unique_tracks)} unique tracks for analysis")
        
        if len(unique_tracks) < 3:
            return jsonify({
                "error": "Not enough tracks for analysis. Please listen to more music on Spotify first."
            }), 400
        
        # Extract audio features
        tracks_features = recommender.extract_audio_features(unique_tracks, sp)
        
        if tracks_features.empty:
            # Fallback: Use simplified analysis based on track metadata
            logger.info("Audio features unavailable, using fallback analysis")
            user_profile = {
                'preferences': {
                    'energy': 0.6,  # Default moderate values
                    'danceability': 0.5,
                    'valence': 0.5,
                    'acousticness': 0.3,
                    'instrumentalness': 0.1,
                    'speechiness': 0.1,
                    'liveness': 0.2,
                    'loudness': -10,
                    'tempo': 120,
                    'key': 5,
                    'mode': 1,
                    'time_signature': 4
                },
                'pca_profile': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Default PCA values
                'fallback_mode': True
            }
            session['user_profile'] = user_profile
            
            # Use track IDs for seed-based recommendations instead
            seed_tracks = [track['id'] for track in unique_tracks[:5] if track.get('id')]
            session['seed_tracks'] = seed_tracks
            
        else:
            # Create user profile
            user_profile = recommender.create_user_profile(tracks_features)
            user_profile['fallback_mode'] = False
            session['user_profile'] = user_profile
        
        # Calculate listening habits summary
        preferences = user_profile['preferences']
        
        # Determine music taste profile
        taste_profile = {
            "energy_level": "High" if preferences['energy'] > 0.7 else "Medium" if preferences['energy'] > 0.4 else "Low",
            "danceability": "High" if preferences['danceability'] > 0.7 else "Medium" if preferences['danceability'] > 0.4 else "Low",
            "valence": "Positive" if preferences['valence'] > 0.6 else "Neutral" if preferences['valence'] > 0.4 else "Melancholic",
            "acousticness": "Acoustic" if preferences['acousticness'] > 0.5 else "Electronic",
            "instrumentalness": "Instrumental" if preferences['instrumentalness'] > 0.5 else "Vocal"
        }
        
        return jsonify({
            "total_tracks_analyzed": len(unique_tracks),
            "preferences": preferences,
            "taste_profile": taste_profile,
            "top_tracks": [
                {
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "image": track['album']['images'][0]['url'] if track['album']['images'] else None
                }
                for track in unique_tracks[:10]
            ]
        })
        
    except Exception as e:
        logger.error(f"Error analyzing listening habits: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return jsonify({
            "error": f"Failed to analyze listening habits: {str(e)}"
        }), 500

@app.route('/api/recommendations')
def get_recommendations():
    token_info = session.get('token_info', None)
    user_profile = session.get('user_profile', None)
    
    if not token_info:
        return jsonify({"error": "Not authenticated"}), 401
    
    if not user_profile:
        return jsonify({"error": "No user profile found. Please analyze listening habits first."}), 400
    
    try:
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Get seed tracks if in fallback mode
        seed_tracks = None
        if user_profile.get('fallback_mode', False):
            seed_tracks = session.get('seed_tracks', None)
        
        recommendations = recommender.get_recommendations(sp, user_profile, seed_tracks)
        
        # Format recommendations
        formatted_recommendations = []
        for track in recommendations:
            if track and track.get('id'):
                formatted_recommendations.append({
                    "id": track['id'],
                    "name": track['name'],
                    "artist": track['artists'][0]['name'] if track['artists'] else 'Unknown',
                    "album": track['album']['name'],
                    "image": track['album']['images'][0]['url'] if track['album']['images'] else None,
                    "preview_url": track.get('preview_url'),
                    "external_url": track['external_urls']['spotify'],
                    "popularity": track.get('popularity', 0)
                })
        
        return jsonify({
            "recommendations": formatted_recommendations,
            "total": len(formatted_recommendations)
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({"error": "Failed to get recommendations"}), 500

@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

# Serve React App (for production)
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
