"""
AI Module for Farmer Crop Advisory System
3 AI Features:
1. Crop Recommendation (Random Forest)
2. Yield Prediction (Linear Regression)
3. Fertilizer Suggestion (Rule-based + ML)
"""

import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ─── Training Data ────────────────────────────────────────────────────────────
# Each row: [N, P, K, pH, rainfall, temperature, humidity] → crop

CROP_DATA = [
    # N,   P,   K,   pH,  rain, temp, humid, crop
    [90,  42,  43,  6.5, 202,  27,   82,   'rice'],
    [85,  58,  41,  7.0, 230,  26,   80,   'rice'],
    [60,  55,  44,  7.0, 203,  28,   82,   'rice'],
    [74,  46,  38,  6.5, 236,  26,   83,   'rice'],
    [78,  52,  36,  7.0, 221,  25,   81,   'rice'],

    [83,  45,  60,  7.0, 67,   28,   65,   'maize'],
    [85,  58,  41,  6.5, 71,   29,   67,   'maize'],
    [82,  47,  50,  7.0, 75,   28,   65,   'maize'],
    [88,  50,  45,  6.8, 73,   30,   68,   'maize'],
    [84,  53,  55,  7.2, 69,   27,   64,   'maize'],

    [0,   45,  35,  6.5, 202,  24,   92,   'jute'],
    [10,  40,  30,  7.0, 220,  23,   90,   'jute'],
    [5,   42,  32,  6.8, 210,  25,   91,   'jute'],

    [21,  67,  17,  6.0, 89,   23,   68,   'cotton'],
    [18,  60,  15,  6.5, 92,   25,   70,   'cotton'],
    [20,  65,  18,  6.0, 85,   24,   69,   'cotton'],
    [22,  68,  20,  6.5, 90,   26,   71,   'cotton'],

    [0,   40,  40,  6.5, 50,   28,   65,   'chickpea'],
    [10,  45,  35,  7.0, 55,   27,   63,   'chickpea'],
    [5,   42,  38,  6.8, 48,   29,   64,   'chickpea'],

    [80,  40,  40,  6.5, 150,  27,   75,   'wheat'],
    [75,  45,  35,  7.0, 160,  25,   73,   'wheat'],
    [82,  42,  38,  6.8, 155,  26,   74,   'wheat'],
    [78,  44,  37,  7.0, 145,  28,   76,   'wheat'],

    [40,  20,  20,  6.5, 75,   30,   55,   'mungbean'],
    [45,  25,  15,  7.0, 80,   32,   57,   'mungbean'],
    [42,  22,  18,  6.8, 78,   31,   56,   'mungbean'],

    [20,  80,  40,  6.5, 120,  28,   70,   'banana'],
    [25,  75,  45,  6.8, 130,  27,   72,   'banana'],
    [22,  78,  42,  7.0, 125,  29,   71,   'banana'],

    [20,  60,  200, 6.5, 150,  29,   75,   'mango'],
    [25,  55,  190, 6.8, 160,  28,   73,   'mango'],
    [22,  58,  195, 7.0, 155,  30,   74,   'mango'],

    [94,  0,   40,  5.5, 145,  24,   65,   'grapes'],
    [90,  5,   35,  5.8, 140,  26,   67,   'grapes'],
    [92,  2,   38,  5.5, 150,  25,   66,   'grapes'],

    [100, 18,  20,  6.0, 300,  27,   88,   'watermelon'],
    [95,  20,  18,  6.2, 290,  28,   86,   'watermelon'],
    [98,  15,  22,  6.0, 310,  26,   87,   'watermelon'],

    [110, 55,  44,  6.5, 95,   39,   40,   'lentil'],
    [105, 50,  40,  6.8, 90,   38,   42,   'lentil'],
    [108, 52,  42,  7.0, 92,   37,   41,   'lentil'],

    [50,  34,  30,  6.5, 50,   30,   55,   'pomegranate'],
    [48,  36,  28,  6.8, 52,   32,   57,   'pomegranate'],
    [52,  33,  32,  7.0, 48,   31,   56,   'pomegranate'],

    [10,  30,  35,  6.5, 600,  30,   90,   'coconut'],
    [15,  28,  32,  6.8, 650,  28,   92,   'coconut'],
    [12,  32,  38,  7.0, 580,  29,   91,   'coconut'],

    [25,  60,  60,  6.0, 200,  35,   70,   'papaya'],
    [28,  58,  55,  6.2, 210,  34,   72,   'papaya'],
    [22,  62,  58,  6.5, 195,  36,   71,   'papaya'],

    [55,  24,  40,  5.8, 120,  30,   68,   'orange'],
    [58,  22,  38,  6.0, 130,  28,   66,   'orange'],
    [52,  25,  42,  5.8, 125,  32,   70,   'orange'],
]

