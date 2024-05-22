from typing import Dict, Optional

from deeploy.models import CreateDeploymentBase


class CreateDeployment(CreateDeploymentBase):
    """Class that contains the options for creating a deployment"""

    model_serverless: bool = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    model_blob_credentials_id: Optional[str] = None
    """str, optional: uuid of credentials generated in Deeploy to access private Blob storage"""
    model_docker_credentials_id: Optional[str] = None
    """str, optional: uuid of credentials generated in Deeploy to access private Docker repo"""
    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    model_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    model_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    model_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in number of cores."""
    model_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in number of cores."""
    model_gpu_request: Optional[float] = None
    """float, optional: GPU request of model pod, in number of GPUs."""
    model_env: Optional[dict] = None
    """dict, optional: env variables to pass to model container key is env var name, value is env var value"""
    model_args: Optional[dict] = None
    """dict, optional: arguments to pass to model container key is argument name, value is argument value"""
    explainer_serverless: bool = False
    """bool, optional: whether to deploy the explainer in a serverless fashion. Defaults to False"""
    explainer_blob_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Blob storage"""
    explainer_docker_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Docker repo"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the explainer pod."""
    explainer_mem_request: Optional[int] = None
    """int, optional: RAM request of explainer pod, in Megabytes."""
    explainer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of explainer pod, in Megabytes."""
    explainer_cpu_request: Optional[float] = None
    """float, optional: CPU request of explainer pod, in number of cores."""
    explainer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of explainer pod, in number of cores."""
    explainer_gpu_request: Optional[float] = None
    """float, optional: GPU request of explainer pod, in number of GPUs."""
    explainer_env: Optional[dict] = None
    """dict, optional: env variables to pass to explainer container key is env var name, value is env var value"""
    explainer_args: Optional[dict] = None
    """dict, optional: arguments to pass to explainer container key is argument name, value is argument value"""
    transformer_serverless: bool = False
    """bool, optional: whether to deploy the transformer in a serverless fashion. Defaults to False"""
    transformer_docker_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Docker repo"""
    transformer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the transformer pod."""
    transformer_mem_request: Optional[int] = None
    """int, optional: RAM request of transformer pod, in Megabytes."""
    transformer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of transformer pod, in Megabytes."""
    transformer_cpu_request: Optional[float] = None
    """float, optional: CPU request of transformer pod, in number of cores."""
    transformer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of transformer pod, in number of cores."""
    transformer_gpu_request: Optional[float] = None
    """float, optional: GPU request of transformer pod, in number of GPUs."""
    transformer_env: Optional[dict] = None
    """dict, optional: env variables to pass to transformer container key is env var name, value is env var value"""
    transformer_args: Optional[dict] = None
    """dict, optional: arguments to pass to transformer container key is argument name, value is argument value"""

    def to_request_body(self) -> Dict:
        return {
            **super().to_request_body(),
            "modelServerless": self.model_serverless,
            "modelBlobCredentialsId": self.model_blob_credentials_id,
            "modelDockerCredentialsId": self.model_docker_credentials_id,
            "modelInstanceType": self.model_instance_type,
            "modelMemRequest": self.model_mem_request,
            "modelMemLimit": self.model_mem_limit,
            "modelCpuRequest": self.model_cpu_request,
            "modelCpuLimit": self.model_cpu_limit,
            "modelGpuRequest": self.model_gpu_request,
            "modelEnv": self.model_env,
            "modelArgs": self.model_args,
            "explainerServerless": self.explainer_serverless,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerBlobCredentialsId": self.explainer_blob_credentials_id,
            "explainerDockerCredentialsId": self.explainer_docker_credentials_id,
            "explainerMemRequest": self.explainer_mem_request,
            "explainerMemLimit": self.explainer_mem_limit,
            "explainerCpuRequest": self.explainer_cpu_request,
            "explainerCpuLimit": self.explainer_cpu_limit,
            "explainerGpuRequest": self.explainer_gpu_request,
            "explainerEnv": self.explainer_env,
            "explainerArgs": self.explainer_args,
            "transformerServerless": self.transformer_serverless,
            "transformerBlobCredentialsId": None,
            "transformerDockerCredentialsId": self.transformer_docker_credentials_id,
            "transformerInstanceType": self.transformer_instance_type,
            "transformerMemRequest": self.transformer_mem_request,
            "transformerMemLimit": self.transformer_mem_limit,
            "transformerCpuRequest": self.transformer_cpu_request,
            "transformerCpuLimit": self.transformer_cpu_limit,
            "transformerGpuRequest": self.transformer_gpu_request,
            "transformerEnv": self.transformer_env,
            "transformerArgs": self.transformer_args,
        }
