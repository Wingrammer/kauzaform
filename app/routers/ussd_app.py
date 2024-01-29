# app/routers/ussd_app.py
import secrets
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.crud import ussd_app as ussd_ussd_app
from app.db.models.ussd_app import USSDApp, USSDAppCreate, USSDAppRead, USSDAppUpdate, USSDAppWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create app
@router.post("/apps/", response_model=USSDAppRead)
def create_app(app: USSDAppCreate, db: Session = Depends(get_db)):
    return ussd_ussd_app.create_ussd_ussd_app(db, app)

# Add other routes as needed

#Update app
@router.patch("/apps/{app_id}", response_model=USSDAppRead)
def update_app(app_id: int, app: USSDAppUpdate, db: Session = Depends(get_db)):
    return ussd_ussd_app.update_ussd_ussd_app(db, app_id, app)

#Fetch app
@router.get("/apps/{app_id}", response_model=USSDAppWithRels)
def get_app(app_id: int, db: Session = Depends(get_db)):
    return ussd_ussd_app.get_ussd_ussd_app(db, app_id)

#Fetch app by code
@router.get("/published-apps/{code}", response_model=USSDAppWithRels)
def get_app_by_code(code: str, secret: Optional[str] = None, db: Session = Depends(get_db)):
    app = ussd_ussd_app.get_ussd_ussd_app_by_code(db, code)

    if app is None or (secret is not None and not secrets.compare_digest(app.secret, secret)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="App not found or secret does not match",
        )

    return app

#Fetch all apps of a tenant
@router.get("/apps", response_model=List[USSDAppRead])
def get_apps(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_ussd_app.get_ussd_ussd_apps(db, tenant_id)

#Delete app
@router.delete("/apps/{app_id}")
def delete_app(app_id: int, db: Session = Depends(get_db)):
    return ussd_ussd_app.delete_ussd_ussd_app(db, app_id)