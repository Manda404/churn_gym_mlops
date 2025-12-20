from __future__ import annotations

from typing import Any, Mapping

import mlflow

from churn_gym.domain.interfaces.experiment_tracker import ExperimentTracker
from churn_gym.infrastructure.tracking.mlflow_setup import MLflowConfigurator
from churn_gym.infrastructure.logging.loguru_logger import LoguruLogger
from churn_gym.infrastructure.utils.exceptions import MLflowSetupError


class MLflowExperimentTracker(ExperimentTracker):
    """
    Implémentation MLflow du port ExperimentTracker.

    Responsabilités :
    - Gestion des expériences MLflow
    - Gestion sûre du cycle de vie des runs
    - Logging des paramètres, métriques et artefacts

    Toute dépendance à MLflow est confinée à l'infrastructure.
    """

    def __init__(self, configurator: MLflowConfigurator):
        self.logger = LoguruLogger()
        self.client, self.artifact_location = configurator.configure()

    # ------------------------------------------------------------------
    # Experiment management
    # ------------------------------------------------------------------
    def setup_experiment(self, name: str) -> str:
        """
        Crée ou récupère une expérience MLflow et la définit comme active.
        """
        existing = self.client.get_experiment_by_name(name)

        if existing:
            exp_id = existing.experiment_id
            self.logger.info(f"Expérience existante : {name}")
        else:
            exp_id = self.client.create_experiment(
                name=name,
                artifact_location=self.artifact_location,
            )
            self.logger.info(
                f"Expérience créée : {name} "
                f"(artifact_location={self.artifact_location})"
            )

        mlflow.set_experiment(experiment_id=exp_id)
        return exp_id

    # ------------------------------------------------------------------
    # Run lifecycle
    # ------------------------------------------------------------------
    def start_run(self, run_name: str | None = None, nested: bool = False) -> None:
        """
        Démarre un run MLflow de manière sûre.

        - Ferme automatiquement un run actif existant (si nested=False)
        - Supporte les runs imbriqués si nested=True
        """
        try:
            active_run = mlflow.active_run()

            if active_run:
                if nested:
                    self.logger.info(
                        f"Run actif détecté ({active_run.info.run_id}) → nested=True"
                    )
                else:
                    self.logger.warning(
                        f"Run actif détecté ({active_run.info.run_id}) → fermeture automatique"
                    )
                    mlflow.end_run()

            self.logger.info(f"Démarrage du run MLflow : {run_name}")
            mlflow.start_run(run_name=run_name, nested=nested)

        except Exception as exc:
            self.logger.error("Impossible de démarrer le run MLflow")
            raise MLflowSetupError(
                "Erreur lors du démarrage du run MLflow."
            ) from exc

    def end_run(self) -> None:
        """
        Termine proprement le run MLflow actif (si existant).
        """
        active_run = mlflow.active_run()

        if active_run:
            self.logger.info(
                f"Fermeture du run MLflow : {active_run.info.run_id}"
            )
            mlflow.end_run()

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    def log_params(self, params: Mapping[str, Any]) -> None:
        mlflow.log_params(params)

    def log_metrics(self, metrics: Mapping[str, float]) -> None:
        mlflow.log_metrics(metrics)

    def log_artifact(self, path: str) -> None:
        mlflow.log_artifact(path)

    def __enter__(self) -> "MLflowExperimentTracker":
        """
        Entrée dans le contexte MLflow.
        Le run doit déjà être démarré.
        """
        self.logger.debug("Entrée dans le contexte MLflowExperimentTracker")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Sortie du contexte :
        - ferme toujours le run MLflow
        """
        if exc_type:
            self.logger.error(
                f"Exception dans le contexte MLflow : {exc_type.__name__}"
            )

        self.end_run()