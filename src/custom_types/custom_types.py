"""
Defines all the types used within Datalyzer
"""

from typing import List
from pydantic import BaseModel

class AggregateWeights(BaseModel):
    """
    Defines the type of a model within an aggregate
    """

    model_name: str
    model_weight: float
    title_sentiment: float
    selftext_sentiment: float
    comments_sentiment: float

class AggregateData(BaseModel):
    """
    Defines the type of an Aggregate
    """
    aggregateName: str
    description: str
    weights: List[AggregateWeights]

class ResultsData(BaseModel):
    """
    Defines the type of a aggregated result
    """
    date: str
    average_score: float

class IndicatorData(BaseModel):
    """
    Defines in the type of an Indicator
    """
    indicatorName: str
    filters: List[str]
    aggregateName: str
    resultsByDay: List[ResultsData]
    resultsByMonth: List[ResultsData]
