from sqlmodel import Session, select, func
from fastapi import APIRouter, Depends, Query, HTTPException, status

from model.reviews import Review, ReviewCreate, ReviewDelete, ReviewListResponse
from model.restaurants import Restaurant
from model.model import get_session, CurrentOwner
from utils.authenticate import check_authentication
from fastapi import status
router = APIRouter(prefix='/review',tags=['review'])


@router.post('/',response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(new_review:ReviewCreate, session:Session = Depends(get_session)):

    restaurant = session.get(Restaurant,new_review.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'detail':'Restaurant Not Found'})


    review = Review(**new_review.model_dump())
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.get('/{rest_id}',response_model=ReviewListResponse)
def read_all_review(rest_id:int,
                    session:Session= Depends(get_session),
                    owner :CurrentOwner = Depends(check_authentication)
                    ):

    restaurant_qurry = select(Restaurant).where(Restaurant.owner_id == owner.id, Restaurant.id== rest_id)
    restaurant_record = session.exec(restaurant_qurry).one_or_none()

    if not restaurant_record:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"details":"you are not allowed to view this data"})

    # Count total numbers of reviews 
    count_query = select(func.count(Review.id)).where(Review.restaurant_id == rest_id)
    count = session.exec(count_query).one()

    # Get the actual reviews. 
    query = select(Review).where(Review.restaurant_id == rest_id )
    reviews = session.exec(query).all()

    return ReviewListResponse(count=count, reviews= reviews)






