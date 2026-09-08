from sqlmodel import Session, create_engine, SQLModel


sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url,echo=True)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)



def get_session():
    """
    Yield the database session context.
    FastAPI handlers closing the request automatically after the request lifecycle.
    """

    with Session(engine) as session:
        yield session