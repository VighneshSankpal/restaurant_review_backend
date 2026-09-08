from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, update

from model.model import get_session

from model.restaurants import Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantListResponse,RestaurantDelete

router = APIRouter(prefix='/restaurant',tags=['restaurant'])


@router.post('/')
def add_restaurant(data:RestaurantCreate, session : Session = Depends(get_session)):

    new_restaurant = Restaurant(**data.model_dump())

    session.add(new_restaurant)
    session.commit()
    session.refresh(new_restaurant)
    return new_restaurant


# Get all present restaurant records
@router.get('/',response_model=RestaurantListResponse)
def read_restaurants(session: Session= Depends(get_session)):

    count_query = select(func.count()).select_from(Restaurant)
    total_count = session.exec(count_query).one()

    query = select(Restaurant)

    restaurants = session.exec(query).all()

    return RestaurantListResponse(restaurants=restaurants , total_count = total_count)


@router.patch('/update/{restaurant_id}', response_model=Restaurant)
def update_restaurant_data( 
                        restaurant_id:int,                           
                        restaurant_update: RestaurantUpdate,
                        session :Session= Depends(get_session),
                           ):

    restaurant = session.get(Restaurant,restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404,
                            detail={
                            "error_code": "RESTAURANT_NOT_FOUND",
                            'message':f'Restaurant with {restaurant_id} does not exist',
                            'restaurant_id':restaurant_id}
                            )


    update_data = restaurant_update.model_dump(exclude_unset=True)

    for key,val in update_data.items():
        setattr(restaurant,key,val)

    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)

    return restaurant


@router.delete('/delete/{restaurant_id}',response_model=RestaurantDelete)
def remove_restaurant(restaurant_id:int, session:Session= Depends(get_session)):

    restaurant =  session.get(Restaurant,restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404,detail={'error_code':'RESTAURNT_NOT_FOUND',
                                                    'message':f'Restaurant with {restaurant_id} does not exist',
                                                    'restaurant_id':restaurant_id
                                                    })

    session.delete(restaurant)                                                    
    session.commit()

    return RestaurantDelete(record=restaurant)
