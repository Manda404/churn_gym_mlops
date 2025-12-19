# src/churn_gym/domain/entities/prediction.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    churn_probability: float
    churn_label: int  # 0 / 1
    risk_level: str
    threshold_used: float