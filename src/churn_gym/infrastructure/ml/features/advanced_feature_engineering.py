# src/churn_gym/infrastructure/ml/features/advanced_feature_engineering.py
from churn_gym.domain.interfaces.feature_engineering_pipeline import FeatureEngineeringPipeline
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.entities.member_record import MemberRecord
from typing import List, Iterable
from datetime import date

class AdvancedFeatureEngineeringPipeline(FeatureEngineeringPipeline):

    def run(self, records: Iterable[MemberRecord]) -> List[FeatureVector]:
        today = date.today()
        features = []

        for r in records:
            # 1. Calculs temporels de base
            tenure_days = (r.last_visit_date - r.join_date).days if r.join_date and r.last_visit_date else None
            days_since_last_visit = (today - r.last_visit_date).days if r.last_visit_date else None

            # 2. Bucketing (Catégories)
            tenure_bucket = "unknown"
            if tenure_days is not None:
                if tenure_days < 90: tenure_bucket = "short"
                elif tenure_days < 365: tenure_bucket = "medium"
                else: tenure_bucket = "long"

            visit_recency_bucket = "unknown"
            if days_since_last_visit is not None:
                visit_recency_bucket = "recent" if days_since_last_visit < 30 else "stale"

            # 3. Ratios Avancés
            # Ratio d'activité (visites par rapport au mois)
            attendance_rate = float(r.visits_per_month / 30) if r.visits_per_month else 0.0
            # Score RFM (Recency/Frequency) : Plus il est haut, plus le risque est grand
            rf_score = 0.0
            if days_since_last_visit is not None and r.visits_per_month and r.visits_per_month > 0:
                rf_score = days_since_last_visit / (30 / r.visits_per_month)

            # Intensité de l'entraînement (poids par minute)
            w_intensity = 0.0
            if r.total_weight_lifted_kg and r.avg_workout_duration_min and r.avg_workout_duration_min > 0:
                w_intensity = r.total_weight_lifted_kg / r.avg_workout_duration_min

            features.append(
                FeatureVector(
                    member_id=r.member_id,
                    age=float(r.age) if r.age is not None else None,
                    avg_workout_duration_min=float(r.avg_workout_duration_min or 0),
                    avg_calories_burned=float(r.avg_calories_burned or 0),
                    total_weight_lifted_kg=float(r.total_weight_lifted_kg or 0),
                    visits_per_month=float(r.visits_per_month or 0),
                    gender=str(r.gender or "unknown"),
                    membership_type=str(r.membership_type or "unknown"),
                    favorite_exercise=str(r.favorite_exercise or "unknown"),
                    tenure_days=float(tenure_days) if tenure_days is not None else None,
                    days_since_last_visit=float(days_since_last_visit) if days_since_last_visit is not None else None,
                    tenure_bucket=tenure_bucket,
                    visit_recency_bucket=visit_recency_bucket,
                    calories_per_minute=float(r.avg_calories_burned / r.avg_workout_duration_min) if r.avg_calories_burned and r.avg_workout_duration_min else 0.0,
                    weight_per_visit=float(r.total_weight_lifted_kg / r.visits_per_month) if r.total_weight_lifted_kg and r.visits_per_month else 0.0,
                    attendance_rate=attendance_rate,
                    recency_frequency_score=rf_score,
                    weight_intensity=w_intensity,
                    churn=int(r.churn) if r.churn is not None else 0,
                )
            )
        return features