# Script to train ML models for risk prediction
# Uses scikit-learn and xgboost

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import joblib

# Load data
data = pd.read_csv('../data/synthetic_data.csv')
# ...add preprocessing and training code here...
