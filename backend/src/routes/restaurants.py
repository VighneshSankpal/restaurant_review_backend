from fastapi import APIRouter, Depends, Query, HTTPException,status
from sqlmodel import Session, select, func, update

from model.model import get_session

from model.restaurants import Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantListResponse,RestaurantDelete

from utils.authenticate import check_authentication 
from model.owner import CurrentOwner
from model.reviews import ReviewListResponse, Review, ReviewCreate


router = APIRouter(prefix='/restaurant',tags=['restaurant'])


@router.post('/')
def add_restaurant(data:RestaurantCreate, session : Session = Depends(get_session), owner:CurrentOwner = Depends(check_authentication)):

    restaurant_data= data.model_dump()
    records = session.exec(select(Restaurant).where(Restaurant.owner_id == owner.id)).one_or_none()

    if records:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail={"message":"Only single restaurant allowed per owner."})
    restaurant_data['owner_id'] = owner.id



    new_restaurant = Restaurant(**restaurant_data)

    session.add(new_restaurant)
    session.commit()
    session.refresh(new_restaurant)
    return new_restaurant


# Get all present restaurant records
@router.get('/',response_model=RestaurantListResponse)
def read_restaurants(session: Session= Depends(get_session),owner:CurrentOwner = Depends(check_authentication)):
    
    count_query = select(func.count()).select_from(Restaurant).where(Restaurant.owner_id == owner.id)
    total_count = session.exec(count_query).one()

    query = select(Restaurant).where(Restaurant.owner_id == owner.id)

    restaurants = session.exec(query).all()

    return RestaurantListResponse(restaurants=restaurants , total_count = total_count)


@router.patch('/update/{restaurant_id}', response_model=Restaurant, )
def update_restaurant_data( 
                        restaurant_id:int,                           
                        restaurant_update: RestaurantUpdate,
                        session :Session= Depends(get_session),
                        owner:CurrentOwner = Depends(check_authentication)
                           ):

   
    restaurant = session.get(Restaurant,restaurant_id)   
    

    if restaurant and  restaurant.owner_id == owner.id:
        update_data = restaurant_update.model_dump(exclude_unset=True)

        for key,val in update_data.items():
            setattr(restaurant,key,val)

        session.add(restaurant)
        session.commit()
        session.refresh(restaurant)

        return restaurant

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                            "error_code": "RESTAURANT_NOT_FOUND",
                            'message':f'Restaurant with {restaurant_id} does not exist',
                            'restaurant_id':restaurant_id}
                            )



@router.delete('/delete/{restaurant_id}',response_model=RestaurantDelete)
def remove_restaurant(restaurant_id:int, session:Session= Depends(get_session), owner:CurrentOwner= Depends(check_authentication)):

    restaurant =  session.get(Restaurant,restaurant_id)

    if restaurant and restaurant.owner_id == owner.id:
        session.delete(restaurant)                                                    
        session.commit()
        return RestaurantDelete(record=restaurant)

    else:
        raise HTTPException(status_code=404,detail={'error_code':'RESTAURNT_NOT_FOUND',
                                                    'message':f'Restaurant with {restaurant_id} does not exist',
                                                    'restaurant_id':restaurant_id
                                                    })






@router.get('/{rest_id}/reviews',response_model=ReviewListResponse)
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



@router.post('/{rest_id}/reviews',response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(rest_id:int, new_review:ReviewCreate, session:Session = Depends(get_session)):

    review_data = new_review.model_dump(exclude_unset=True)

    restaurant = session.exec(select(Restaurant).where(Restaurant.id == rest_id)).one_or_none()

    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'message':f"Restaurant Not Found of ID: {rest_id}", 'restaurant_id':rest_id})

    review_data['restaurant_id'] = restaurant.id

    review = Review(**review_data)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review




