from pydantic import field_validator
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal


class GenderType(BaseModel):
    gender : Literal["male", "female", "other"]  = Field(..., description = "Gender of the person")

class Person(BaseModel):
    name: str = Field(...) # Required field
    age: int = Field(..., gt=0, lt=120, description= "Age must be greater than 0 and less than 120")
    email : Optional[str] = None # Optional field (required importing optional from typing)
    gender : GenderType = Field(..., description = "Gender of the person")



# field_validator:
# @field_validator
# @classmethod
def validate_name(cls, value):
    return value.title()




p = Person(
    name="Mayuresh",
    age=40,
    gender=GenderType(gender="other")
)

print(p)

