# app/routers/ussd_state.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.crud import state as ussd_state
from app.db.models.state import USSDStateCreate, USSDStateRead, USSDStateUpdate, USSDStateWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create state
@router.post("/states/", response_model=USSDStateRead)
def create_state(state: USSDStateCreate, db: Session = Depends(get_db)):
    return ussd_state.create_ussd_state(db, state)

# Add other routes as needed

#Update state
@router.patch("/states/{state_id}", response_model=USSDStateRead)
def update_state(state_id: int, state: USSDStateUpdate, db: Session = Depends(get_db)):
    return ussd_state.update_ussd_state(db, state_id, state)

#Fetch state
@router.get("/states/{state_id}", response_model=List[USSDStateWithRels])
def get_state(state_id: int, db: Session = Depends(get_db)):
    return ussd_state.get_ussd_state(db, state_id)

#Fetch all states of a tenant
@router.get("/states", response_model=List[USSDStateRead])
def get_states(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_state.get_ussd_states(db, tenant_id)

#Delete state
@router.delete("/states/{state_id}")
def delete_state(state_id: int, db: Session = Depends(get_db)):
    return ussd_state.delete_ussd_state(db, state_id)