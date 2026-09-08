from sqlmodel import SQLModel, Field
from datetime import datetime

class Review(SQLModel, table=True):

    id : int | None = Field(default=None, primary_key=True)
    restaurant_id : int | None = Field(default=None,foreign_key='restaurant.id')

    rating : int = Field(ge=1, le=5)
    reviewer_name :str 
    phone_no : str|None = Field(default=None,min_length=10, max_length=10)
    description:str | None  = Field(default=None)
    created_at : datetime| None= Field(default_factory=datetime.now)

    redirected_at_google: bool = Field(default=False)

    

    
class ReviewCreate(SQLModel):
    restaurant_id : int 
    rating : int = Field(ge=1, le=5)
    reviewer_name : str = Field(max_length=35)

    phone_no : str| None = Field(default=None,min_length=10, max_length=10)
    description:str | None  = Field(default=None, max_length=1000)
    





    
