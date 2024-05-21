from typing import Dict, Optional

from deeploy.models import CreateDeploymentBase


class CreateAzureMLDeployment(CreateDeploymentBase):
    """Class that contains the options for creating an Azure Machine Learning deployment"""

    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    model_instance_count: Optional[int] = None
    """int, optional: the amount of compute instances used for your model deployment"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the explainer"""
    explainer_instance_count: Optional[int] = None
    """int, optional: the amount of compute instances used for your explainer deployment"""

    def to_request_body(self) -> Dict:
        return {
            **super().to_request_body(),
            "modelInstanceType": self.model_instance_type,
            "modelInstanceCount": self.model_instance_count,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerInstanceCount": self.explainer_instance_count,
        }
