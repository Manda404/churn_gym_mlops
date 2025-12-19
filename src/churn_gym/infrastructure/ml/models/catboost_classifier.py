# src/churn_gym/infrastructure/ml/catboost/catboost_trainer.py
import pandas as pd
from catboost import CatBoostClassifier, Pool

from churn_gym.domain.interfaces.model_trainer import ModelTrainer
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.entities.model_artifact import ModelArtifact
from churn_gym.infrastructure.ml.features.features_selection import FEATURES_ALL, CATEGORICAL_FEATURES, TARGET_COLUMN, NUMERICAL_FEATURES


class CatBoostTrainer(ModelTrainer):

    def __init__(self, config: dict, output_dir: str = "artifacts"):
        self.config = config
        self.output_dir = output_dir

    def train(self, features: list[FeatureVector]) -> ModelArtifact:
        df = pd.DataFrame([f.__dict__ for f in features])

        y = df[TARGET_COLUMN]
        X = df[FEATURES_ALL]


        pool = Pool(
            data=X,
            label=y,
            cat_features=CATEGORICAL_FEATURES,
        )

        model = CatBoostClassifier(**self.config)
        model.fit(pool, verbose=100)

        model_path = f"{self.output_dir}/catboost_model.cbm"
        model.save_model(model_path)

        return ModelArtifact(
            model_path=model_path,
            numerical_features = NUMERICAL_FEATURES,
            categorical_features=CATEGORICAL_FEATURES,
            feature_names=list(X.columns),
        )
