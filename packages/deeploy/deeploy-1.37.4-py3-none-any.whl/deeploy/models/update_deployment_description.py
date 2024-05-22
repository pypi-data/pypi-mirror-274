from typing import Dict, Optional

from pydantic import BaseModel


class UpdateDeploymentDescription(BaseModel):
    """Class that contains the options for updating a model that doesn't require restarting pods"""

    name: Optional[str] = None
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""

    def to_request_body(self) -> Dict:
        request_body = {
            "name": self.name,
            "description": self.description,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}
