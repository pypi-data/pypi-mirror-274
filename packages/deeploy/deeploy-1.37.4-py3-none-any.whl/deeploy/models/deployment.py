from typing import Dict, Optional, Union

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class Deployment(BaseModel):
    id: str
    team_id: str
    name: str
    workspace_id: str
    owner_id: str
    public_url: Optional[str]
    description: Optional[str]
    active_version: Optional[Union[Dict, str]]
    updating_to: Optional[Union[Dict, str]]
    last_version: Optional[Union[Dict, str]]
    status: int
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
