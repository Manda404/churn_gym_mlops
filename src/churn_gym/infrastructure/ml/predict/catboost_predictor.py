# src/churn_gym/infrastructure/ml/predict//catboost_predictor.py
import numpy as np
import pandas as pd
from typing import Union
from catboost import CatBoostClassifier
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.interfaces.model_predictor import ModelPredictor
from churn_gym.infrastructure.ml.features.features_selection import FEATURES_ALL, TARGET_COLUMN, CATEGORICAL_FEATURES
from pathlib import Path
class CatBoostPredictor(ModelPredictor):

    def __init__(self, model_path: Union[str, Path]):  # categorical_features: list[str]
        self.model = CatBoostClassifier()
        self.model.load_model(Path(model_path))

    def score(self, features: list[FeatureVector]) -> list[float]:
        df = pd.DataFrame([f.__dict__ for f in features])
        probs = self.model.predict_proba(df[FEATURES_ALL])[:, 1]
        return [float(p) for p in probs]
