# src/churn_gym/application/use_cases/train_model.py
from churn_gym.domain.interfaces.model_trainer import ModelTrainer
from churn_gym.domain.entities.feature_vector import FeatureVector
from typing import List

class TrainModelUseCase:

    def __init__(self, trainer: ModelTrainer):
        self.trainer = trainer

    def execute(self, features: List[FeatureVector]):
        return self.trainer.train(features)
