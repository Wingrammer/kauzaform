from sqlmodel import Field, Relationship
from app.db.models.base import CustomBaseModel
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from app.db.models.state import USSDState

class USSDOptionBase(CustomBaseModel):
    option_text: str
    option_value: str
    triggers_form: Optional[str] = None
    curl_template: Optional[str] = None
    next_state_id: Optional[int] = Field(default=None, foreign_key="ussdstate.id")
    state_id: Optional[int] = Field(default=None, foreign_key="ussdstate.id")
    app_id: int = Field(foreign_key="ussdapp.id")

class USSDOption(USSDOptionBase, table=True):
    next_state: Optional[USSDState] = Relationship(back_populates="previous_option", sa_relationship_kwargs=dict(foreign_keys="[USSDOption.next_state_id]"))
    state: Optional[USSDState] = Relationship(back_populates="options", sa_relationship_kwargs=dict(foreign_keys="[USSDOption.state_id]"))

class USSDOptionRead(USSDOptionBase):
    pass

class USSDOptionCreate(USSDOptionBase):
    pass

class USSDOptionUpdate(CustomBaseModel):
    option_text: Optional[str] = None
    option_value: Optional[str] = None
    triggers_form: Optional[str] = None
    curl_template: Optional[str] = None
    next_state_id: Optional[int] = None
    state_id: Optional[int] = None

class USSDOptionWithRels(USSDOptionBase):
    next_state: Optional[Any] = None
    state: Optional[Any] = None