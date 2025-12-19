# src/churn_gym/infrastructure/ml/predict//catboost_predictor.py
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.interfaces.model_predictor import ModelPredictor
from churn_gym.infrastructure.ml.features.features_selection import FEATURES_ALL

class CatBoostPredictor(ModelPredictor):

    def __init__(self, model_path: str, categorical_features: list[str]):
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)
        self.categorical_features = categorical_features

    def predict_proba(self, features: list[FeatureVector]) -> list[float]:
        df = pd.DataFrame([f.__dict__ for f in features])

        # sécurité: None -> NaN
        df = df.replace({None: np.nan})

        # en inférence on ne doit pas avoir churn, mais on sécurise
        if "churn" in df.columns:
            df = df.drop(columns=["churn"])

        # catégorielles => string
        for col in self.categorical_features:
            df[col] = df[col].astype("string")

        probs = self.model.predict_proba(df)[:, 1]
        return [float(p) for p in probs]
