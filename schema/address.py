from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class AddressBase(BaseModel):
    address: str
    longitude: float
    latitude: float

    class Config:
        from_attributes = True

class AddressCreateSchema(AddressBase):
    pass

class AddressViewSchema(AddressBase):
    id: int
    distance: Optional[float] = None

class AddressRequestSchema(BaseModel):
    distance: Optional[Decimal] = Field(default=None)
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class AddressUpdateSchema(BaseModel):
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
