# app/routers/ussd_app.py
import secrets
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.crud import ussd_app as ussd_ussd_app
from app.db.models.ussd_app import USSDApp, USSDAppCreate, USSDAppRead, USSDAppUpdate, USSDAppWithRels
from app.db.engine import get_db
# from hashlib import sha256
# from base64 import urlsafe_b64encode, urlsafe_b64decode

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
@router.get("/published-apps/{public_id}", response_model=USSDAppWithRels)
def get_app_by_public_id(public_id: str, secret: Optional[str] = None, db: Session = Depends(get_db)):
    app = ussd_ussd_app.get_ussd_ussd_app_by_public_id(db, public_id)
    
    if app is None or (secret is not None and not secrets.compare_digest(app.secret, secret)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="App not found or secret does not match",
        )
    print(0)
    return app

#Fetch all apps of a tenant
@router.get("/apps", response_model=List[USSDAppRead])
def get_apps(tenant_id: str, db: Session = Depends(get_db)):
    return ussd_ussd_app.get_ussd_ussd_apps(db, tenant_id)

#Delete app
@router.delete("/apps/{app_id}")
def delete_app(app_id: int, db: Session = Depends(get_db)):
    return ussd_ussd_app.delete_ussd_ussd_app(db, app_id)

# def encode_tenant_id_to_hash(tenant_id: str, code: str) -> str:
#     # Combine the tenant_id and code and hash the result
#     data_to_hash = f"{tenant_id}{code}".encode('utf-8')
#     hashed_data = sha256(data_to_hash).digest()

#     # Convert the hashed data to a URL-safe base64-encoded string
#     hash_encoded = urlsafe_b64encode(hashed_data).decode('utf-8')

#     return hash_encoded

# def decode_hash_to_tenant_id(hash: str, code: str) -> str:
#     # Decode the hash from URL-safe base64
#     hashed_data = urlsafe_b64decode(hash.encode('utf-8'))

#     # Verify the integrity of the data by recomputing the hash
#     expected_hash = sha256(f"{tenant_id}{code}".encode('utf-8')).digest()

#     if hashed_data != expected_hash:
#         # Hash verification failed, handle error accordingly
#         raise ValueError("Hash verification failed")

#     # Extract the tenant_id from the original data
#     tenant_id = ...  # Implement the extraction logic based on your data format

#     return tenant_id