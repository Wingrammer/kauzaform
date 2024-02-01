import uuid
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional

from app.db.models.state import USSDStateWithRels

def generate_session_id() -> str:
    """
    Generate a unique session ID using UUID.
    """
    return str(uuid.uuid4())



class USSDSessionInput(BaseModel):
    id: Optional[str] = Field(default_factory=generate_session_id)
    user_id: str
    user_input: Optional[str] = None
    app_id: Optional[str] = None
    resume_old_session: bool = False
    # Add other session-related fields as needed

    class Config:
        from_attributes = True

class USSDSession(USSDSessionInput):
    
    expiration: Optional[datetime] = None
    current_state: Optional[USSDStateWithRels] = None
    output: Optional[str | bytes] = None
