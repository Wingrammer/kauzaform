from sqlmodel import Field, Relationship
from app.db.models.form import USSDForm
from app.db.models.state import USSDState
from .option import USSDOption
from app.db.models.base import CustomBaseModel
from typing import Any, List, Optional

class USSDAppBase(CustomBaseModel):
    secret: Optional[str] = None
    initial_state_id: Optional[int] = Field(default=None, foreign_key="ussdstate.id", nullable=True)
    code: str = Field(index=True, unique=True)
    session_expiry: int = Field(default=30)

class USSDApp(USSDAppBase, table=True):
    states: Optional[List[USSDState]] = Relationship(back_populates="app", sa_relationship_kwargs={"primaryjoin":"USSDState.app_id == USSDApp.id", "lazy": "joined"})
    forms: Optional[List[USSDForm]] = Relationship(back_populates="app", sa_relationship_kwargs={"primaryjoin":"USSDForm.app_id == USSDApp.id", "lazy": "joined"})

class USSDAppCreate(USSDAppBase):
    pass

class USSDAppRead(USSDAppBase):
    pass

class USSDAppUpdate(CustomBaseModel):
    secret: Optional[str] = None
    initial_state_id: Optional[int] = None
    code: Optional[str] = None
    session_expiry: Optional[int] = None

class USSDAppWithRels(USSDAppRead):
    states: List[Any] = []
    forms: List[Any] = []