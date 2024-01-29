from typing import ClassVar, Optional

from sqlmodel import Field

from app.db.models.base import CustomBaseModel

class USSDAPIActionBase(CustomBaseModel):
    action_name: str = Field(index=True)
    curl_template: str

class USSDAPIAction(USSDAPIActionBase, table=True):
    pass

class USSDAPIActionRead(USSDAPIActionBase):
    pass

class USSDAPIActionCreate(USSDAPIActionBase):
    pass

class USSDAPIActionUpdate(CustomBaseModel):
    action_name: Optional[str] = None
    curl_template: Optional[str] = None

class USSDAPIActionWithRels(USSDAPIActionRead):
    pass