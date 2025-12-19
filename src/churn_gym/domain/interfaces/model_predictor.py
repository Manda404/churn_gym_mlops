# src/churn_gym/domain/interfaces/model_predictor.py
from typing import List
from abc import ABC, abstractmethod
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.entities.prediction import Prediction


class ModelPredictor(ABC):

    @abstractmethod
    def predict(self, features: List[FeatureVector]) -> List[Prediction]:
        pass
