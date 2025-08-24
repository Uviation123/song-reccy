import React, { useState, useEffect } from 'react';
import { 
  Music, 
  Brain, 
  RefreshCw, 
  ExternalLink, 
  Play,
  TrendingUp,
  Zap,
  Heart,
  Volume2
} from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/user-profile', { withCredentials: true });
      setUser(response.data);
    } catch (error) {
      console.error('Authentication failed:', error);
      window.location.href = '/';
    }
  };

  const analyzeListeningHabits = async () => {
    setAnalyzing(true);
    setError(null);
    try {
      const response = await axios.get('/api/analyze-listening-habits', { withCredentials: true });
      setAnalysis(response.data);
    } catch (error) {
      setError('Failed to analyze listening habits. Please try again.');
      console.error('Analysis failed:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const getRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/recommendations', { withCredentials: true });
      setRecommendations(response.data.recommendations);
    } catch (error) {
      if (error.response?.status === 400) {
        setError('Please analyze your listening habits first.');
      } else {
        setError('Failed to get recommendations. Please try again.');
      }
      console.error('Recommendations failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatPreference = (key, value) => {
    const percentage = Math.round(value * 100);
    let description = '';
    
    switch (key) {
      case 'energy':
        description = percentage > 70 ? 'High Energy' : percentage > 40 ? 'Moderate Energy' : 'Low Energy';
        break;
      case 'danceability':
        description = percentage > 70 ? 'Very Danceable' : percentage > 40 ? 'Somewhat Danceable' : 'Not Very Danceable';
        break;
      case 'valence':
        description = percentage > 60 ? 'Positive Mood' : percentage > 40 ? 'Neutral Mood' : 'Melancholic';
        break;
      case 'acousticness':
        description = percentage > 50 ? 'Acoustic' : 'Electronic';
        break;
      default:
        description = `${percentage}%`;
    }
    
    return { percentage, description };
  };

  const getIcon = (key) => {
    switch (key) {
      case 'energy': return <Zap size={20} />;
      case 'danceability': return <Music size={20} />;
      case 'valence': return <Heart size={20} />;
      case 'acousticness': return <Volume2 size={20} />;
      default: return <TrendingUp size={20} />;
    }
  };

  if (!user) {
    return (
      <div className="container" style={{ paddingTop: '2rem' }}>
        <div className="loading">
          <RefreshCw className="loading-spinner" size={24} />
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ paddingTop: '2rem' }}>
      {/* User Profile Section */}
      <div className="glass-card" style={{ marginBottom: '2rem', textAlign: 'center' }}>
        {user.images && user.images[0] && (
          <img 
            src={user.images[0].url} 
            alt="Profile"
            style={{ 
              width: '80px', 
              height: '80px', 
              borderRadius: '50%', 
              marginBottom: '1rem' 
            }}
          />
        )}
        <h2 style={{ color: 'white', marginBottom: '0.5rem' }}>
          Welcome, {user.display_name}!
        </h2>
        <p style={{ color: 'rgba(255, 255, 255, 0.7)' }}>
          {user.followers} followers on Spotify
        </p>
      </div>

      {/* Analysis Section */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3 style={{ color: '#333' }}>
            <Brain size={24} style={{ marginRight: '8px' }} />
            Music Taste Analysis
          </h3>
          <button 
            onClick={analyzeListeningHabits}
            disabled={analyzing}
            className="btn btn-primary"
          >
            {analyzing ? (
              <>
                <RefreshCw className="loading-spinner" size={16} />
                Analyzing...
              </>
            ) : (
              <>
                <Brain size={16} />
                Analyze My Taste
              </>
            )}
          </button>
        </div>

        {analysis && (
          <div>
            {/* Statistics */}
            <div className="grid grid-3" style={{ marginBottom: '2rem' }}>
              <div className="glass-card stat-card">
                <span className="stat-number">{analysis.total_tracks_analyzed}</span>
                <span className="stat-label">Tracks Analyzed</span>
              </div>
              <div className="glass-card stat-card">
                <span className="stat-number">{analysis.taste_profile.energy_level}</span>
                <span className="stat-label">Energy Level</span>
              </div>
              <div className="glass-card stat-card">
                <span className="stat-number">{analysis.taste_profile.valence}</span>
                <span className="stat-label">Mood Preference</span>
              </div>
            </div>

            {/* Detailed Preferences */}
            <div className="grid grid-2" style={{ marginBottom: '2rem' }}>
              {Object.entries(analysis.preferences)
                .filter(([key]) => ['energy', 'danceability', 'valence', 'acousticness'].includes(key))
                .map(([key, value]) => {
                  const { percentage, description } = formatPreference(key, value);
                  return (
                    <div key={key} className="preference-card">
                      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0.5rem' }}>
                        {getIcon(key)}
                        <span className="preference-label" style={{ marginLeft: '8px' }}>
                          {key}
                        </span>
                      </div>
                      <div style={{ 
                        background: 'rgba(255, 255, 255, 0.1)', 
                        borderRadius: '10px', 
                        height: '8px',
                        marginBottom: '0.5rem',
                        border: '1px solid rgba(0, 245, 255, 0.2)',
                        boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.2)'
                      }}>
                        <div style={{ 
                          background: 'linear-gradient(45deg, #00f5ff, #1ed760)',
                          width: `${percentage}%`,
                          height: '100%',
                          borderRadius: '10px',
                          transition: 'width 0.3s ease',
                          boxShadow: '0 0 10px rgba(0, 245, 255, 0.5)',
                          position: 'relative'
                        }} />
                      </div>
                      <span className="preference-description">
                        {description}
                      </span>
                    </div>
                  );
                })}
            </div>

            {/* Top Tracks */}
            <h4 style={{ color: '#333', marginBottom: '1rem' }}>Your Recent Favorites</h4>
            <div className="grid grid-2">
              {analysis.top_tracks.slice(0, 4).map((track, index) => (
                <div key={index} className="track-card">
                  {track.image && (
                    <img 
                      src={track.image} 
                      alt={track.name}
                      className="track-image"
                    />
                  )}
                  <div className="track-info">
                    <h4>{track.name}</h4>
                    <p>{track.artist}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Recommendations Section */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3 style={{ color: '#333' }}>
            <Music size={24} style={{ marginRight: '8px' }} />
            Recommended Songs
          </h3>
          <button 
            onClick={getRecommendations}
            disabled={loading || !analysis}
            className="btn btn-primary"
          >
            {loading ? (
              <>
                <RefreshCw className="loading-spinner" size={16} />
                Loading...
              </>
            ) : (
              <>
                <RefreshCw size={16} />
                Get Recommendations
              </>
            )}
          </button>
        </div>

        {!analysis && (
          <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
            Please analyze your listening habits first to get personalized recommendations.
          </p>
        )}

        {recommendations.length > 0 && (
          <div className="grid grid-2">
            {recommendations.map((track, index) => (
              <div key={track.id} className="track-card">
                {track.image && (
                  <img 
                    src={track.image} 
                    alt={track.name}
                    className="track-image"
                  />
                )}
                <div className="track-info" style={{ flex: 1 }}>
                  <h4>{track.name}</h4>
                  <p>{track.artist}</p>
                  <p style={{ fontSize: '11px' }}>{track.album}</p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {track.preview_url && (
                    <button 
                      onClick={() => {
                        const audio = new Audio(track.preview_url);
                        audio.play();
                      }}
                      className="btn btn-secondary"
                      style={{ padding: '6px 12px', fontSize: '12px' }}
                    >
                      <Play size={14} />
                    </button>
                  )}
                  <a 
                    href={track.external_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary"
                    style={{ padding: '6px 12px', fontSize: '12px' }}
                  >
                    <ExternalLink size={14} />
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="error">
          {error}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
