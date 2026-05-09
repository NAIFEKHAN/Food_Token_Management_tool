"""Pydantic request/response schemas."""
from typing import Optional
from pydantic import BaseModel, Field


class StudentLoginIn(BaseModel):
    roll_no: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class FoodSelectIn(BaseModel):
    food_type: str  # "Veg" | "Non-Veg"


class AdminLoginIn(BaseModel):
    username: str
    password: str


class VerifyTokenIn(BaseModel):
    token_id: str


class StudentOut(BaseModel):
    id: int
    name: str
    roll_no: str
    food_type: Optional[str] = None
    token_id: Optional[str] = None
    token_status: Optional[str] = None

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    name: str
    roll_no: str
    food_type: str
    token_id: str
    qr_code: str  # data URL
    event_name: str
