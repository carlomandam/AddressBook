from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from schema.address import AddressCreateSchema, AddressViewSchema, AddressRequestSchema, AddressUpdateSchema
from models.address import Address
from database import SessionLocal
from typing import Optional
from math import radians, sin, cos, sqrt, atan2
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of earth in kilometers
    return c * r


def get_db():
    db = SessionLocal()
    db.connection().connection.create_function('haversine', 4, haversine) # Register the haversine function
    try:
        yield db
    finally:
        db.close()


@app.get("/addresses/")
async def get_addresses(request: AddressRequestSchema = Depends(), db: Session = Depends(get_db)):
    try:        
        # Use haversine function in the query if parameters are present
        if request.longitude is not None and request.latitude is not None and request.distance is not None:
            query = db.query(Address, func.haversine(Address.longitude, Address.latitude, request.longitude, request.latitude).label('distance')).filter(
                func.haversine(Address.longitude, Address.latitude, request.longitude, request.latitude) <= request.distance
            )
            addresses = query.all()   
            address_response = []

            for row, distance in addresses:
                address_response.append(AddressViewSchema(
                    id=row.id,
                    address=row.address,
                    longitude=row.longitude,
                    latitude=row.latitude,
                    distance=distance
                ))
        # Return all address if parameters are not present or incomplete
        else:
            address_response = db.query(Address).all()
        
        return address_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/address/")
async def create_address(address: AddressCreateSchema, db: Session = Depends(get_db)):
    try:
        new_address = Address(address=address.address,
                                longitude=address.longitude,
                                latitude=address.latitude)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create address: {str(e)}")
    finally:
        db.close()

    return new_address


@app.patch("/addresses/{address_id}")
async def update_address(address_id: int, address_data: AddressUpdateSchema,  db: Session = Depends(get_db)):
    try:
        # Retrieve the address from the database
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        # Update the address fields with the new data
        for field in address_data.model_dump():
            new_value =  getattr(address_data, field)
            if new_value is not None: 
                setattr(address, field, new_value)

        db.commit()

        return {"message": "Address updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.delete("/addresses/{address_id}")
async def delete_address(address_id: int,  db: Session = Depends(get_db)):
    try:
        # Retrieve the address from the database
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        # Delete the address
        db.delete(address)
        db.commit()

        return {"message": "Address deleted successfully"}
    except Exception as e:
        # Rollback the transaction in case of error
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()