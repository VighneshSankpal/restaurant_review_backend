from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from model.owner import Owner, OwnerCreate, OwnerListResponse, OwnerDelete, OwnerUpdate
from model.model import get_session
from datetime import datetime, timedelta
from pwdlib import PasswordHash

import jwt

from utils.settings import settings

password_hash = PasswordHash.recommended()

def get_password_hash(password:str):
    return password_hash.hash(password)

def veryfiy_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

router = APIRouter(prefix='/owner',tags=['owner'])


@router.post('/',response_model=Owner, status_code=status.HTTP_201_CREATED)
def add_owner(data:OwnerCreate, session:Session=Depends(get_session)):

    
    owner_data = data.model_dump(exclude_unset=True)
    try:
        password = owner_data.pop('password')
        owner_data['hashed_password'] = get_password_hash(password)       
        

        new_owner = Owner(**owner_data)    
    
        session.add(new_owner)
        session.commit()
        session.refresh(new_owner)

    

    except IntegrityError as e:
        raise HTTPException(status_code=409, detail={'ERROR_CORE':'INTEGRITY_ERROR',
                                                     'message':f"{new_owner.email} already exist in database.",
                                                     'email':new_owner.email,
                                                     
                                                     })

    except Exception as e:

        raise HTTPException(status_code=400,detail={'message':"Invalid Input."})

    return new_owner

    

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

    exp_time = datetime.now()+timedelta(hours=48)

    token = jwt.encode(payload={'_id':owner.id,'email':owner.email},
                       key=settings.LOGIN_SECREATE_KEY, 
                       algorithm=settings.LOGIN_ALGORITHM
                       )

    return token


 
    


@router.get('/',response_model=OwnerListResponse)
def get_owners( session:Session = Depends(get_session)):

    count_query = select(func.count()).select_from(Owner)
    total_count = session.exec(count_query).one()
    query =  select(Owner)

    owners =  session.exec(query).all()

    return OwnerListResponse(count = total_count, owners=owners)



@router.patch('/update/{id}',response_model=OwnerUpdate)
def update_owner_info(id:int,data : OwnerUpdate, session:Session=Depends(get_session)):

    owner_record = session.get(Owner,id)

    if not owner_record:
        raise HTTPException(status_code=404,detail={'owner_id':id,
                                                    'ERROR_CODE':'OWNER_NOT_FOUND',
                                                    'message':f'Owner with id: {id} is not present in the database'
                                                    }
                                                    )


    update_data = data.model_dump(exclude_unset=True)

    for key,val in update_data.items():
        setattr(owner_record,key,val)


    # session.add(owner_record)
    session.commit()
    session.refresh(owner_record)

    return owner_record
