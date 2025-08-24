# Quick Setup Guide 🚀

## Prerequisites
1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 14+** - [Download here](https://nodejs.org/)
3. **Spotify Developer Account** - [Sign up here](https://developer.spotify.com/)

## Spotify App Configuration

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
2. Click "Create App"
3. Fill in:
   - **App name**: Song Reccy
   - **App description**: AI-powered song recommendations
   - **Redirect URI**: `http://127.0.0.1:5000/callback`
4. Save your **Client ID** and **Client Secret**

## Installation Steps

### Step 1: Setup Backend
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment
1. Copy `env_example.txt` to `.env`
2. Edit `.env` with your Spotify credentials:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
SECRET_KEY=any_random_string_here
```

### Step 3: Setup Frontend
```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Use Startup Scripts
- **Windows**: Double-click `start.bat`
- **Mac/Linux**: Run `./start.sh`

### Option 2: Manual Start
1. **Backend**: 
   ```bash
   cd backend
   python app.py
   ```
2. **Frontend** (in new terminal):
   ```bash
   cd frontend
   npm start
   ```

## Access the App
- Open your browser to: http://127.0.0.1:3000
- Click "Connect with Spotify"
- Authorize the app
- Enjoy your personalized recommendations! 🎵

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Run `pip install -r requirements.txt` in backend folder
   - Run `npm install` in frontend folder

2. **"Authentication failed"**
   - Check your `.env` file has correct Spotify credentials
   - Verify redirect URI matches in Spotify dashboard

3. **CORS errors**
   - Make sure backend is running on port 5000
   - Make sure frontend is running on port 3000

4. **No recommendations appearing**
   - Make sure you have listening history on Spotify
   - Try the "Analyze My Taste" button first

Need more help? Check the full README.md or open an issue on GitHub!
