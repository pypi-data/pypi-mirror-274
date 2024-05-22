from typing import Optional

from pydantic import BaseModel


class DockerReference(BaseModel):
    image: str
    uri: str
    port: Optional[int]


class BlobReference(BaseModel):
    url: str
    region: Optional[str]


class MLFlowBlobReference(BaseModel):
    region: str


class MLFlowReference(BaseModel):
    model: str
    stage: Optional[str]
    version: Optional[str]
    blob: Optional[MLFlowBlobReference]


class AzureMLReference(BaseModel):
    image: str
    uri: str
    port: int
    readiness_path: str
    liveness_path: str
    model: Optional[str]
    version: Optional[str]


class ModelReference(BaseModel):
    docker: Optional[DockerReference]
    blob: Optional[BlobReference]
    mlflow: Optional[MLFlowReference]
    azureML: Optional[AzureMLReference]


class ExplainerReference(BaseModel):
    docker: Optional[DockerReference]
    blob: Optional[BlobReference]
    mlflow: Optional[MLFlowReference]
    azureML: Optional[AzureMLReference]


class TransformerReference(BaseModel):
    docker: Optional[DockerReference]
    blob: Optional[BlobReference]


class ModelReferenceJson(BaseModel):
    reference: ModelReference


class ExplainerReferenceJson(BaseModel):
    reference: ExplainerReference


class TransformerReferenceJson(BaseModel):
    reference: TransformerReference
