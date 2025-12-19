# src/churn_gym/domain/entities/feature_vector.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class FeatureVector:
    member_id: str

    # =====================
    # Original numerical
    # =====================
    age: Optional[float]
    avg_workout_duration_min: Optional[float]
    avg_calories_burned: Optional[float]
    total_weight_lifted_kg: Optional[float]
    visits_per_month: Optional[float]

    # =====================
    # Categorical (CatBoost native)
    # =====================
    gender: Optional[str]
    membership_type: Optional[str]
    favorite_exercise: Optional[str]

    # =====================
    # Date-derived features
    # =====================
    tenure_days: Optional[int]
    days_since_last_visit: Optional[int]
    visit_recency_bucket: Optional[str]
    tenure_bucket: Optional[str]

    # =====================
    # Behavioral ratios
    # =====================
    calories_per_minute: Optional[float]
    weight_per_visit: Optional[float]
    
    # Nouveaux ratios ajoutés pour la performance du modèle
    attendance_rate: Optional[float]          # visites / 30 jours
    recency_frequency_score: Optional[float]  # déviation de l'habitude de visite
    weight_intensity: Optional[float]         # kg soulevés / min de workout

    # =====================
    # Target
    # =====================
    churn: Optional[int]  # 0 / 1