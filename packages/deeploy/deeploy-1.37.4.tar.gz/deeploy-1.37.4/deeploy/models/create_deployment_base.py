from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums import ExplainerType, ModelType, TransformerType


class CreateDeploymentBase(BaseModel):
    """Class that contains the base options for creating a Deployment"""

    name: str
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    repository_id: Optional[str] = None
    """str: uuid of the Repository"""
    branch_name: Optional[str] = None
    """str: the branch name of the Repository to deploy"""
    commit: Optional[str] = None
    """str: the commit sha on the selected branch"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""
    model_type: ModelType
    """int: enum value from ModelType class"""
    explainer_type: Optional[ExplainerType] = ExplainerType.NO_EXPLAINER
    """int, optional: enum value from ExplainerType class. Defaults to 0 (no explainer)"""
    transformer_type: Optional[TransformerType] = TransformerType.NO_TRANSFORMER
    """int, optional: enum value from TransformerType class. Defaults to 0 (no transformer)"""

    def to_request_body(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "contractPath": self.contract_path,
            "modelType": self.model_type.value,
            "explainerType": self.explainer_type.value,
            "transformerType": self.transformer_type.value,
        }


class CreateDeployment(BaseModel):
    """"""
