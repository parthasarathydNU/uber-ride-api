from pydantic import BaseModel


class BookingRequest(BaseModel):
    customerName: str
    from_location: str
    to_location: str