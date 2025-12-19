from typing import Iterable
import numpy as np

from churn_gym.domain.interfaces.preprocessing_pipeline import PreprocessingPipeline
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord


class RobustPreprocessingPipeline(PreprocessingPipeline):
    """
    Responsibilities:
    - Cast types
    - Handle missing values
    - Normalize categorical values
    - Normalize target
    - Guarantee: no None in numerical / categorical features
    """

    def run(self, raw_records: Iterable[RawMemberRecord]) -> list[MemberRecord]:
        records: list[MemberRecord] = []

        for r in raw_records:
            # =====================
            # Target normalization
            # =====================
            if r.churn is None:
                churn = np.nan
            else:
                churn = 1 if str(r.churn).strip().lower() == "yes" else 0

            # =====================
            # Numerical features
            # =====================
            age = float(r.age) if r.age is not None else np.nan
            avg_workout_duration_min = (
                float(r.avg_workout_duration_min)
                if r.avg_workout_duration_min is not None
                else np.nan
            )
            avg_calories_burned = (
                float(r.avg_calories_burned)
                if r.avg_calories_burned is not None
                else np.nan
            )
            total_weight_lifted_kg = (
                float(r.total_weight_lifted_kg)
                if r.total_weight_lifted_kg is not None
                else np.nan
            )
            visits_per_month = (
                float(r.visits_per_month)
                if r.visits_per_month is not None
                else np.nan
            )

            # =====================
            # Categorical features
            # =====================
            gender = str(r.gender).strip().lower() if r.gender else "UNKNOWN"
            membership_type = (
                str(r.membership_type).strip()
                if r.membership_type
                else "UNKNOWN"
            )
            favorite_exercise = (
                str(r.favorite_exercise).strip()
                if r.favorite_exercise
                else "UNKNOWN"
            )

            # =====================
            # Dates (kept as-is)
            # =====================
            join_date = r.join_date
            last_visit_date = r.last_visit_date

            # =====================
            # Build clean MemberRecord
            # =====================
            records.append(
                MemberRecord(
                    member_id=str(r.member_id),
                    age=age,
                    gender=gender,
                    membership_type=membership_type,
                    join_date=join_date,
                    last_visit_date=last_visit_date,
                    favorite_exercise=favorite_exercise,
                    avg_workout_duration_min=avg_workout_duration_min,
                    avg_calories_burned=avg_calories_burned,
                    total_weight_lifted_kg=total_weight_lifted_kg,
                    visits_per_month=visits_per_month,
                    churn=churn,
                )
            )

        return records
