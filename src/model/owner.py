from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class Owner(SQLModel, table=True):

    id :int|None = Field(default=None,primary_key=True)
    email :EmailStr = Field(unique=True,index=True)
    hashed_password : str
    created_at: datetime |None= Field(default_factory=datetime.now)




class OwnerCreate(SQLModel):
    """Owner validations while creating new owner"""

    email : EmailStr
    hashed_password: str |None = Field(default=None)
    password: str 



class OwnerUpdate(SQLModel):
    """Update the owner attribute field values."""
    email: EmailStr|None = Field(default=None)
    hashed_password : str|None =  Field(default=None)



class OwnerListResponse(SQLModel):
    """Return the multiple owners at same type. (mainly for testing not much real usecase)"""

    success: bool |None = Field(default=True)
    count: int 
    owners : list[Owner]



class OwnerDelete(SQLModel):
    """Delete the owner data."""
    success: bool|None = Field(default=True)
    owner : Owner