# Yield training data: [N, P, K, pH, rainfall, temp, humidity] → yield (kg/acre)
YIELD_DATA = [
    # N,   P,  K,   pH,  rain, temp, humid, yield
    [90,  42,  43,  6.5, 202,  27,   82,   1800],
    [85,  58,  41,  7.0, 230,  26,   80,   1950],
    [60,  30,  30,  6.0, 150,  28,   75,   1200],
    [40,  20,  25,  5.5, 100,  30,   65,   900],
    [120, 60,  55,  7.0, 250,  25,   85,   2400],
    [100, 50,  50,  6.8, 220,  26,   83,   2200],
    [75,  40,  42,  6.5, 180,  27,   80,   1600],
    [50,  25,  30,  5.8, 120,  31,   68,   1100],
    [110, 55,  48,  7.2, 240,  24,   88,   2300],
    [30,  15,  20,  5.5, 90,   33,   60,   800],
    [95,  48,  45,  6.8, 210,  27,   81,   2000],
    [65,  35,  38,  6.2, 165,  29,   73,   1400],
    [80,  45,  44,  6.5, 195,  27,   79,   1750],
    [55,  28,  32,  5.9, 130,  30,   70,   1050],
    [105, 52,  50,  7.0, 235,  25,   84,   2350],
]


class CropRecommender:
    """AI Feature 1: Recommend best crop using Random Forest"""

    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self._train()

    def _train(self):
        data = np.array(CROP_DATA)
        X = data[:, :7].astype(float)
        y = data[:, 7]

        y_encoded = self.label_encoder.fit_transform(y)

        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.model.fit(X, y_encoded)

    def predict(self, N, P, K, ph, rainfall, temperature, humidity):
        """Returns (recommended_crop, confidence, top_3_with_scores)"""
        features = np.array([[N, P, K, ph, rainfall, temperature, humidity]])
        proba = self.model.predict_proba(features)[0]

        top3_idx = np.argsort(proba)[::-1][:3]
        top3 = [
            {
                'crop': self.label_encoder.classes_[i],
                'score': round(float(proba[i]) * 100, 1)
            }
            for i in top3_idx
        ]

        best_crop = top3[0]['crop']
        confidence = top3[0]['score']

        return best_crop, confidence, top3


class YieldPredictor:
    """AI Feature 2: Predict crop yield using Linear Regression"""

    def __init__(self):
        self.model = LinearRegression()
        self._train()

    def _train(self):
        data = np.array(YIELD_DATA)
        X = data[:, :7]
        y = data[:, 7]
        self.model.fit(X, y)

    def predict(self, N, P, K, ph, rainfall, temperature, humidity):
        """Returns predicted yield in kg/acre and category"""
        features = np.array([[N, P, K, ph, rainfall, temperature, humidity]])
        yield_val = max(500, float(self.model.predict(features)[0]))
        yield_val = round(yield_val)

        if yield_val < 1000:
            category = 'low'
        elif yield_val < 1800:
            category = 'medium'
        else:
            category = 'high'

        return yield_val, category


