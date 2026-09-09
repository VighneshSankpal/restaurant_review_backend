from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from model.owner import Owner, OwnerCreate, OwnerListResponse, OwnerDelete, OwnerUpdate
from model.model import get_session



router = APIRouter(prefix='/owner',tags=['owner'])

@router.post('/',response_model=OwnerCreate)
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



