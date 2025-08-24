# 🎵 Song Reccy - Futuristic AI Music Discovery

> **AI-Powered Spotify Recommendations with a Stunning Glassmorphism UI**

An intelligent music discovery platform that analyzes your Spotify listening habits using advanced machine learning algorithms to deliver personalized song recommendations. Built with a cutting-edge futuristic interface featuring glassmorphism design elements.

![Song Reccy](https://img.shields.io/badge/Song-Reccy-00f5ff?style=for-the-badge&logo=spotify&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=black)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-f7931e?style=for-the-badge&logo=scikit-learn&logoColor=white)

## 🚀 Live Demo
*Coming Soon - Deploy to Vercel/Heroku*

## Features ✨

- **AI-Powered Analysis**: Uses machine learning to analyze your music preferences
- **Spotify Integration**: Seamlessly connects with your Spotify account
- **Beautiful UI**: Modern, responsive design with glassmorphism effects
- **Real-time Recommendations**: Get instant song suggestions based on your taste
- **Music Profile**: Detailed analysis of your listening habits and preferences

## Tech Stack 🛠️

### Backend
- **Flask**: Python web framework
- **Spotipy**: Spotify Web API Python library
- **Scikit-learn**: Machine learning library for recommendations
- **Pandas & Numpy**: Data processing and analysis

### Frontend
- **React**: JavaScript UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **Lucide React**: Beautiful icons

### Machine Learning
- **Principal Component Analysis (PCA)**: Dimensionality reduction
- **Cosine Similarity**: Recommendation algorithm
- **StandardScaler**: Feature normalization

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- Spotify Developer Account
- Git (for cloning and deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/song-reccy.git
cd song-reccy
```

### 2. Spotify App Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Create a new app
3. Add `http://127.0.0.1:5000/callback` to Redirect URIs
4. Note your Client ID and Client Secret

### 3. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file (NEVER commit this file!)
cp env_example.txt .env

# Edit .env with your Spotify credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
SECRET_KEY=your_secret_key_here

# Run the Flask app
python app.py
```

> ⚠️ **Important**: Never commit your `.env` file to GitHub! It contains sensitive API credentials.

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the React app
npm start
```

### 5. Access the Application
- Frontend: http://127.0.0.1:3000
- Backend API: http://127.0.0.1:5000

## How It Works 🧠

### 1. Authentication
- Users authenticate with Spotify using OAuth 2.0
- App requests permissions to read listening history and top tracks

### 2. Data Collection
- Fetches user's top tracks (short, medium, long term)
- Retrieves recently played tracks
- Extracts audio features for each track

### 3. Machine Learning Analysis
- **Feature Extraction**: Analyzes 12 audio features:
  - Danceability, Energy, Key, Loudness, Mode
  - Speechiness, Acousticness, Instrumentalness
  - Liveness, Valence, Tempo, Time Signature

- **User Profile Creation**: 
  - Calculates mean preferences across all tracks
  - Applies PCA for dimensionality reduction
  - Creates a mathematical representation of user taste

- **Recommendation Engine**:
  - Searches for candidate tracks across multiple genres
  - Extracts features for candidate tracks
  - Uses cosine similarity to find tracks similar to user profile
  - Returns top matching recommendations

### 4. Recommendation Display
- Shows personalized song recommendations
- Provides track previews and Spotify links
- Displays user's music taste analysis

## API Endpoints 📡

- `GET /login` - Initiate Spotify OAuth
- `GET /callback` - Handle OAuth callback
- `GET /user-profile` - Get current user info
- `GET /analyze-listening-habits` - Analyze user's music taste
- `GET /recommendations` - Get personalized recommendations
- `GET /logout` - Clear session

## Machine Learning Details 🤖

### Audio Features Used
- **Danceability**: How suitable a track is for dancing
- **Energy**: Perceptual measure of intensity and power
- **Valence**: Musical positiveness (happy vs sad)
- **Acousticness**: Whether the track is acoustic
- **Instrumentalness**: Predicts whether a track contains vocals
- **Tempo**: Overall estimated tempo in BPM

### Algorithm
1. **Data Preprocessing**: Normalize features using StandardScaler
2. **Dimensionality Reduction**: Apply PCA to reduce feature space
3. **Similarity Calculation**: Use cosine similarity for recommendations
4. **Candidate Selection**: Search across multiple genres for diversity

## 📤 Deploying to GitHub

### Initial Upload
```bash
# Initialize git repository (if not already done)
git init

# Add all files (except those in .gitignore)
git add .

# Make your first commit
git commit -m "🎵 Initial commit: AI-powered Spotify recommendation app with glassmorphism UI"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/song-reccy.git

# Push to GitHub
git push -u origin main
```

### Important Files Protected by .gitignore
- ✅ `.env` - Environment variables (API keys)
- ✅ `node_modules/` - Node.js dependencies
- ✅ `__pycache__/` - Python cache files
- ✅ `.cache` - Spotify cache files
- ✅ Build outputs and logs

### Environment Variables for Deployment
When deploying to platforms like Heroku or Vercel, set these environment variables:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=https://your-domain.com/callback
SECRET_KEY=your_production_secret_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) for music data
- [Spotipy](https://spotipy.readthedocs.io/) for Python Spotify integration
- [Scikit-learn](https://scikit-learn.org/) for machine learning capabilities

## Support 💬

If you have any questions or need help with setup, please open an issue on GitHub.

---

Made with ❤️ and 🎵 by the Song Reccy team
