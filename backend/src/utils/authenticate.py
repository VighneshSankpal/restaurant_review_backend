from jwt.exceptions import InvalidTokenError
from fastapi import Request,Depends, HTTPException, status 
from sqlmodel import Session, select

from datetime import datetime
from utils.settings import settings
import jwt
from model.model import get_session
from model.owner import Owner, CurrentOwner

def check_authentication(request: Request, session : Session= Depends(get_session)):


    token = request.headers.get('authorization')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'detail':"Authorized before using application"})

    token = token.split(" ")[-1]


    try:

        data= jwt.decode(token,key=settings.LOGIN_SECREATE_KEY, algorithms=[settings.LOGIN_ALGORITHM])

        current_time = datetime.now().timestamp()
        if current_time >  data['expiration_time']:
            raise InvalidTokenError()
            
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'detail':"Authorized before using application"})


    owner = session.exec(select(Owner).where(Owner.id == data.get('id') ,Owner.email == data.get('email') )).one_or_none()

    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'detail':"Authorized before using application"})
        
    return CurrentOwner(id=owner.id, email=owner.email)



        
