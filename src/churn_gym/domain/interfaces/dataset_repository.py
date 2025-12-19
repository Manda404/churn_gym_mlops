# src/churn_gym/domain/interfaces/dataset_repository.py
from abc import ABC, abstractmethod
from typing import Iterable
from churn_gym.domain.entities.raw_member_record import RawMemberRecord


class DatasetRepository(ABC):

    @abstractmethod
    def load_raw(self) -> Iterable[RawMemberRecord]:
        pass
