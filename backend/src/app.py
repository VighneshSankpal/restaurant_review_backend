from fastapi import FastAPI, Depends,status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from model.model import create_db_and_table
from model.owner import CurrentOwner

from utils.authenticate import check_authentication

from utils.settings import settings
from routes.restaurants import router as restaurant_router
from routes.owners import router as owner_router
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

app.add_middleware(CORSMiddleware,settings.ALLOWED_ORIGINS,allow_credentials=True,allow_headers=['*'],allow_methods=["*"])

app.include_router(restaurant_router)
app.include_router(owner_router)

@app.get('/',tags=['root'])
def root():
    return {
        'message':"Welcome to Restaurant Review Analysis application."
    }

@app.get('/health',tags=['health'],status_code=status.HTTP_200_OK)
def health(owner : CurrentOwner =  Depends(check_authentication) ):
    return {"key":True}

if __name__ == '__main__':
    uvicorn.run('app:app',port = 8080,reload=True)