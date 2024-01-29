from sqlmodel import Session, select
from app.db.engine import engine
from app.db.models.option import USSDOption, USSDOptionCreate, USSDOptionUpdate

def create_ussd_option(db: Session, option: USSDOptionCreate):
    """Create an option"""
    db_option = USSDOption.model_validate(option)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

def get_ussd_option(db: Session, option_id: int):
    
    return db.exec(select(USSDOption).where(USSDOption.id == option_id)).first()

def get_ussd_options(db: Session, tenant_id: str):
    """Get all options of an app or a tenant"""
    
    return db.exec(select(USSDOption).where(USSDOption.tenant_id == tenant_id)).unique().all()

def update_ussd_option(db: Session, option_id: int, new_data: USSDOptionUpdate):
    db_option = db.get(USSDOption, option_id)
    if not db_option:
        raise ValueError(f"USSDOption with id {option_id} not found")
    option_data = new_data.model_dump(exclude_unset=True)
    for key, value in option_data.items():
        setattr(db_option, key, value)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option

def delete_ussd_option(db: Session, option_id: int):
    option = db.get(USSDOption, option_id)
    if not option:
        raise ValueError(f"USSDOption with id {option_id} not found")
    db.delete(option)
    db.commit()
    return option
