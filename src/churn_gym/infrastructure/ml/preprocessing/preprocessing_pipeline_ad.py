# src/churn_gym/infrastructure/ml/preprocessing/preprocessing_pipeline.py
from churn_gym.domain.interfaces.preprocessing_pipeline import PreprocessingPipeline
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord


class BasicPreprocessingPipeline(PreprocessingPipeline):

    def run(self, raw_records):
        records = []

        for r in raw_records:
            churn = None
            if r.churn is not None:
                churn = 1 if str(r.churn).lower() == "yes" else 0

            records.append(
                MemberRecord(
                    member_id=r.member_id,
                    age=float(r.age) if r.age is not None else None,
                    gender=str(r.gender).lower() if r.gender else None,
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

        return records
