from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class USSDSession(BaseModel):
    id: str
    app_id: str
    user_id: str
    expiration: Optional[datetime]
    current_state: Optional[int] = None
    # Add other session-related fields as needed

    class Config:
        orm_mode = True
