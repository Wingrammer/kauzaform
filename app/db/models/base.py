from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class CustomBaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    tenant_id: str = Field(index=True)