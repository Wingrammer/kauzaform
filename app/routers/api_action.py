# app/routers/ussd_api_action.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.crud import api_action as ussd_api_action
from app.db.models.api_action import USSDAPIAction, USSDAPIActionCreate, USSDAPIActionRead, USSDAPIActionUpdate, USSDAPIActionWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create api_action
@router.post("/api_actions/", response_model=USSDAPIActionRead)
def create_api_action(api_action: USSDAPIActionCreate, db: Session = Depends(get_db)):
    return ussd_api_action.create_ussd_api_action(db, api_action)

# Add other routes as needed

#Update api_action
@router.patch("/api_actions/{api_action_id}", response_model=USSDAPIActionRead)
def update_api_action(api_action_id: int, api_action: USSDAPIActionUpdate, db: Session = Depends(get_db)):
    return ussd_api_action.update_ussd_api_action(db, api_action_id, api_action)

#Fetch api_action
@router.get("/api_actions/{api_action_id}", response_model=USSDAPIActionWithRels)
def get_api_action(api_action_id: int, db: Session = Depends(get_db)):
    return ussd_api_action.get_ussd_api_action(db, api_action_id)

#Fetch all api_actions of a tenant
@router.get("/api_actions", response_model=List[USSDAPIActionRead])
def get_api_actions(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_api_action.get_ussd_api_actions(db, tenant_id)

#Delete api_action
@router.delete("/api_actions/{api_action_id}")
def delete_api_action(api_action_id: int, db: Session = Depends(get_db)):
    return ussd_api_action.delete_ussd_api_action(db, api_action_id)