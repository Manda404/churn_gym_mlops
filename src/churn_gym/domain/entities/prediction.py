from dataclasses import dataclass


@dataclass(frozen=True)
class Prediction:
    """
    Représente une prédiction finale de churn,
    combinant sortie du modèle et décision métier.
    """

    churn_probability: float
    churn_label: int          # 0 = non churn, 1 = churn
    risk_level: str           # low / medium / high
    threshold_used: float
