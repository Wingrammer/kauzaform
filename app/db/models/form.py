from sqlmodel import Field, Relationship
from app.db.models.base import CustomBaseModel
from typing import TYPE_CHECKING, Any, ClassVar, Optional, List


if TYPE_CHECKING:
    from app.db.models.state import USSDState
    from app.db.models.ussd_app import USSDApp

class USSDFormBase(CustomBaseModel):
    submission_action: Optional[str] = None
    response_template: Optional[str] = None
    form_name: str = Field(index=True)
    app_id: int = Field(foreign_key="ussdapp.id")

class USSDForm(USSDFormBase, table=True):
    states: Optional[List["USSDState"]] = Relationship(back_populates="form", sa_relationship_kwargs={"primaryjoin":"USSDState.form_id == USSDForm.id", "lazy": "joined"})
    app: "USSDApp" = Relationship(back_populates="forms", sa_relationship_kwargs=dict(foreign_keys="[USSDForm.app_id]"))

class USSDFormRead(USSDFormBase):
    pass

class USSDFormCreate(USSDFormBase):
    pass

class USSDFormUpdate(CustomBaseModel):
    submission_action: Optional[str] = None
    response_template: Optional[str] = None
    form_name: Optional[str] = None

class USSDFormWithRels(USSDFormRead):
    states: List[Any] = []