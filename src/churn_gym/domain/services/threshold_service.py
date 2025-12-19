# src/churn_gym/domain/services/threshold_service.py
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ThresholdConfig:
    threshold: float = 0.5
    medium_risk: float = 0.35   # ex: 0.35 à 0.5
    high_risk: float = 0.7      # ex: >= 0.7 (indépendant du threshold de décision)


class ThresholdService:
    """
    Convertit une probabilité en:
    - label binaire via un seuil
    - niveau de risque (low/medium/high)
    - trace du seuil utilisé
    """

    def __init__(self, config: ThresholdConfig):
        self.config = config

    def to_decision(self, p: float) -> Tuple[int, str, float]:
        # Label via seuil de décision
        label = 1 if p >= self.config.threshold else 0

        # Risk level (exemple simple; tu peux ajuster)
        if p >= self.config.high_risk:
            risk = "high"
        elif p >= self.config.medium_risk:
            risk = "medium"
        else:
            risk = "low"

        return label, risk, self.config.threshold