class FertilizerAdvisor:
    """AI Feature 3: Suggest fertilizer based on soil N, P, K levels"""

    CROP_REQUIREMENTS = {
        'rice':       {'N': 100, 'P': 50, 'K': 50},
        'maize':      {'N': 90,  'P': 60, 'K': 55},
        'wheat':      {'N': 80,  'P': 45, 'K': 40},
        'cotton':     {'N': 60,  'P': 70, 'K': 25},
        'chickpea':   {'N': 20,  'P': 50, 'K': 40},
        'mungbean':   {'N': 40,  'P': 30, 'K': 25},
        'lentil':     {'N': 110, 'P': 55, 'K': 45},
        'banana':     {'N': 25,  'P': 80, 'K': 50},
        'mango':      {'N': 25,  'P': 60, 'K': 200},
        'grapes':     {'N': 95,  'P': 5,  'K': 38},
        'watermelon': {'N': 100, 'P': 20, 'K': 22},
        'coconut':    {'N': 12,  'P': 32, 'K': 38},
        'papaya':     {'N': 25,  'P': 60, 'K': 60},
        'orange':     {'N': 55,  'P': 24, 'K': 42},
        'pomegranate':{'N': 50,  'P': 35, 'K': 30},
        'jute':       {'N': 5,   'P': 42, 'K': 32},
        'default':    {'N': 70,  'P': 45, 'K': 40},
    }

    FERTILIZERS = {
        'N_low':  'Add Urea (46-0-0) — 50 kg/acre to boost Nitrogen',
        'N_ok':   'Nitrogen is sufficient. No Urea needed.',
        'N_high': 'Nitrogen is high. Reduce Urea application.',
        'P_low':  'Add Single Super Phosphate (SSP) — 25 kg/acre for Phosphorus',
        'P_ok':   'Phosphorus level is adequate.',
        'P_high': 'Phosphorus is excess. Avoid DAP this season.',
        'K_low':  'Add Muriate of Potash (MOP) — 30 kg/acre for Potassium',
        'K_ok':   'Potassium level is good.',
        'K_high': 'Potassium is high. Skip MOP this season.',
    }

    def suggest(self, crop, N, P, K):
        req = self.CROP_REQUIREMENTS.get(crop, self.CROP_REQUIREMENTS['default'])

        def level(actual, required):
            ratio = actual / required
            if ratio < 0.75:
                return 'low'
            elif ratio > 1.25:
                return 'high'
            return 'ok'

        n_lvl = level(N, req['N'])
        p_lvl = level(P, req['P'])
        k_lvl = level(K, req['K'])

        suggestions = [
            f"🌱 Nitrogen (N): {self.FERTILIZERS[f'N_{n_lvl}']}",
            f"🟤 Phosphorus (P): {self.FERTILIZERS[f'P_{p_lvl}']}",
            f"🟡 Potassium (K): {self.FERTILIZERS[f'K_{k_lvl}']}",
        ]

        if n_lvl == 'low' and p_lvl == 'low':
            suggestions.append("💡 Tip: Consider applying DAP (18-46-0) which provides both N and P together.")

        if n_lvl == 'ok' and p_lvl == 'ok' and k_lvl == 'ok':
            suggestions.append("✅ Soil nutrients are well-balanced for this crop. Maintain current practice.")

        return '\n'.join(suggestions)


# Singleton instances (loaded once at startup)
_crop_recommender = None
_yield_predictor = None
_fertilizer_advisor = None


def get_crop_recommender():
    global _crop_recommender
    if _crop_recommender is None:
        _crop_recommender = CropRecommender()
    return _crop_recommender


def get_yield_predictor():
    global _yield_predictor
    if _yield_predictor is None:
        _yield_predictor = YieldPredictor()
    return _yield_predictor


def get_fertilizer_advisor():
    global _fertilizer_advisor
    if _fertilizer_advisor is None:
        _fertilizer_advisor = FertilizerAdvisor()
    return _fertilizer_advisor
