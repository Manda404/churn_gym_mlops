# src/churn_gym/application/use_cases/load_dataset.py
from churn_gym.domain.interfaces.dataset_repository import DatasetRepository


class LoadDatasetUseCase:

    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def execute(self):
        return self.repository.load_raw()
