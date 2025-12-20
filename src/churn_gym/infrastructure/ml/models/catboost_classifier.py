# src/churn_gym/infrastructure/ml/catboost/catboost_trainer.py

from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier, Pool

from churn_gym.domain.interfaces.model_trainer import ModelTrainer
from churn_gym.domain.interfaces.experiment_tracker import ExperimentTracker
from churn_gym.domain.entities.feature_vector import FeatureVector
from churn_gym.domain.entities.model_artifact import ModelArtifact
from churn_gym.infrastructure.logging.loguru_logger import LoguruLogger
from churn_gym.infrastructure.ml.features.features_selection import (
    FEATURES_ALL,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN,
    NUMERICAL_FEATURES,
)
from churn_gym.infrastructure.utils.config_loader import load_yaml_config
from churn_gym.infrastructure.utils.root_finder import get_repository_root
from churn_gym.infrastructure.tracking.run_name_generator import generate_run_name


class CatBoostTrainer(ModelTrainer):
    """
    Trainer CatBoost avec tracking MLflow complet.

    Responsabilités :
    - Entraînement du modèle CatBoost
    - Logging des paramètres, métriques et artefacts
    - Génération des courbes d'entraînement
    - Calcul et visualisation des feature importances
    """

    def __init__(
        self,
        config: dict,
        tracker: ExperimentTracker,
    ):
        self.config = config
        self.tracker = tracker
        self.logger = LoguruLogger()

        self.run_name = generate_run_name("CATB")
        self.tracker.start_run(run_name=self.run_name)

        # Création du dossier d'artefacts
        root = get_repository_root()
        cfg = load_yaml_config(root / "configs/paths.yaml")

        self.output_models_dir = root / Path(cfg["paths"]["models_dir"])
        self.output_models_dir.mkdir(parents=True, exist_ok=True)

        self.output_reports_dir = root / Path(cfg["paths"]["reports_dir"])
        self.output_reports_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Training
    # ------------------------------------------------------------------
    def train(self, features: List[FeatureVector]) -> ModelArtifact:
        self.logger.info("Début de l'entraînement CatBoost")

        # =============================
        # Préparation des données
        # =============================
        df = pd.DataFrame([f.__dict__ for f in features])

        y = df[TARGET_COLUMN]
        X = df[FEATURES_ALL]

        self.logger.debug(f"Shape X={X.shape}, y={y.shape}")
        self.logger.info(f"Nombre de features : {X.shape[1]}")

        pool = Pool(
            data=X,
            label=y,
            cat_features=CATEGORICAL_FEATURES,
        )

        # =============================
        # Modèle
        # =============================
        model = CatBoostClassifier(**self.config)

        # =============================
        # Entraînement + Tracking MLflow
        # =============================
        with self.tracker:
            # 1. Paramètres
            self.tracker.log_params(self.config)

            # 2. Entraînement
            model.fit(
                pool,
                verbose=100,
                eval_set=pool,
                use_best_model=False,
            )

            # 3. Métriques par itération
            evals_result = model.get_evals_result()
            train_metrics = evals_result.get("learn", {})

            for metric_name, values in train_metrics.items():
                for step, value in enumerate(values):
                    self.tracker.log_metrics({metric_name: value})

            # 4. Courbes d'entraînement
            self._log_training_curves(train_metrics)

            # 5. Feature importances
            _ = self._log_feature_importances(model, X)

            # 6. Sauvegarde du modèle
            model_path = self.output_models_dir / f"{self.run_name.lower()}_model.cbm"
            model.save_model(model_path)

            self.logger.info(f"Modèle sauvegardé : {model_path}")
            self.tracker.log_artifact(str(model_path))

        self.logger.info("Entraînement CatBoost terminé")

        return ModelArtifact(
            model_path=str(model_path),
            numerical_features=NUMERICAL_FEATURES,
            categorical_features=CATEGORICAL_FEATURES,
            feature_names=list(X.columns),
        )

    # ------------------------------------------------------------------
    # Utils
    # ------------------------------------------------------------------
    def _log_training_curves(self, metrics: dict) -> None:
        """
        Génère et log les courbes d'entraînement dans MLflow.
        """
        for metric_name, values in metrics.items():
            plt.figure(figsize=(8, 5))
            plt.plot(values, label=f"train_{metric_name}")
            plt.xlabel("Iteration")
            plt.ylabel(metric_name)
            plt.title(f"Training Curve - {metric_name}")
            plt.legend()
            plt.grid(True)

            plot_path = self.output_reports_dir / f"{self.run_name.lower()}_training_curve_{metric_name}.png"
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            self.tracker.log_artifact(str(plot_path))

    def _log_feature_importances(
        self,
        model: CatBoostClassifier,
        X: pd.DataFrame,
        top_n: int = 20,
    ) -> pd.DataFrame:
        """
        Calcule, sauvegarde et log les feature importances CatBoost.
        """
        self.logger.info("Calcul des feature importances CatBoost")

        importances = model.get_feature_importance(
            type="PredictionValuesChange"
        )

        importance_df = pd.DataFrame(
            {
                "feature": X.columns,
                "importance": importances,
            }
        ).sort_values("importance", ascending=False)

        # CSV
        csv_path = self.output_reports_dir / f"{self.run_name.lower()}_feature_importances.csv"
        importance_df.to_csv(csv_path, index=False)
        self.tracker.log_artifact(str(csv_path))

        # Courbe TOP N
        top_features = importance_df.head(top_n)

        plt.figure(figsize=(10, 6))
        plt.barh(
            top_features["feature"][::-1],
            top_features["importance"][::-1],
        )
        plt.xlabel("Importance")
        plt.title(f"Top {top_n} Feature Importances (CatBoost)")
        plt.grid(True)

        plot_path = self.output_reports_dir / f"{self.run_name.lower()}_feature_importances.png"
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        self.tracker.log_artifact(str(plot_path))

        return importance_df
