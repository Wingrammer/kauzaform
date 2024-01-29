from sqlmodel import Session, select
from app.db.engine import engine
from app.db.models.field import USSDField, USSDFieldCreate, USSDFieldUpdate

def create_ussd_form(db: Session, form: USSDFieldCreate):
    """Create an form"""
    db_form = USSDField.model_validate(form)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def get_ussd_form(db: Session, form_id: int):
    
    return db.exec(select(USSDField).where(USSDField.id == form_id)).first()

def get_ussd_forms(db: Session, tenant_id: str):
    """Get all forms of an app or a tenant"""
    
    return db.exec(select(USSDField).where(USSDField.tenant_id == tenant_id)).unique().all()

def update_ussd_form(db: Session, form_id: int, new_data: USSDFieldUpdate):
    db_form = db.get(USSDField, form_id)
    if not db_form:
        raise ValueError(f"USSDField with id {form_id} not found")
    form_data = new_data.model_dump(exclude_unset=True)
    for key, value in form_data.items():
        setattr(db_form, key, value)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def delete_ussd_form(db: Session, form_id: int):
    form = db.get(USSDField, form_id)
    if not form:
        raise ValueError(f"USSDField with id {form_id} not found")
    db.delete(form)
    db.commit()
    return form
