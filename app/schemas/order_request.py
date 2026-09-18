from pydantic import BaseModel


class OrderExtractionRequest(BaseModel):
    text: str