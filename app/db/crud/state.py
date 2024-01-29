from sqlmodel import Session, select
from app.db.engine import engine
from app.db.models.state import USSDState, USSDStateCreate, USSDStateUpdate

def create_ussd_state(db: Session, state: USSDStateCreate):
    """Create an state"""
    db_state = USSDState.model_validate(state)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state

def get_ussd_state(db: Session, state_id: int):
    
    return db.exec(select(USSDState).where(USSDState.id == state_id)).first()

def get_ussd_states(db: Session, tenant_id: str):
    """Get all states of an app or a tenant"""
    
    return db.exec(select(USSDState).where(USSDState.tenant_id == tenant_id)).unique().all()

def update_ussd_state(db: Session, state_id: int, new_data: USSDStateUpdate):
    db_state = db.get(USSDState, state_id)
    if not db_state:
        raise ValueError(f"USSDState with id {state_id} not found")
    state_data = new_data.model_dump(exclude_unset=True)
    for key, value in state_data.items():
        setattr(db_state, key, value)
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state

def delete_ussd_state(db: Session, state_id: int):
    state = db.get(USSDState, state_id)
    if not state:
        raise ValueError(f"USSDState with id {state_id} not found")
    db.delete(state)
    db.commit()
    return state
