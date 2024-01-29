# app/routers/ussd_option.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.crud import option as ussd_option
from app.db.models.option import USSDOption, USSDOptionCreate, USSDOptionRead, USSDOptionUpdate, USSDOptionWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create option
@router.post("/options/", response_model=USSDOptionRead)
def create_option(option: USSDOptionCreate, db: Session = Depends(get_db)):
    return ussd_option.create_ussd_option(db, option)

# Add other routes as needed

#Update option
@router.patch("/options/{option_id}", response_model=USSDOptionRead)
def update_option(option_id: int, option: USSDOptionUpdate, db: Session = Depends(get_db)):
    return ussd_option.update_ussd_option(db, option_id, option)

#Fetch option
@router.get("/options/{option_id}", response_model=USSDOptionWithRels)
def get_option(option_id: int, db: Session = Depends(get_db)):
    return ussd_option.get_ussd_option(db, option_id)

#Fetch all options of a tenant
@router.get("/options", response_model=List[USSDOptionRead])
def get_options(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_option.get_ussd_options(db, tenant_id)

#Delete option
@router.delete("/options/{option_id}")
def delete_option(option_id: int, db: Session = Depends(get_db)):
    return ussd_option.delete_ussd_option(db, option_id)




