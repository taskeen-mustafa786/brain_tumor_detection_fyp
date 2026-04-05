# 🚀 Deployment Guide

## Frontend Deployment (GitHub Pages)

### 1. Deploy Frontend to GitHub Pages

```bash
# Install dependencies
npm install

# Deploy to GitHub Pages
npm run deploy
```

**Frontend URL:** https://taskeen-mustafa786.github.io/brain_tumor_detection_fyp

### 2. Update Backend URL in Production

After deploying the backend, update the `API_BASE_URL` in `index.html`:

```javascript
// Replace this line in index.html:
return 'https://your-backend-app.herokuapp.com'; // Replace with your actual backend URL
```

## Backend Deployment (Heroku)

### 1. Create Heroku App

```bash
# Install Heroku CLI
# Create new app
heroku create your-brain-tumor-backend

# Set environment variables
heroku config:set APP_ENV=production
heroku config:set DEBUG=false
heroku config:set PORT=8000
# Add your Firebase config variables here
```

### 2. Deploy Backend

> Note: For Heroku deployment, the root `requirements.txt` now contains the backend dependencies.
> The Streamlit dependencies have been saved to `requirements-streamlit.txt` so the repository can still preserve the frontend dependency list.

```bash
# Login to Heroku
heroku login

# Deploy
git push heroku main

# Or if using different branch
git push heroku frontend-html-css-js:main
```

### 3. Update Frontend

After backend deployment, update the backend URL in `index.html` and redeploy frontend:

```bash
npm run deploy
```

## Environment Variables for Backend

Create a `.env` file in the backend directory with:

```env
# Application
APP_ENV=production
DEBUG=false
PORT=8000

# Firebase Configuration
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id

# Security
JWT_SECRET=your_secure_jwt_secret_here

# Model
MODEL_PATH=TL-Model/TL_btd_model.h5
```

## Alternative Backend Deployment Options

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render
1. Connect GitHub repository
2. Choose "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

## Testing Deployment

1. **Frontend:** Visit https://taskeen-mustafa786.github.io/brain_tumor_detection_fyp
2. **Backend:** Check https://your-backend-url/health
3. **Integration:** Test login, upload, and prediction features

## Troubleshooting

- **CORS Issues:** Ensure backend allows frontend domain
- **Firebase Config:** Verify all Firebase variables are set
- **Model Loading:** Ensure model files are accessible
- **Port Issues:** Check if PORT environment variable is used correctly