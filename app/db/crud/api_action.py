from sqlmodel import Session, select
from app.db.engine import engine
from app.db.models.api_action import USSDAPIAction, USSDAPIActionCreate, USSDAPIActionUpdate

def create_ussd_api_action(db: Session, api_action: USSDAPIActionCreate):
    """Create an api_action"""
    db_api_action = USSDAPIAction.model_validate(api_action)
    db.add(db_api_action)
    db.commit()
    db.refresh(db_api_action)
    return db_api_action

def get_ussd_api_action(db: Session, api_action_id: int):
    
    return db.exec(select(USSDAPIAction).where(USSDAPIAction.id == api_action_id)).first()

def get_ussd_api_actions(db: Session, tenant_id: str):
    """Get all api_actions of an app or a tenant"""
    
    return db.exec(select(USSDAPIAction).where(USSDAPIAction.tenant_id == tenant_id)).unique().all()

def update_ussd_api_action(db: Session, api_action_id: int, new_data: USSDAPIActionUpdate):
    db_api_action = db.get(USSDAPIAction, api_action_id)
    if not db_api_action:
        raise ValueError(f"USSDAPIAction with id {api_action_id} not found")
    api_action_data = new_data.model_dump(exclude_unset=True)
    for key, value in api_action_data.items():
        setattr(db_api_action, key, value)
    db.add(db_api_action)
    db.commit()
    db.refresh(db_api_action)
    return db_api_action

def delete_ussd_api_action(db: Session, api_action_id: int):
    api_action = db.get(USSDAPIAction, api_action_id)
    if not api_action:
        raise ValueError(f"USSDAPIAction with id {api_action_id} not found")
    db.delete(api_action)
    db.commit()
    return api_action
