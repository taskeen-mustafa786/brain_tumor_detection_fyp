# 🧠 Brain Tumor Detection - Final Year Project

> A comprehensive web-based application for automated brain tumor detection using state-of-the-art AI/ML technologies with cloud integration and HIPAA-compliant patient management.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.1-red)](https://streamlit.io/)
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
- **Secure Authentication** - Ready for production deployment
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

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Usage Guide

### 1. Make a Prediction
```
📥 Upload MRI/CT scan → 👤 Select/Register patient → ⚙️ Set threshold → 🔮 Analyze → 💾 Save
```

### 2. View Patient Records
```
Search patient → View history → Add records → Export data
```

### 3. Compare Models
```
View metrics → Analyze performance → Compare F1/Precision/Recall → Export comparison
```

## 📁 Project Structure

```
brain_tumor_detection_fyp/
├── 📄 README.md                 ← You are here
├── 📄 CLOUD_SETUP.md            ← Cloud deployment guide
├── 🐍 app.py                    ← Main Streamlit app
├── 📋 requirements.txt           ← Dependencies
├── 📋 .env.example              ← Configuration template
├── .streamlit/
│   └── config.toml              ← Streamlit settings
├── 📁 utils/
│   ├── model_utils.py           ← Model & prediction logic
│   ├── firestore_config.py      ← Cloud database wrapper
│   └── patient_db.py            ← Patient management
├── 📁 pages/
│   ├── dashboard.py             ← Overview dashboard
│   ├── predict.py               ← Prediction interface
│   ├── patient_records.py       ← Patient management UI
│   └── model_comparison.py      ← Results & comparison
├── 📁 TL-Model/
│   ├── TL_btd_model.h5          ← Transfer learning model
│   └── TL_btd_model.ipynb       ← Training notebook
└── 📁 model_from_scratch/
    ├── btd_model2.h5            ← Custom CNN model
    └── Copy_of_Model_development_Training_Evolution.ipynb
```

## 💻 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Streamlit | 1.31.1 |
| **ML/DL** | TensorFlow/Keras | 2.14.0 |
| **Database** | Firebase Firestore | - |
| **Visualization** | Plotly | 5.18.0 |
| **Python** | Python | 3.8+ |
| **Cloud** | Google Cloud | - |

## 📚 Documentation

- [Installation Guide](CLOUD_SETUP.md#-installation)
- [Configuration Guide](CLOUD_SETUP.md#-configuration)
- [Usage Guide](CLOUD_SETUP.md#-usage-guide)
- [Deployment Guide](CLOUD_SETUP.md#-deployment)
- [Security Guide](CLOUD_SETUP.md#-security--privacy)

## 🔐 Security & Compliance

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
- **Streamlit** - Web framework
- **Firebase** - Cloud infrastructure

---

**<div align="center">Automated Brain Tumor Detection | Version 1.0 | 2026</div>**
