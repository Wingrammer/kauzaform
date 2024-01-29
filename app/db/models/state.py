from sqlmodel import Field, Relationship
from app.db.models.field import USSDField
from app.db.models.base import CustomBaseModel
from typing import TYPE_CHECKING, Any, ClassVar, Optional, List


if TYPE_CHECKING:
    from app.db.models.option import USSDOption
    from app.db.models.form import USSDForm
    from app.db.models.ussd_app import USSDApp

class USSDStateBase(CustomBaseModel):
    state_name: str
    message: str
    submission_action: Optional[str] = None
    curl_template: Optional[str] = None
    response_template: Optional[str] = None
    form_id: Optional[int] = Field(default=None, foreign_key="ussdform.id", nullable=True)
    app_id: int = Field(foreign_key="ussdapp.id")

class USSDState(USSDStateBase, table=True):
    
    # initial_to_app_id: Optional[int] = Field(default=None, foreign_key="ussdapp.id", nullable=True)
    # initial_to_app: Optional["USSDApp"] = Relationship(back_populates="initial_state")
    options: Optional[List["USSDOption"]] = Relationship(back_populates="state", sa_relationship_kwargs={"primaryjoin":"USSDOption.state_id == USSDState.id", "lazy": "joined"})
    previous_option: Optional["USSDOption"] = Relationship(back_populates="next_state", sa_relationship_kwargs={"primaryjoin":"USSDOption.state_id == USSDState.id", "lazy": "joined"})
    fields: Optional[List[USSDField]] = Relationship(back_populates="states", sa_relationship_kwargs={"primaryjoin":"USSDField.state_id == USSDState.id", "lazy": "joined"})
    form: Optional["USSDForm"] = Relationship(back_populates="states", sa_relationship_kwargs=dict(foreign_keys="[USSDState.form_id]"))
    app: "USSDApp" = Relationship(back_populates="states", sa_relationship_kwargs=dict(foreign_keys="[USSDState.app_id]"))

class USSDStateRead(USSDStateBase):
    pass

class USSDStateCreate(USSDStateBase):
    pass

class USSDStateUpdate(CustomBaseModel):
    state_name: Optional[str] = None
    message: Optional[str] = None
    submission_action: Optional[str] = None
    curl_template: Optional[str] = None
    response_template: Optional[str] = None
    form_id: Optional[int] = None

class USSDStateWithRels(USSDStateRead):
    options: List[Any] = []
    previous_option: Optional[Any] = None
    fields: List[Any] = []
    form: Optional[Any] = None
