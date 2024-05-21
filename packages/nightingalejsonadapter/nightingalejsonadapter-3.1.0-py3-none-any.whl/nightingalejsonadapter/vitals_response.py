from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_serializer
from datetime import datetime


class VitalPredictions(BaseModel):
    HR: float
    RR: float
    SBP: float
    DBP: float
    SPO2: float


class VitalEarlyWarningScore(BaseModel):
    HR: int
    RR: int
    SBP: int
    DBP: int
    SPO2: int

class ProcedureMessage(BaseModel):
    procedureName: str
    predictedInterventionTimestamp: datetime
    message: str
    
    @field_serializer('predictedInterventionTimestamp')
    def timestamp_serializer(self, predictedInterventionTimestamp: datetime, _info):
        return predictedInterventionTimestamp.isoformat().replace('+00:00', '') + 'Z'


class Prediction(BaseModel):
    timestamp: datetime
    earlyWarningScore: int
    vitalPredictions: VitalPredictions
    vitalEarlyWarningScore: VitalEarlyWarningScore
    shockIndex: float
    
    @field_serializer('timestamp')
    def timestamp_serializer(self, timestamp: datetime, _info):
        return timestamp.isoformat().replace('+00:00', '') + 'Z'


class Model(BaseModel):
    UUID: str
    timestamp: datetime
    requestId: str
    globalincidentid: str
    lastMeasurementTimestamp: datetime
    predictionTimestampId: str
    predictionTimeDeltaMinutes: int
    victimId: str
    procedureMessageCount: int
    procedureMessages: List[ProcedureMessage]
    predictions: List[Prediction]
    
    @field_serializer('timestamp')
    def timestamp_serializer(self, timestamp: datetime, _info):
        return timestamp.isoformat().replace('+00:00', '') + 'Z'
    
    @field_serializer('lastMeasurementTimestamp')
    def timestamp_serializer(self, lastMeasurementTimestamp: datetime, _info):
        return lastMeasurementTimestamp.isoformat().replace('+00:00', '') + 'Z'