from datetime import date
from pydantic import RootModel
from typing import List, Literal
from pydantic import BaseModel, ValidationInfo, field_validator

class DiseaseReport(BaseModel):
    disease_name: Literal["measles", "pertussis", "meningococcus"]
    report_period_start: date
    report_period_end: date
    date_type: Literal["cccd", "jurisdiction date hierarchy"]
    time_unit: Literal["week", "month"]
    disease_subtype: str
    reporting_jurisdiction: str
    state: Literal[
        "AL", "AK", "AZ", "AR", "AS",
        "CA", "CO", "CT", "DE", "DC",
        "FL", "GA", "GU", "HI", "ID",
        "IL", "IN", "IA", "KS", "KY",
        "LA", "ME", "MD", "MA", "MI",
        "MN", "MS", "MO", "MT", "NE",
        "NV", "NH", "NJ", "NM", "NY",
        "NC", "ND", "MP", "OH", "OK",
        "OR", "PA", "PR", "RI", "SC",
        "SD", "TN", "TX", "TT", "UT",
        "VT", "VA", "VI", "WA", "WV",
        "WI", "WY"
    ]
    geo_name: str
    geo_unit: Literal["county", "state", "region", "planning area", "hsa", "NA"]
    age_group: Literal[
        "<1 y", "1-4 y", "5-11 y", "12-18 y",
        "19-22 y", "23-44 y", "45-64 y", ">=65 y",
        "total", "unknown", "unspecified"
    ]
    confirmation_status: Literal["confirmed", "confirmed and probable"]
    outcome: Literal["cases", "hospitalizations", "deaths"]
    count: int
    
    class Config:
        """
        forbid extra data columns
        """
        extra = "forbid"
    
    @field_validator('count')
    @classmethod
    def count_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('count must be >= 0')
        return v
    
    @field_validator('disease_subtype')
    @classmethod
    def validate_disease_subtype(cls, v, info: ValidationInfo):
        """
        validate disease_subtype based on disease_name
        """
        disease_name = info.data.get('disease_name')
        
        if disease_name == "meningococcus":
            if v not in ["A", "B", "C", "W", "X", "Y", "Z", "unknown", "unspecified"]:
                raise ValueError(
                    f"for meningococcus, disease_subtype must be one of: A, B, C, W, X, Y, Z, unknown, unspecified. got: {v}"
                )
        elif disease_name in ["measles", "pertussis"]:
            if v not in ["NA", "unknown"]:
                raise ValueError(
                    f"for {disease_name}, disease_subtype must be 'NA' or 'unknown'. got: {v}"
                )
        
        return v
    
    @field_validator('time_unit')
    @classmethod
    def validate_time_unit(cls, v, info: ValidationInfo):
        """
        validate time_unit based on disease_name
        """
        disease_name = info.data.get('disease_name')
        
        if disease_name == "measles" and v not in ["week", "month"]:
            raise ValueError("measles must have time_unit of 'week' or 'month'")
        if disease_name == "pertussis" and v != "month":
            raise ValueError("pertussis must have time_unit of 'month'")
        if disease_name == "meningococcus" and v != "month":
            raise ValueError("meningococcus must have time_unit of 'month'")
        
        return v

class DiseaseReportDataset(RootModel[List[DiseaseReport]]):
    pass