import os
import mlflow
from mlflow.tracking import MlflowClient

from churn_gym.infrastructure.logging.loguru_logger import LoguruLogger
from churn_gym.infrastructure.utils.exceptions import (
    MLflowConfigurationError,
    MLflowSetupError,
)


class MLflowConfigurator:
    """
    Configure et initialise MLflow à partir des variables d’environnement.

    Responsabilité :
    - Valider la configuration MLflow
    - Initialiser la connexion au backend MLflow
    - Déclencher les migrations si nécessaire
    """

    def __init__(self):
        self.logger = LoguruLogger()

        self.tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
        self.artifact_uri = os.environ.get("MLFLOW_ARTIFACT_URI")

        self.logger.debug(f"MLFLOW_TRACKING_URI = {self.tracking_uri}")
        self.logger.debug(f"MLFLOW_ARTIFACT_URI = {self.artifact_uri}")

        if not self.tracking_uri:
            self.logger.error("MLFLOW_TRACKING_URI manquant")
            raise MLflowConfigurationError("MLFLOW_TRACKING_URI manquant.")

        if not self.artifact_uri:
            self.logger.error("MLFLOW_ARTIFACT_URI manquant")
            raise MLflowConfigurationError("MLFLOW_ARTIFACT_URI manquant.")

    def configure(self) -> tuple[MlflowClient, str]:
        """
        Initialise MLflow et retourne :
        - le client MLflow
        - l'artifact_location normalisée

        Raises
        ------
        MLflowSetupError
            Si MLflow ne peut pas être initialisé correctement.
        """
        try:
            self.logger.info("Initialisation de MLflow")
            mlflow.set_tracking_uri(self.tracking_uri)

            artifact_uri = self.artifact_uri
            if not artifact_uri.startswith(("file:", "http", "s3", "gs")):
                artifact_uri = f"file:{os.path.abspath(artifact_uri)}"

            self.logger.info(f"Artifact URI normalisée : {artifact_uri}")

            client = MlflowClient(tracking_uri=self.tracking_uri)

            # Test réel de connexion (déclenche migrations Alembic)
            self.logger.info("Test de connexion MLflow (search_experiments)")
            client.search_experiments()

            self.logger.info("MLflow configuré avec succès")
            return client, artifact_uri

        except Exception as exc:
            self.logger.error("Échec de l'initialisation MLflow")
            raise MLflowSetupError(
                "Impossible d'initialiser MLflow (backend ou migrations invalides)."
            ) from exc