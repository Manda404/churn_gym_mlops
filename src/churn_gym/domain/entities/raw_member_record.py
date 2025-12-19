# src/churn_gym/domain/entities/raw_member_record.py
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class RawMemberRecord:
    member_id: str
    name: Optional[str]
    age: Optional[float]                 # dans ton CSV : 19.0 etc.
    gender: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    membership_type: Optional[str]
    join_date: Optional[date]
    last_visit_date: Optional[date]
    favorite_exercise: Optional[str]
    avg_workout_duration_min: Optional[float]
    avg_calories_burned: Optional[float]
    total_weight_lifted_kg: Optional[float]
    visits_per_month: Optional[float]
    churn: Optional[bool]                # None en inference
