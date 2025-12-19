# src/churn_gym/application/use_cases/preprocess_dataset.py
from churn_gym.domain.interfaces.preprocessing_pipeline import PreprocessingPipeline
from churn_gym.domain.entities.raw_member_record import RawMemberRecord
from typing import Iterable


class PreprocessDatasetUseCase:

    def __init__(self, pipeline: PreprocessingPipeline):
        self.pipeline = pipeline

    def execute(
        self, raw_records: Iterable[RawMemberRecord]
    ):
        return self.pipeline.run(raw_records)
