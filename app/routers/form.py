# app/routers/ussd_form.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.crud import form as ussd_form
from app.db.models.form import USSDForm, USSDFormCreate, USSDFormRead, USSDFormUpdate, USSDFormWithRels
from app.db.engine import get_db

router = APIRouter()

# Add your routes here

#Create form
@router.post("/forms/", response_model=USSDFormRead)
def create_form(form: USSDFormCreate, db: Session = Depends(get_db)):
    return ussd_form.create_ussd_form(db, form)

# Add other routes as needed

#Update form
@router.patch("/forms/{form_id}", response_model=USSDFormRead)
def update_form(form_id: int, form: USSDFormUpdate, db: Session = Depends(get_db)):
    return ussd_form.update_ussd_form(db, form_id, form)

#Fetch form
@router.get("/forms/{form_id}", response_model=USSDFormWithRels)
def get_form(form_id: int, db: Session = Depends(get_db)):
    return ussd_form.get_ussd_form(db, form_id)

#Fetch all forms of a app
@router.get("/forms", response_model=List[USSDFormRead])
def get_forms(app_id: int, db: Session = Depends(get_db)):
    return ussd_form.get_ussd_forms(db, app_id)

#Delete form
@router.delete("/forms/{form_id}")
def delete_form(form_id: int, db: Session = Depends(get_db)):
    return ussd_form.delete_ussd_form(db, form_id)