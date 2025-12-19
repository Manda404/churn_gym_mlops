# src/churn_gym/infrastructure/ml/preprocessing/preprocessing_pipeline.py
from churn_gym.domain.interfaces.preprocessing_pipeline import PreprocessingPipeline
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord
from datetime import date


class BasicPreprocessingPipeline(PreprocessingPipeline):

    def run(self, raw_records):
        processed = []

        for r in raw_records:
            churn = None
            if r.churn is not None:
                churn = True if str(r.churn).lower() == "yes" else False

            processed.append(
                MemberRecord(
                    member_id=r.member_id,
                    age=r.age,
                    gender=r.gender,
                    membership_type=r.membership_type,
                    join_date=r.join_date,
                    last_visit_date=r.last_visit_date,
                    favorite_exercise=r.favorite_exercise,
                    avg_workout_duration_min=r.avg_workout_duration_min,
                    avg_calories_burned=r.avg_calories_burned,
                    total_weight_lifted_kg=r.total_weight_lifted_kg,
                    visits_per_month=r.visits_per_month,
                    churn=churn,
                )
            )

        return processed
