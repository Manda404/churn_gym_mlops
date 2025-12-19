# src/churn_gym/infrastructure/data_sources/csv_loader_pandas.py
import pandas as pd
from datetime import datetime
from typing import List

from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.interfaces.dataset_repository import DatasetRepository


class PandasCSVLoader(DatasetRepository):
    """
    Infrastructure adapter:
    - reads CSV with pandas
    - maps rows to RawMemberRecord
    """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_raw(self) -> List[RawMemberRecord]:
        df = pd.read_csv(self.csv_path)

        # Normalize column names (defensive)
        df.columns = [c.strip() for c in df.columns]

        records: List[RawMemberRecord] = []

        for _, row in df.iterrows():
            records.append(
                RawMemberRecord(
                    member_id=str(row["Member_ID"]),
                    name=row.get("Name"),
                    age=row.get("Age"),
                    gender=row.get("Gender"),
                    address=row.get("Address"),
                    phone_number=row.get("Phone_Number"),
                    membership_type=row.get("Membership_Type"),
                    join_date=self._parse_date(row.get("Join_Date")),
                    last_visit_date=self._parse_date(row.get("Last_Visit_Date")),
                    favorite_exercise=row.get("Favorite_Exercise"),
                    avg_workout_duration_min=row.get("Avg_Workout_Duration_Min"),
                    avg_calories_burned=row.get("Avg_Calories_Burned"),
                    total_weight_lifted_kg=row.get("Total_Weight_Lifted_kg"),
                    visits_per_month=row.get("Visits_Per_Month"),
                    churn=row.get("Churn"),
                )
            )

        return records

    @staticmethod
    def _parse_date(value):
        if pd.isna(value):
            return None
        return datetime.strptime(str(value), "%Y-%m-%d").date()
