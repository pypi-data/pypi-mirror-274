import base64
from typing import List

import requests
from pydantic import parse_obj_as

from deeploy.enums import AuthType, PredictionVersion
from deeploy.models import (
    ActualResponse,
    CreateActuals,
    CreateAzureMLDeployment,
    CreateDeployment,
    CreateEvaluation,
    CreateSageMakerDeployment,
    Deployment,
    Evaluation,
    GetPredictionLogsOptions,
    PredictionLog,
    Repository,
    UpdateAzureMLDeployment,
    UpdateDeployment,
    UpdateDeploymentDescription,
    UpdateSageMakerDeployment,
    V1Prediction,
    V2Prediction,
    Workspace,
)
from deeploy.models.prediction_log import RequestLog


class DeeployService(object):
    """
    A class for interacting with the Deeploy API
    """

    request_timeout = 300

    def __init__(
        self,
        host: str,
        access_key: str = None,
        secret_key: str = None,
        token: str = None,
        insecure: bool = False,
    ) -> None:
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__token = token
        self.__host = f"http://api.{host}" if insecure else f"https://api.{host}"

        if not (access_key and secret_key) and not token:
            raise Exception(
                "No authentication method provided. Please provide a token or personal key pair"
            )

    def get_repositories(self, workspace_id: str) -> List[Repository]:
        url = "%s/workspaces/%s/repositories" % (self.__host, workspace_id)

        repositories_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        repositories = parse_obj_as(List[Repository], repositories_response.json())

        return repositories

    def get_repository(self, workspace_id: str, repository_id: str) -> Repository:
        url = "%s/workspaces/%s/repositories/%s" % (
            self.__host,
            workspace_id,
            repository_id,
        )

        repository_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(repository_response):
            raise Exception("Repository does not exist in the workspace.")

        repository = parse_obj_as(Repository, repository_response.json())

        return repository

    def get_deployment(
        self, workspace_id: str, deployment_id: str, withExamples: bool = False
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "withExamples": withExamples,
        }
        deployment_response = requests.get(
            url,
            params=params,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception(
                "Failed to retrieve the deployment: %s" % str(deployment_response.json())
            )

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def create_deployment(self, workspace_id: str, deployment: CreateDeployment) -> Deployment:
        url = "%s/workspaces/%s/deployments" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def create_sagemaker_deployment(
        self, workspace_id: str, deployment: CreateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/sagemaker" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def create_azure_ml_deployment(
        self, workspace_id: str, deployment: CreateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/azure-ml" % (self.__host, workspace_id)
        data = deployment.to_request_body()

        deployment_response = requests.post(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to create the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def update_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def update_sagemaker_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateSageMakerDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/sagemaker/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def update_azure_ml_deployment(
        self, workspace_id: str, deployment_id: str, update: UpdateAzureMLDeployment
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/azure-ml/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()

        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the Deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json())

        return deployment

    def update_deployment_description(
        self, workspace_id: str, deployment_id: str, update: UpdateDeploymentDescription
    ) -> Deployment:
        url = "%s/workspaces/%s/deployments/%s/description" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        data = update.to_request_body()
        deployment_response = requests.patch(
            url,
            json=data,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(deployment_response):
            raise Exception("Failed to update the deployment: %s" % str(deployment_response.json()))

        deployment = parse_obj_as(Deployment, deployment_response.json()["data"])

        return deployment

    def get_workspace(self, workspace_id: str) -> Workspace:
        url = "%s/workspaces/%s" % (self.__host, workspace_id)

        workspace_response = requests.get(
            url,
            auth=(self.__access_key, self.__secret_key),
            timeout=self.request_timeout,
        )
        if not self.__request_is_successful(workspace_response):
            raise Exception("Workspace does not exist.")

        workspace = parse_obj_as(Workspace, workspace_response.json())

        return workspace

    def predict(
        self, workspace_id: str, deployment_id: str, request_body: dict
    ) -> V1Prediction or V2Prediction:
        url = "%s/workspaces/%s/deployments/%s/predict" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        prediction_response = requests.post(
            url,
            json=request_body,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(prediction_response):
            raise Exception(f"Failed to call predictive model: {prediction_response.json()}")

        prediction = self.__parse_prediction(prediction_response)
        return prediction

    def explain(
        self,
        workspace_id: str,
        deployment_id: str,
        request_body: dict,
        image: bool = False,
    ) -> object:
        url = "%s/workspaces/%s/deployments/%s/explain" % (
            self.__host,
            workspace_id,
            deployment_id,
        )
        params = {
            "image": str(image).lower(),
        }

        explanation_response = requests.post(
            url,
            json=request_body,
            params=params,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(explanation_response):
            raise Exception(f"Failed to call explainer model: {explanation_response.json()}")

        explanation = explanation_response.json()
        return explanation

    def get_one_prediction_log(
        self,
        workspace_id: str,
        deployment_id: str,
        request_log_id: str,
        prediction_log_id: str,
    ) -> PredictionLog:
        url = "%s/workspaces/%s/deployments/%s/requestLogs/%s/predictionLogs/%s" % (
            self.__host,
            workspace_id,
            deployment_id,
            request_log_id,
            prediction_log_id,
        )

        log_response = requests.get(
            url,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(log_response):
            raise Exception("Failed to get log %s." % prediction_log_id)

        log = parse_obj_as(PredictionLog, log_response.json())
        return log

    def get_prediction_logs(
        self, workspace_id: str, deployment_id: str, params: GetPredictionLogsOptions
    ) -> List[PredictionLog]:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        logs_response = requests.get(
            url,
            params=params.to_params(),
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = parse_obj_as(List[PredictionLog], logs_response.json())
        return logs

    def get_request_logs(self, workspace_id: str, deployment_id: str) -> List[RequestLog]:
        url = "%s/workspaces/%s/deployments/%s/requestLogs" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        logs_response = requests.get(
            url,
            headers=self.__get_headers(AuthType.ALL),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(logs_response):
            raise Exception("Failed to get logs.")

        logs = parse_obj_as(List[RequestLog], logs_response.json())
        return logs

    def evaluate(
        self,
        workspace_id: str,
        deployment_id: str,
        prediction_log_id: str,
        evaluation_input: CreateEvaluation,
    ) -> Evaluation:
        url = "%s/workspaces/%s/deployments/%s/predictionLogs/%s/evaluatePrediction" % (
            self.__host,
            workspace_id,
            deployment_id,
            prediction_log_id,
        )

        if evaluation_input.agree is True and ("desired_output" in evaluation_input):
            raise Exception(
                "A desired_output can not be provided when agreeing with the inference."
            )

        data = evaluation_input.to_request_body()
        evaluation_response = requests.post(
            url,
            json=data,
            headers=self.__get_headers(AuthType.TOKEN),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(evaluation_response):
            if evaluation_response.status_code == 409:
                raise Exception("Log has already been evaluated.")
            elif evaluation_response.status_code == 401:
                raise Exception("No permission to perform this action.")
            else:
                raise Exception("Failed to request evaluation.")

        evaluation = parse_obj_as(Evaluation, evaluation_response.json())
        return evaluation

    def actuals(
        self, workspace_id: str, deployment_id: str, actuals_input: CreateActuals
    ) -> List[ActualResponse]:
        url = "%s/workspaces/%s/deployments/%s/actuals" % (
            self.__host,
            workspace_id,
            deployment_id,
        )

        data = actuals_input.to_request_body()
        actuals_response = requests.put(
            url,
            json=data,
            headers=self.__get_headers(AuthType.TOKEN),
            timeout=self.request_timeout,
        )

        if not self.__request_is_successful(actuals_response):
            if actuals_response.status_code == 401:
                raise Exception("No permission to perform this action.")
            else:
                raise Exception("Failed to submit actuals.")

        actuals = parse_obj_as(List[ActualResponse], actuals_response.json())
        return actuals

    def __request_is_successful(self, request: requests.Response) -> bool:
        if str(request.status_code)[0] == "2":
            return True
        return False

    def __check_prediction_version(self, prediction_response: dict) -> PredictionVersion:
        if len(prediction_response.json()) > 1:
            return PredictionVersion.V2
        else:
            return PredictionVersion.V1

    def __parse_prediction(self, prediction_response: dict) -> V1Prediction or V2Prediction:
        if self.__check_prediction_version(prediction_response) == PredictionVersion.V1:
            prediction = parse_obj_as(V1Prediction, prediction_response.json())
        else:
            prediction = parse_obj_as(V2Prediction, prediction_response.json())
        return prediction

    def __get_headers(self, supported_auth: AuthType):
        headers = {}
        if (self.__access_key and self.__secret_key) and (
            supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
        ):
            credentials = self.__access_key + ":" + self.__secret_key
            b64Val = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = "Basic %s" % b64Val
        elif (self.__token) and (
            supported_auth == AuthType.TOKEN or supported_auth == AuthType.ALL
        ):
            headers["Authorization"] = "Bearer " + self.__token
        elif (self.__access_key and self.__secret_key) and not (
            supported_auth == AuthType.BASIC or supported_auth == AuthType.ALL
        ):
            raise Exception("This function currently does not support Basic authentication.")
        else:
            raise Exception("This function currently does not support Token authentication.")

        return headers
