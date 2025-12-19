# src/churn_gym/domain/interfaces/feature_engineering_pipeline.py
from typing import Iterable
from abc import ABC, abstractmethod
from churn_gym.domain.entities.member_record import MemberRecord


class FeatureEngineeringPipeline(ABC):

    @abstractmethod
    def run(
        self, records: Iterable[MemberRecord]
    ) -> list[MemberRecord]:
        pass
