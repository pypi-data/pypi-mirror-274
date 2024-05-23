from typing import List, Optional

from mlflow.pydantic_v1 import BaseModel


# Metric associated with a run, represented as a key-value pair.
class MetricDto(BaseModel):
    key: str
    value: Optional[float]
    timestamp: Optional[int]
    step: Optional[int] = 0


class GetMetricHistoryResponse(BaseModel):
    metrics: List[MetricDto]


class MetricCollectionDto(BaseModel):
    key: Optional[str]
    metrics: Optional[List[MetricDto]]


class ListMetricHistoryRequestDto(BaseModel):
    run_id: str
    metric_keys: Optional[List[str]]


class ListMetricHistoryResponseDto(BaseModel):
    metric_collections: List[MetricCollectionDto]
