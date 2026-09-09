from model.owner import OwnerCreate
from model.model import get_session
from fastapi import Depends
from sqlmodel import Session

def register(owner:OwnerCreate,session:Session= Depends(get_session)):
    return {
        'msg':"Register Owner."
    }