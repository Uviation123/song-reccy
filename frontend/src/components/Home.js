import React, { useState } from 'react';
import { Music, Brain, Headphones, ArrowRight, Sparkles } from 'lucide-react';
import axios from 'axios';

const Home = () => {
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/login');
      window.location.href = response.data.auth_url;
    } catch (error) {
      console.error('Login failed:', error);
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ paddingTop: '2rem' }}>
      {/* Hero Section */}
      <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
        <div className="glass-card" style={{ maxWidth: '800px', margin: '0 auto' }}>
          <h1 style={{ 
            fontSize: '3.5rem', 
            marginBottom: '1rem', 
            background: 'linear-gradient(45deg, #00f5ff, #1ed760, #ff77c6, #00f5ff)',
            backgroundSize: '300% 300%',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 'bold',
            animation: 'gradient-shift 4s ease infinite',
            textShadow: '0 0 40px rgba(0, 245, 255, 0.5)',
            letterSpacing: '2px'
          }}>
            <Sparkles size={40} style={{ 
              marginRight: '15px', 
              color: '#00f5ff',
              filter: 'drop-shadow(0 0 10px rgba(0, 245, 255, 0.7))'
            }} />
            Song Reccy
          </h1>
          <p style={{ 
            fontSize: '1.3rem', 
            marginBottom: '2rem', 
            color: 'rgba(255, 255, 255, 0.9)',
            lineHeight: '1.6'
          }}>
            Discover your next favorite song with AI-powered recommendations 
            based on your unique listening habits
          </p>
          <button 
            onClick={handleLogin}
            disabled={loading}
            className="btn btn-primary"
            style={{ 
              fontSize: '1.1rem', 
              padding: '15px 30px',
              marginBottom: '1rem'
            }}
          >
            {loading ? (
              <>
                <div className="loading-spinner">⏳</div>
                Connecting...
              </>
            ) : (
              <>
                <Music size={20} />
                Connect with Spotify
                <ArrowRight size={20} />
              </>
            )}
          </button>
          <p style={{ 
            fontSize: '0.9rem', 
            color: 'rgba(255, 255, 255, 0.7)',
            marginTop: '1rem'
          }}>
            We'll analyze your listening history to create personalized recommendations
          </p>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid grid-3" style={{ marginBottom: '4rem' }}>
        <div className="glass-card" style={{ textAlign: 'center' }}>
          <Brain size={48} style={{ color: '#1DB954', marginBottom: '1rem' }} />
          <h3 style={{ marginBottom: '1rem', color: 'white' }}>AI-Powered Analysis</h3>
          <p style={{ color: 'rgba(255, 255, 255, 0.8)', lineHeight: '1.6' }}>
            Our machine learning algorithm analyzes your music preferences including 
            energy, danceability, tempo, and mood to understand your unique taste.
          </p>
        </div>

        <div className="glass-card" style={{ textAlign: 'center' }}>
          <Headphones size={48} style={{ color: '#1DB954', marginBottom: '1rem' }} />
          <h3 style={{ marginBottom: '1rem', color: 'white' }}>Smart Recommendations</h3>
          <p style={{ color: 'rgba(255, 255, 255, 0.8)', lineHeight: '1.6' }}>
            Get personalized song suggestions that match your listening habits, 
            discovering new music you'll love while staying true to your taste.
          </p>
        </div>

        <div className="glass-card" style={{ textAlign: 'center' }}>
          <Music size={48} style={{ color: '#1DB954', marginBottom: '1rem' }} />
          <h3 style={{ marginBottom: '1rem', color: 'white' }}>Spotify Integration</h3>
          <p style={{ color: 'rgba(255, 255, 255, 0.8)', lineHeight: '1.6' }}>
            Seamlessly connects with your Spotify account to access your listening 
            history and provide recommendations you can instantly add to your playlists.
          </p>
        </div>
      </div>

      {/* How It Works Section */}
      <div className="card" style={{ marginBottom: '4rem' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: '#333' }}>
          How It Works
        </h2>
        <div className="grid grid-2">
          <div style={{ padding: '1rem' }}>
            <h4 style={{ color: '#1DB954', marginBottom: '0.5rem' }}>1. Connect Your Spotify</h4>
            <p style={{ color: '#666', lineHeight: '1.6' }}>
              Securely connect your Spotify account to allow us to analyze your listening history.
            </p>
          </div>
          <div style={{ padding: '1rem' }}>
            <h4 style={{ color: '#1DB954', marginBottom: '0.5rem' }}>2. AI Analysis</h4>
            <p style={{ color: '#666', lineHeight: '1.6' }}>
              Our machine learning model analyzes audio features of your favorite tracks.
            </p>
          </div>
          <div style={{ padding: '1rem' }}>
            <h4 style={{ color: '#1DB954', marginBottom: '0.5rem' }}>3. Get Recommendations</h4>
            <p style={{ color: '#666', lineHeight: '1.6' }}>
              Receive personalized song recommendations based on your unique music profile.
            </p>
          </div>
          <div style={{ padding: '1rem' }}>
            <h4 style={{ color: '#1DB954', marginBottom: '0.5rem' }}>4. Discover & Enjoy</h4>
            <p style={{ color: '#666', lineHeight: '1.6' }}>
              Listen to your recommendations and discover your next favorite song!
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="glass-card" style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h2 style={{ marginBottom: '1rem', color: 'white' }}>
          Ready to Discover Amazing Music?
        </h2>
        <p style={{ 
          marginBottom: '2rem', 
          color: 'rgba(255, 255, 255, 0.8)',
          fontSize: '1.1rem'
        }}>
          Join thousands of music lovers who've discovered their new favorite songs with Song Reccy
        </p>
        <button 
          onClick={handleLogin}
          disabled={loading}
          className="btn btn-primary"
          style={{ fontSize: '1.1rem', padding: '15px 30px' }}
        >
          {loading ? (
            <>
              <div className="loading-spinner">⏳</div>
              Connecting...
            </>
          ) : (
            <>
              Get Started Now
              <ArrowRight size={20} />
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default Home;
