from fastapi import FastAPI
from contextlib import asynccontextmanager
from model.model import create_db_and_table

from routes.restaurants import router as restaurant_router
from routes.reviews import router as reviews_router
import uvicorn

@asynccontextmanager
async def lifespan(app:FastAPI):
    "Lifecycle of FastAPI app"
    # Startup Logic
    print("Starting APP: Creating database and tables..")
    create_db_and_table()
    print("Database and tables created.")
    yield

    # Shutdown clean-up
    print("Shutting down application.")


app = FastAPI(title='Restaurant Review',version='1.0.0',lifespan=lifespan,debug=True)

app.include_router(restaurant_router)
app.include_router(reviews_router)

@app.get('/',tags=['root'])
def root():
    return {
        'message':"Welcome to Restaurant Review Analysis application."
    }


if __name__ == '__main__':
    uvicorn.run('app:app',port = 8080,reload=True)