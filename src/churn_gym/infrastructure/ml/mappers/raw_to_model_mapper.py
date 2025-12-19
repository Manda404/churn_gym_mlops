# src/churn_gym/infrastructure/ml/mappers/raw_to_model_mapper.py
from churn_gym.domain.interfaces.record_mapper import RecordMapper
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord


class RawToModelRecordMapper(RecordMapper):
    def to_model_record(self, raw: RawMemberRecord) -> MemberRecord:
        return MemberRecord(
            member_id=raw.member_id,
            age=raw.age,
            gender=raw.gender,
            membership_type=raw.membership_type,
            join_date=raw.join_date,
            last_visit_date=raw.last_visit_date,
            favorite_exercise=raw.favorite_exercise,
            avg_workout_duration_min=raw.avg_workout_duration_min,
            avg_calories_burned=raw.avg_calories_burned,
            total_weight_lifted_kg=raw.total_weight_lifted_kg,
            visits_per_month=raw.visits_per_month,
            churn=raw.churn,
        )
