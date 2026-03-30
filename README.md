# 🌾 Kisan AI — Smart Farmer Crop Advisory System

AI-powered crop recommendation system built with **Python + Django + MySQL + Scikit-learn**

---

## 🤖 3 AI Features

| Feature | Algorithm | What it does |
|---------|-----------|-------------|
| Crop Recommendation | Random Forest | Suggests best crop from N, P, K, pH, rainfall, temperature, humidity |
| Yield Prediction | Linear Regression | Predicts expected yield in kg/acre |
| Fertilizer Advisory | Rule-based ML | Suggests Urea, SSP, MOP based on soil nutrient gaps |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11 + Django 4.2
- **Database**: MySQL
- **AI/ML**: Scikit-learn, NumPy, Pandas
- **Frontend**: HTML5 + CSS3 (no framework — pure custom)
- **Deployment**: Railway.app (free tier)

---

## 🚀 Local Setup (Step by Step)

### 1. Clone & Enter Project
```bash
git clone <your-repo-url>
cd farmer_crop_ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MySQL Database
```sql
-- Run in MySQL Workbench or terminal
CREATE DATABASE farmer_crop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env and fill in your MySQL password
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Admin User
```bash
python manage.py createsuperuser
```

### 8. Run Server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## 📁 Project Structure

```
farmer_crop_ai/
├── manage.py
├── requirements.txt
├── Procfile               ← Railway deployment
├── railway.json           ← Railway config
├── .env.example
│
├── farmer_crop_ai/        ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                  ← Main Django app
│   ├── models.py          ← FarmerProfile, CropAdvisory, WeatherData
│   ├── views.py           ← All page views + AJAX endpoint
│   ├── urls.py
│   └── admin.py
│
├── ai/                    ← All AI/ML code
│   └── crop_ai.py         ← CropRecommender, YieldPredictor, FertilizerAdvisor
│
└── templates/
    └── core/
        ├── base.html          ← Navigation, footer, styles
        ├── home.html          ← Landing page
        ├── login.html
        ├── register.html
        ├── dashboard.html     ← Stats + recent advisories
        ├── get_advisory.html  ← Form with LIVE AI preview
        ├── result.html        ← Full AI result page
        └── history.html       ← All past advisories
```

---


## 👨‍🌾 Supported Crops (15+)

Rice, Maize, Wheat, Cotton, Chickpea, Jute, Mungbean, Lentil,
Banana, Mango, Grapes, Watermelon, Coconut, Papaya, Orange, Pomegranate

---

Built with ❤️ for Indian Farmers | Python + Django + MySQL + Scikit-learn
