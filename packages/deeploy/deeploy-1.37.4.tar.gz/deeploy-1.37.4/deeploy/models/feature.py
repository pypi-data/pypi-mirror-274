from typing import Optional

from pydantic import BaseModel


class Feature(BaseModel):
    name: str
    observed_min: Optional[float]
    observed_max: Optional[float]
