# src/churn_gym/domain/interfaces/record_mapper.py
from abc import ABC, abstractmethod
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from churn_gym.domain.entities.member_record import MemberRecord


class RecordMapper(ABC):

    @abstractmethod
    def to_model_record(self, raw: RawMemberRecord) -> MemberRecord:
        pass
