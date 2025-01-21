import os
import grpc
import da_dv_pb2
import da_dv_pb2_grpc

from typing import List
from fastapi import FastAPI, HTTPException, Query
from datavisualisation import DataVisualisationAPI
from custom_types import AggregateData, IndicatorData

app = FastAPI()

dvapi = DataVisualisationAPI()

grpc_server_address = os.getenv("GRPC_SERVER_ADDRESS", "localhost:50051")
print(grpc_server_address)

@app.get("/getmodeldescription", response_model=str)
def get_model_description(name: str):
    models = dvapi.get_models()
    for model in models:
        if model["model_name"] == name:
            return model["description"]
    raise HTTPException(status_code=500, detail="Model with such name does not exist")

@app.get("/getallaggregates", response_model=List[AggregateData])
def get_aggregates():
    aggregates = dvapi.get_aggregates()
    return aggregates

@app.get("/getaggregate", response_model=AggregateData)
def get_aggregate(name: str):
    aggregates = dvapi.get_aggregates()
    for aggregate in aggregates:
        if aggregate["aggregateName"] == name:
            return aggregate
    raise HTTPException(status_code=500, detail="Aggregate with such name does not exist")

@app.put("/updateaggregate", response_model=AggregateData)
def update_aggregate(updated_data: dict):
    dvapi.upsert_aggregate(updated_data)

    with grpc.insecure_channel(grpc_server_address) as channel:
        stub = da_dv_pb2_grpc.RecalculateAggregateStub(channel)
        request = da_dv_pb2.RecalculateRequest(object_name=updated_data['aggregateName'])
        response = stub.RecalculateAggregate(request)
        print(response.result)

    return updated_data

@app.put("/createaggregate", response_model=str)
def create_aggregate(name: str):
    models = dvapi.get_models_list()
    weights = []
    for model in models:
        weights.append({
            "model_name": model,
            "model_weight": 0,
            "title_sentiment": 0,
            "selftext_sentiment": 0,
            "comments_sentiment": 0
        })
    new_aggregate = {
        'aggregateName': name,
        'description': "",
        'weights': weights
    }
    dvapi.upsert_aggregate(new_aggregate)
    return name

@app.put("/deleteaggregate", response_model=str)
def delete_aggregate(name: str):
    indicators = dvapi.get_indicators()
    for indicator in indicators:
        if indicator['aggregateName'] == name:
            raise HTTPException(status_code=500, detail="At least one indicator is still using this aggregate")

    dvapi.delete_aggregate(name)
    return name

@app.get("/getallindicators", response_model=List[IndicatorData])
def get_indicators():
    indicators = dvapi.get_indicators()
    return indicators

@app.get("/getindicator", response_model=IndicatorData)
def get_indicator(name: str):
    indicators = dvapi.get_indicators()
    for indicator in indicators:
        if indicator['indicatorName'] == name:
            return indicator
    raise HTTPException(status_code=500, detail="Indicator with such name does not exist")

@app.get("/getindicators", response_model=List[IndicatorData])
def get_some_indicators(name: List[str]=Query(...)):
    indicators = dvapi.get_indicators()
    matched_indicators = [indicator for indicator in indicators if indicator["indicatorName"] in name]

    if not matched_indicators:
        raise HTTPException(status_code=500, detail="No indicators found with the specified indicator list")

    return matched_indicators


@app.put("/createindicator", response_model=str)
def create_indicator(indicator_data: dict):
    dvapi.upsert_indicator(indicator_data)

    with grpc.insecure_channel(grpc_server_address) as channel:
        stub = da_dv_pb2_grpc.RecalculateIndicatorStub(channel)
        request = da_dv_pb2.RecalculateRequest(object_name=indicator_data['indicatorName'])
        response = stub.RecalculateIndicator(request)
        print(response.result)

    return indicator_data['indicatorName']

@app.put("/deleteindicator", response_model=str)
def delete_indicator(name: str):
    dvapi.delete_indicator(name)
    return name
