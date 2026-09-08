from sqlmodel import Session, select, func
from fastapi import APIRouter, Depends, Query

from model.reviews import Review, ReviewCreate, ReviewDelete, ReviewListResponse
from model.model import get_session


router = APIRouter(prefix='/review',tags=['review'])


@router.post('/',response_model=Review)
def create_review(new_review:ReviewCreate, session:Session = Depends(get_session)):

    review = Review(**new_review.model_dump())

    session.add(review)
    session.commit()
    session.refresh(review)

    return review


@router.get('/',response_model=ReviewListResponse)
def read_all_review(rest_id:int,
                    session:Session= Depends(get_session)):

    count_query = select(func.count(Review.id)).where(Review.restaurant_id == rest_id)
    count = session.exec(count_query).one()



    query = select(Review).where(Review.restaurant_id == rest_id )
    reviews = session.exec(query)

    return ReviewListResponse(count=count, reviews= reviews)



