# src/churn_gym/domain/entities/model_artifact.py
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ModelArtifact:
    model_path: str
    numerical_features: List[str]
    categorical_features: List[str]
    feature_names: List[str]
