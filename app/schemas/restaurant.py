from pydantic import BaseModel


class RestaurantInfo(BaseModel):
    name: str
    cuisine: str
    description: str
    rating: float
    vegetarian: bool