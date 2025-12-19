# src/churn_gym/domain/interfaces/model_trainer.py
from abc import ABC, abstractmethod
from typing import Any, List
from churn_gym.domain.entities.feature_vector import FeatureVector


class ModelTrainer(ABC):

    @abstractmethod
    def train(self, features: List[FeatureVector]) -> Any:
        pass
