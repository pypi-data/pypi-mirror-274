from typing import Dict, Optional

from deeploy.models import CreateDeploymentBase


class CreateSageMakerDeployment(CreateDeploymentBase):
    """Class that contains the options for creating a SageMaker deployment"""

    region: Optional[str] = None
    """str, optional: the AWS region used for this Deployment"""
    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the explainer"""
    transformer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the explainer"""

    def to_request_body(self) -> Dict:
        return {
            **super().to_request_body(),
            "region": self.region,
            "modelInstanceType": self.model_instance_type,
            "explainerInstanceType": self.explainer_instance_type,
            "transformerInstanceType": self.transformer_instance_type,
        }
