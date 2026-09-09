from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session, select, func

from model.owner import Owner, OwnerCreate, OwnerListResponse, OwnerDelete, OwnerUpdate
from model.model import get_session


router = APIRouter(prefix='/owner',tags=['owner'])


@router.post('/',response_model=OwnerCreate, status_code=status.HTTP_201_CREATED)
def add_owner(data:OwnerCreate, session:Session=Depends(get_session)):

    new_owner = Owner(**data.model_dump())

    session.add(new_owner)
    session.commit()
    session.refresh(new_owner)

    return new_owner


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
