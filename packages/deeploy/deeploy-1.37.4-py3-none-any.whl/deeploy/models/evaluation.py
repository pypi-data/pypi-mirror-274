from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class Evaluation(BaseModel):
    id: str
    team_id: str
    agree: bool
    desired_output: Optional[Dict]
    comment: Optional[str]
    personal_keys_id: Optional[str]
    token_id: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
