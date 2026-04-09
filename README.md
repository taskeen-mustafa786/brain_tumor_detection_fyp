# 🧠 Brain Tumor Detection - Final Year Project

> A comprehensive web-based application for automated brain tumor detection using state-of-the-art AI/ML technologies with cloud integration and HIPAA-compliant patient management.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)](https://fastapi.tiangolo.com/)
[![TensorFlow 2.14](https://img.shields.io/badge/TensorFlow-2.14-orange)](https://www.tensorflow.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-yellow)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-FYP-green)](#license)

## 📚 Table of Contents

- [Features](#features)
- [Model Performance](#model-performance)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Documentation](#documentation)
- [Contributing](#contributing)

## ✨ Features

### 🤖 AI/ML Capabilities
- **90.59% Accuracy** - EfficientNetB0 transfer learning model
- **Real-time Predictions** - Instant tumor detection on MRI/CT scans
- **Model Comparison** - Comprehensive metrics and performance analysis
- **Confidence Scoring** - Detailed prediction confidence levels

### 👥 Patient Management
- **Patient Registry** - Secure patient record system
- **Medical History** - Track medications, allergies, procedures
- **Prediction History** - Complete scan history per patient
- **Easy Search** - Quick patient lookup and filtering

### ☁️ Cloud Integration
- **Firestore Database** - HIPAA-compliant cloud storage
- **Demo Mode** - Works without credentials (in-memory storage)
- **Secure Authentication** - JWT-based authentication
- **Scalable Architecture** - Built for growth

### 📊 Analytics & Reports
- **Test Results Dashboard** - F1-score, recall, precision, AUC-ROC
- **Model Performance Comparison** - Side-by-side model analysis
- **System Monitoring** - Real-time status and metrics
- **Data Visualization** - Interactive charts and graphs

## 📊 Model Performance

### Transfer Learning Model (EfficientNetB0) ✅ RECOMMENDED

| Metric | Score | Status |
|--------|-------|--------|
| **Accuracy** | 90.59% | ✅ Meets SRS |
| **Precision** | 91.45% | ✅ Excellent |
| **Recall** | 88.76% | ✅ Excellent |
| **F1-Score** | 0.9008 | ✅ Best |
| **AUC-ROC** | 0.9532 | ✅ Excellent |
| **Val Loss** | 0.2618 | ✅ Low |

**Status**: ✅ Production Ready - Exceeds all requirements

### Custom CNN Model (From Scratch) ⚠️ ALTERNATIVE

| Metric | Score | Status |
|--------|-------|--------|
| **Accuracy** | 83.37% | ⚠️ Below SRS |
| **Precision** | 84.21% | ✅ Good |
| **Recall** | 81.54% | ✅ Good |
| **F1-Score** | 0.8286 | ✅ Good |
| **AUC-ROC** | 0.8947 | ✅ Good |
| **Val Loss** | 0.4112 | ⚠️ Higher |

**Status**: ⚠️ Research/Backup - Not for production

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda
- 2GB RAM minimum

### Installation (2 minutes)

```bash
# Clone repository
git clone <repository-url>
cd brain_tumor_detection_fyp

# Backend Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup (optional for development)
npm install

# Start Backend
cd backend
python main.py
```

The backend will run at `http://localhost:8001`

## 📖 Usage Guide

### 1. Access the Application
- Open `index.html` in your web browser (backend must be running)
- Backend runs on `http://localhost:8001`

### 2. Make a Prediction
```
📥 Upload MRI/CT scan → 👤 Login/Register → ⚙️ Set parameters → 🔮 Analyze → 💾 Save results
```

### 3. View Patient Records
```
Login → View dashboard → Access medical history → Review predictions
```

### 4. Model Information
```
Dashboard → Model Performance → View metrics and comparisons
```

## 📁 Project Structure

```
brain_tumor_detection_fyp/
├── 📄 README.md                 ← You are here
├── 🌐 index.html                ← Main frontend application
├── 📋 requirements.txt          ← Backend dependencies
├── 📁 backend/
│   └── 🐍 main.py               ← FastAPI backend server
├── 📁 utils/
│   ├── model_utils.py           ← Model & prediction logic
│   ├── firestore_config.py      ← Cloud database wrapper
│   └── patient_db.py            ← Patient management
├── 📁 TL-Model/
│   └── TL_btd_model.h5          ← Transfer learning model
└── 📁 model_from_scratch/
    └── btd_model2.h5            ← Custom CNN model
```

## 💻 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | HTML/CSS/JavaScript | - |
| **Backend** | FastAPI | 0.104.1 |
| **ML/DL** | TensorFlow/Keras | 2.14.0 |
| **Database** | Firebase Firestore | - |
| **Authentication** | JWT + Firebase Auth | - |
| **Python** | Python | 3.8+ |

##  Security & Compliance

✅ HIPAA-ready architecture
✅ Data encryption support
✅ Firebase security rules
✅ No credential hardcoding
✅ Audit logging ready

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of a Final Year Project (FYP). See LICENSE file for details.

## 👨‍💼 Contact & Support

- **Email**: [project-email]
- **GitHub Issues**: [Create an issue](../../issues)
- **Documentation**: [Full Guide](CLOUD_SETUP.md)

## 🙏 Acknowledgments

- **EfficientNetB0** - ImageNet pretrained weights
- **TensorFlow** - Deep learning framework
- **FastAPI** - Modern Python web framework
- **Firebase** - Cloud infrastructure

---

**<div align="center">Automated Brain Tumor Detection | Version 1.0 | 2026</div>**
