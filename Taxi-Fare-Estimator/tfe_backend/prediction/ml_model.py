import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib

SCALER_PATH = 'scaler.joblib'
MODEL_PATH = 'ml_model.joblib'

class TaxiFareEstimator:
    def __init__(self):
        """
        Initialize the estimator with an XGBoost model and a scaler.
        """
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def preprocess(self, df, fit_scaler=False):
        """
        Clean, prepare, and scale the dataset.
        """
        features = ['distance', 'time', 'day_of_week', 'passengers']
        X = df[features]
        y = df["fare"]

        if fit_scaler:
            self.scaler.fit(X)
        
        X_scaled = self.scaler.transform(X)
        return X_scaled, y

    def train(self, df):
        """
        Train model on the provided dataset.
        """
        X_scaled, y = self.preprocess(df, fit_scaler=True)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        print("Model trained successfully")
        self.save_model()

    def predict(self, ride_features):
        """
        Predict fare for a single ride.
        ride_features: dict with keys like distance, time, day_of_week, passengers
        """
        if not self.is_trained:
            try:
                self.load_model()
            except FileNotFoundError:
                raise Exception("Model is not trained yet and could not be loaded!")

        # Create a DataFrame from the input dictionary
        X = pd.DataFrame([ride_features])
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)[0]

    def evaluate(self, df):
        """
        Evaluate model performance (MAE, RMSE).
        """
        X_scaled, y = self.preprocess(df)
        preds = self.model.predict(X_scaled)
        mae = mean_absolute_error(y, preds)
        rmse = np.sqrt(mean_squared_error(y, preds))
        return {"MAE": mae, "RMSE": rmse}

    def save_model(self):
        """
        Save trained model and scaler to disk.
        """
        joblib.dump(self.scaler, SCALER_PATH)
        joblib.dump(self.model, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH} and scaler to {SCALER_PATH}")

    def load_model(self):
        """
        Load trained model and scaler from disk.
        """
        self.scaler = joblib.load(SCALER_PATH)
        self.model = joblib.load(MODEL_PATH)
        self.is_trained = True
        print(f"Model and scaler loaded from disk")
