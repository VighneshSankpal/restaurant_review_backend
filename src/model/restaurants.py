from sqlmodel import SQLModel, Field
from datetime import datetime



class Restaurant(SQLModel, table=True):

    id : int|None = Field(default=None, primary_key=True)
    name: str = Field( max_length=50)
    google_place_id : str| None = Field(default=None,index=True)
    created_at : datetime = Field(default_factory=datetime.now)
    is_veg_only : bool = Field(default=False)

    location: str = Field(max_length=50)

    owner_id : int = Field(foreign_key='owner.id',unique=True)

    updated_at : datetime = Field(default_factory=datetime.now)



class RestaurantCreate(SQLModel):
    name: str = Field( max_length=50)
    google_place_id : str | None = Field(default=None)
    is_veg_only : bool = Field(default=False)
    owner_id: int 
    location: str = Field(max_length=50)
    



class RestaurantUpdate(SQLModel):

    name: str|None = Field(default=None, max_length=50)
    google_place_id : str|None = Field(default=None)
    is_veg_only : bool | None = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)
    location: str|None = Field(default=None, max_length=50)



class RestaurantListResponse(SQLModel):
    success: bool = True
    total_count :int|None 
    restaurants : list[Restaurant]



class RestaurantDelete(SQLModel):
    success: bool= True
    record :Restaurant


