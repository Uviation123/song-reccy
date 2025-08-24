import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Music, LogOut } from 'lucide-react';
import axios from 'axios';

const Navbar = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get('/user-profile', { withCredentials: true });
      setUser(response.data);
    } catch (error) {
      setUser(null);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.get('/logout', { withCredentials: true });
      setUser(null);
      window.location.href = '/';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="logo">
            <Music size={24} style={{ marginRight: '8px' }} />
            Song Reccy
          </Link>
          
          {user && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span style={{ color: 'white' }}>
                Welcome, {user.display_name}!
              </span>
              <button 
                onClick={handleLogout}
                className="btn btn-secondary"
                style={{ padding: '8px 16px', fontSize: '14px' }}
              >
                <LogOut size={16} />
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
