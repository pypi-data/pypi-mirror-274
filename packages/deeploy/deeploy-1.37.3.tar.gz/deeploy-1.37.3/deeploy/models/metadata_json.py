from typing import List, Optional

from pydantic import BaseModel


class MetadataJson(BaseModel):
    features: Optional[List[dict]]
    predictionClasses: Optional[dict]
    problemType: Optional[str]
    exampleInput: Optional[dict]
    exampleOutput: Optional[dict]
    inputTensorShape: Optional[str]
    outputTensorShape: Optional[str]
    customId: Optional[str]
