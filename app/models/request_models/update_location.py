from pydantic import BaseModel, Field, validator

class UpdateLocation(BaseModel):

    name: str = Field(None, min_length=1, max_length=100, description="Name of the location")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Name must not be empty or just whitespace')
        return v.strip() if v else v
