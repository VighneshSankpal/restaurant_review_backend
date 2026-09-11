from sqlmodel import Session, create_engine, SQLModel
from pydantic import BaseModel,EmailStr
from sqlalchemy import event
import os 
from utils.settings import settings



# sqlite_file_name = 'database.db'
# sqlite_url = f'sqlite:///{sqlite_file_name}'

# engine = create_engine(sqlit,e_url,echo=True)




engine = create_engine(settings.DATABASE_URL,echo=True)
def create_db_and_table():
    SQLModel.metadata.create_all(engine)


# @event.listens_for(engine, "connect")
# def enable_foreign_keys(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


def get_session():
    """
    Yield the database session context.
    FastAPI handlers closing the request automatically after the request lifecycle.
    """

    with Session(engine) as session:
        yield session


class CurrentOwner(BaseModel):
    id:int 
    email : EmailStr
