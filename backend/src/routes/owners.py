from fastapi import APIRouter, Depends, HTTPException,status, Request
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from model.owner import Owner, OwnerCreate, OwnerListResponse, OwnerDelete, OwnerUpdate
from model.model import get_session
from datetime import datetime, timedelta
from pwdlib import PasswordHash

import jwt
from utils.settings import settings

from utils.authenticate import check_authentication 


password_hash = PasswordHash.recommended()

def get_password_hash(password:str):
    return password_hash.hash(password)

def veryfiy_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

router = APIRouter(prefix='/owner',tags=['owner'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_owner(data:OwnerCreate, session:Session=Depends(get_session),):

    
    owner_data = data.model_dump(exclude_unset=True)
    try:
        password = owner_data.pop('password')
        owner_data['hashed_password'] = get_password_hash(password)       
        

        new_owner = Owner(**owner_data)    
    
        session.add(new_owner)
        session.commit()
        session.refresh(new_owner)

        exp_time = int((datetime.now()+timedelta(hours=settings.TOKEN_EXP_HOURS)).timestamp())
        
        token = jwt.encode(payload={'id':new_owner.id,'email':new_owner.email, 'expiration_time':exp_time},
                            key=settings.LOGIN_SECRET_KEY, 
                            algorithm=settings.LOGIN_ALGORITHM,
    
                            
                            )
        return {'token':token}

    

    except IntegrityError as e:
        raise HTTPException(status_code=409, detail={'ERROR_CORE':'INTEGRITY_ERROR',
                                                     'message':f"{new_owner.email} already exist in database.",
                                                     'email':new_owner.email,
                                                     
                                                     })

    except Exception as e:

        raise HTTPException(status_code=400,detail={'message':"Invalid Input."})


    

@router.post('/login',status_code=status.HTTP_200_OK)
def login_user(data:OwnerCreate, session:Session = Depends(get_session),):
    query = select(Owner).where(Owner.email == data.email)

    owner =  session.exec(query).one_or_none()

    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail={
                                "ERROR_CODE":"INVALID_CREDENTIAL",
                                 'message': 'Invalid email or password.'
                                 }
                            )


    if not veryfiy_password(data.password, owner.hashed_password) :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail={
                                "ERROR_CODE":"INVALID_CREDENTIAL",
                                 'message': 'Invalid email or password.'
                                 }
                            )

    exp_time = int((datetime.now()+timedelta(hours=settings.TOKEN_EXP_HOURS)).timestamp())

    token = jwt.encode(payload={'id':owner.id,'email':owner.email, 'expiration_time':exp_time},
                       key=settings.LOGIN_SECRET_KEY, 
                       algorithm=settings.LOGIN_ALGORITHM,

                       
                       )

    return {"token":token}


 
    


@router.get('/',response_model=OwnerListResponse)
def get_owners( session:Session = Depends(get_session)):

    count_query = select(func.count()).select_from(Owner)
    total_count = session.exec(count_query).one()
    query =  select(Owner)

    owners =  session.exec(query).all()

    return OwnerListResponse(count = total_count, owners=owners)



@router.patch('/update',response_model=OwnerUpdate)
def update_owner_info(data : OwnerUpdate, session:Session=Depends(get_session),  owner = Depends(check_authentication)):

    update_data = data.model_dump(exclude_unset=True)

    for key,val in update_data.items():
        setattr(owner,key,val)

    
    session.commit()
    session.refresh(owner)

    return owner



