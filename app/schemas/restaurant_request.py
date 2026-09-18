from pydantic import BaseModel


class RestaurantRequest(BaseModel):
    restaurant_name: str
    cuisine: str