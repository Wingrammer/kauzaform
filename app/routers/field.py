# app/routers/ussd_field.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.crud import field as ussd_field
from app.db.models.field import USSDField, USSDFieldCreate, USSDFieldRead, USSDFieldUpdate, USSDFieldWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create field
@router.post("/fields/", response_model=USSDFieldRead)
def create_field(field: USSDFieldCreate, db: Session = Depends(get_db)):
    return ussd_field.create_ussd_field(db, field)

# Add other routes as needed

#Update field
@router.patch("/fields/{field_id}", response_model=USSDFieldRead)
def update_field(field_id: int, field: USSDFieldUpdate, db: Session = Depends(get_db)):
    return ussd_field.update_ussd_field(db, field_id, field)

#Fetch field
@router.get("/fields/{field_id}", response_model=USSDFieldWithRels)
def get_field(field_id: int, db: Session = Depends(get_db)):
    return ussd_field.get_ussd_field(db, field_id)

#Fetch all fields of a tenant
@router.get("/fields", response_model=List[USSDFieldRead])
def get_fields(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_field.get_ussd_fields(db, tenant_id)

#Delete field
@router.delete("/fields/{field_id}")
def delete_field(field_id: int, db: Session = Depends(get_db)):
    return ussd_field.delete_ussd_field(db, field_id)