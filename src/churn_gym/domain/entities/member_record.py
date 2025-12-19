# src/churn_gym/domain/entities/member_record.py
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class MemberRecord:
    member_id: str
    age: Optional[float]
    gender: Optional[str]
    membership_type: Optional[str]
    join_date: Optional[date]
    last_visit_date: Optional[date]
    favorite_exercise: Optional[str]
    avg_workout_duration_min: Optional[float]
    avg_calories_burned: Optional[float]
    total_weight_lifted_kg: Optional[float]
    visits_per_month: Optional[float]
    churn: Optional[bool]  # None en inference
