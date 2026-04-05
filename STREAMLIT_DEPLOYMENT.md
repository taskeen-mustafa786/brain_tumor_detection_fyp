# 🚀 Streamlit Cloud Deployment Guide

## Prerequisites

1. **GitHub Account** - Your code must be on GitHub
2. **Firebase Project** (Optional) - For production database features
3. **Streamlit Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)

## Quick Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has these files:
- `app.py` (main Streamlit app)
- `requirements.txt` (Python dependencies)
- `packages.txt` (system dependencies)
- `.streamlit/config.toml` (Streamlit configuration)
- `.streamlit/secrets.toml.example` (secrets template)

### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub repository
4. Select the main file: `app.py`
5. Click **"Deploy"**

### 3. Configure Secrets (Optional)

For production features, add secrets in Streamlit Cloud:

1. Go to your app dashboard
2. Click **"⋮"** → **"Settings"**
3. Go to **"Secrets"** section
4. Copy the content from `.streamlit/secrets.toml.example`
5. Replace with your actual Firebase credentials

## Firebase Setup (Production)

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Create a project"**
3. Enable **Firestore Database**
4. Enable **Authentication** (Email/Password)

### 2. Get Service Account Credentials

1. Go to **Project Settings** → **Service Accounts**
2. Click **"Generate new private key"**
3. Download the JSON file
4. Extract the values for `secrets.toml`

### 3. Configure Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write for authenticated users
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Demo Mode

The app works in **demo mode** without Firebase:
- ✅ All features functional
- ✅ In-memory data storage
- ✅ Model predictions work
- ❌ Data persistence across sessions

## Troubleshooting

### Common Issues

**1. TensorFlow Installation Fails**
- The app uses `tensorflow==2.15.0` (compatible with Streamlit Cloud)
- If issues persist, try `tensorflow-cpu==2.15.0`

**2. Model Loading Issues**
- Ensure model files are in the repository
- Check file paths in `MODEL_PATH` configuration

**3. Memory Issues**
- Streamlit Cloud has memory limits
- Models load on-demand to save memory
- Consider using smaller model files

**4. Firebase Connection Issues**
- Verify all secrets are correctly set
- Check Firebase project is active
- Ensure Firestore is enabled

### Performance Optimization

1. **Model Caching**: Models are cached in session state
2. **Lazy Loading**: Heavy imports are loaded on-demand
3. **Memory Management**: Large objects are cleared when not needed

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FIREBASE_PROJECT_ID` | Firebase project ID | No (demo mode) |
| `FIREBASE_PRIVATE_KEY` | Service account private key | No (demo mode) |
| `FIREBASE_CLIENT_EMAIL` | Service account email | No (demo mode) |
| `MODEL_PATH` | Path to ML model file | Yes |
| `CONFIDENCE_THRESHOLD` | Prediction confidence threshold | No (default: 0.7) |

## File Structure for Deployment

```
your-repo/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── packages.txt             # System dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example # Secrets template
├── utils/
│   ├── firestore_config.py  # Database operations
│   ├── model_utils.py       # ML model utilities
│   └── patient_db.py        # Patient management
├── TL-Model/
│   └── TL_btd_model.h5      # Trained model
├── pages/
│   ├── dashboard.py         # Dashboard page
│   ├── predict.py           # Prediction page
│   ├── patient_records.py   # Patient records
│   └── model_comparison.py  # Model comparison
└── README.md                # This file
```

## Support

- 📧 **Issues**: Create GitHub issues
- 📖 **Documentation**: Check inline code comments
- 🔧 **Debugging**: Use `st.error()` and `st.write()` for debugging

## Cost Considerations

- **Streamlit Cloud**: Free tier available
- **Firebase**: Free tier (1GB database, 50K reads/day)
- **TensorFlow**: No additional cost

---

🎉 **Happy Deploying!** Your brain tumor detection system is ready for the world!