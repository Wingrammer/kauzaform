from sqlmodel import Field, Relationship
from app.db.models.base import CustomBaseModel
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional
if TYPE_CHECKING:
    from app.db.models.state import USSDState

class USSDFieldBase(CustomBaseModel):
    prompt: str
    field_name: str = Field(index=True)
    state_id: Optional[int] = Field(default=None, foreign_key="ussdstate.id", nullable=True)
    

class USSDField(USSDFieldBase, table=True):
    states: Optional[List["USSDState"]] = Relationship(back_populates="fields", sa_relationship_kwargs=dict(foreign_keys="[USSDField.state_id]"))

class USSDFieldRead(USSDFieldBase):
    pass

class USSDFieldCreate(USSDFieldBase):
    pass

class USSDFieldUpdate(CustomBaseModel):
    prompt: Optional[str] = None
    field_name: Optional[str] = None
    state_id: Optional[int] = None

class USSDFieldWithRels(USSDFieldRead):
    states: List[Any] = []