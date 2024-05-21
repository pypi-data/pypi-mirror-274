from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class RequestLog(BaseModel):
    id: str
    team_id: str
    deployment_id: str
    commit: str
    request_content_type: str
    response_time_m_s: int
    status_code: int
    personal_keys_id: Optional[str]
    token_id: Optional[str]
    created_at: str
    prediction_logs: Optional[Dict]

    class Config:
        alias_generator = to_lower_camel


class PredictionLog(BaseModel):
    id: str
    team_id: str
    request_body: Optional[Dict]
    response_body: Optional[Dict]
    request_log: Dict
    evaluation: Optional[Dict]
    actual: Optional[Dict]
    created_at: str
    tags: Dict

    class Config:
        alias_generator = to_lower_camel
