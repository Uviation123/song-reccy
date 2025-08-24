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
   - **Redirect URIs**: 
     - **Recommended**: `http://127.0.0.1:5000/api/callback` (for development)
     - **Legacy fallback**: `http://127.0.0.1:5000/callback` (if you already have this configured)
     - **Production**: `https://your-domain.com/api/callback` (replace with your actual domain)
4. Save your **Client ID** and **Client Secret**

**Important**: 
- The app supports both `/callback` and `/api/callback` routes for backwards compatibility
- We recommend using `/api/callback` for new setups
- You must add both development and production redirect URIs to your Spotify app

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
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/api/callback
SECRET_KEY=any_random_string_here
```

**Note**: For development, use the localhost redirect URI as shown above. For production deployment, you'll need to set the production redirect URI as an environment variable.

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

## Production Deployment

### Fly.io Deployment

1. **Set Production Environment Variables**:
   ```bash
   fly secrets set SPOTIFY_CLIENT_ID=your_client_id_here
   fly secrets set SPOTIFY_CLIENT_SECRET=your_client_secret_here
   fly secrets set SPOTIFY_REDIRECT_URI=https://your-app-name.fly.dev/api/callback
   fly secrets set SECRET_KEY=your_secure_random_key_here
   ```

2. **Update Spotify App Settings**:
   - Go to your Spotify Developer Dashboard
   - Edit your app
   - Add your production redirect URI: `https://your-app-name.fly.dev/api/callback`
   - Make sure to keep the development URI as well

3. **Deploy**:
   ```bash
   fly deploy
   ```

### Common Production Issues

1. **"Invalid redirect URI" error**:
   - Make sure your production domain is added to Spotify app settings
   - Verify the SPOTIFY_REDIRECT_URI environment variable matches exactly

2. **Redirects to IP address instead of domain**:
   - This issue should be fixed with the latest updates
   - The app now auto-detects the correct domain for redirects

3. **Spotify redirects to /callback instead of /api/callback**:
   - The app now supports both routes for backwards compatibility
   - If you see this in the logs, consider updating your Spotify app settings to use `/api/callback`
   - Both routes will work, but `/api/callback` is the recommended path
   - Make sure frontend is running on port 3000

4. **No recommendations appearing**
   - Make sure you have listening history on Spotify
   - Try the "Analyze My Taste" button first

Need more help? Check the full README.md or open an issue on GitHub!
