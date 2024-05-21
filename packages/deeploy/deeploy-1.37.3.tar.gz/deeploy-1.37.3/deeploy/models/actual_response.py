from pydantic import BaseModel

from deeploy.common.functions import to_lower_camel


class ActualResponse(BaseModel):
    prediction_log_id: str
    status: int
    message: str

    class Config:
        alias_generator = to_lower_camel
