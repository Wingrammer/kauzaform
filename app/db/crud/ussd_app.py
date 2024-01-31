from sqlmodel import Session, select
from app.db.engine import engine
from app.db.models.ussd_app import USSDApp, USSDAppCreate, USSDAppUpdate

def create_ussd_ussd_app(db: Session, ussd_app: USSDAppCreate):
    """Create an app"""
    db_ussd_app = USSDApp.model_validate(ussd_app)
    db.add(db_ussd_app)
    db.commit()
    db.refresh(db_ussd_app)
    return db_ussd_app

def get_ussd_ussd_app(db: Session, ussd_app_id: int):
    return db.exec(select(USSDApp).where(USSDApp.id == ussd_app_id)).first()

def get_ussd_ussd_apps(db: Session, tenant_id: str):
    """Get all apps of a tenant"""
    return db.exec(select(USSDApp).where(USSDApp.tenant_id == tenant_id)).unique().all()

def get_ussd_ussd_app_by_public_id(db: Session, public_id: str):
    return db.exec(select(USSDApp).where(USSDApp.public_id == public_id)).unique().one()

def update_ussd_ussd_app(db: Session, ussd_app_id: int, new_data: USSDAppUpdate):
    db_ussd_app = db.get(USSDApp, ussd_app_id)
    if not db_ussd_app:
        raise ValueError(f"USSDApp with id {ussd_app_id} not found")
    ussd_app_data = new_data.model_dump(exclude_unset=True)
    for key, value in ussd_app_data.items():
        setattr(db_ussd_app, key, value)
    db.add(db_ussd_app)
    db.commit()
    db.refresh(db_ussd_app)
    return db_ussd_app

def delete_ussd_ussd_app(db: Session, ussd_app_id: int):
    ussd_app = db.get(USSDApp, ussd_app_id)
    if not ussd_app:
        raise ValueError(f"USSDApp with id {ussd_app_id} not found")
    db.delete(ussd_app)
    db.commit()
    return ussd_app
