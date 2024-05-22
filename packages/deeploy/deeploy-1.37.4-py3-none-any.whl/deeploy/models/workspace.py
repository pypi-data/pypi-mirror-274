from typing import Optional

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class Workspace(BaseModel):
    id: str
    team_id: str
    name: str
    description: Optional[str]
    owner_id: str
    slack_webhook_url: Optional[str]
    default_deployment_backend: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
