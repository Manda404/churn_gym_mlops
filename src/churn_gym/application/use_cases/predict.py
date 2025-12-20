# src/churn_gym/application/use_cases/predict.py
from typing import List
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.entities.prediction import Prediction
from churn_gym.domain.interfaces.model_predictor import ModelPredictor
from churn_gym.domain.services.threshold_service import ThresholdService


class PredictUseCase:

    def __init__(self, predictor: ModelPredictor, threshold_service: ThresholdService):
        self.predictor = predictor
        self.threshold_service = threshold_service

    def execute(self, features: List[FeatureVector]) -> List[Prediction]:
        probs = self.predictor.score(features)

        preds: List[Prediction] = []
        for p in probs:
            label, risk, threshold_used = self.threshold_service.to_decision(p)
            preds.append(
                Prediction(
                    churn_probability=p,
                    churn_label=label,
                    risk_level=risk,
                    threshold_used=threshold_used,
                )
            )
        return preds
