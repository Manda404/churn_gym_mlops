# src/churn_gym/application/use_cases/build_features.py
from typing import Iterable,  List
from churn_gym.domain.interfaces.feature_engineering_pipeline import FeatureEngineeringPipeline
from churn_gym.domain.entities.member_record import MemberRecord
from churn_gym.domain.entities.feature_vector import FeatureVector


class BuildFeaturesUseCase:

    def __init__(self, pipeline: FeatureEngineeringPipeline):
        self.pipeline = pipeline

    def execute(
        self,
        records: Iterable[MemberRecord],
    ) -> List[FeatureVector]:
        return self.pipeline.run(records)
