# src/churn_gym/domain/interfaces/preprocessing_pipeline.py
from abc import ABC, abstractmethod
from typing import Iterable
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord


class PreprocessingPipeline(ABC):

    @abstractmethod
    def run(
        self, raw_records: Iterable[RawMemberRecord]
    ) -> list[MemberRecord]:
        pass
