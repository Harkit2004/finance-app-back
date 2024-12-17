from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId  # This is necessary for MongoDB's ObjectId

# Custom function to convert MongoDB's ObjectId to a string
def str_objectid(v):
    if isinstance(v, ObjectId):
        return str(v)
    return v

class User(BaseModel):
    user_id: Optional[str] = Field(default_factory=str)  # Will be populated by MongoDB's _id
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    verified: bool = False  # Default to not verified

    class Config:
        # Set the ORM mode so that Pydantic can handle MongoDB ObjectId
        orm_mode = True
        # Custom example schema
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "verified": False
            }
        }

    # Make sure to handle the ObjectId conversion to string
    @classmethod
    def from_mongo(cls, data):
        """Convert MongoDB document to Pydantic model."""
        data["user_id"] = str_objectid(data["_id"])
        return cls(**data)
    
    def to_mongo(self):
        """Convert Pydantic model to MongoDB document."""
        data = self.model_dump()  # Replacing dict() with model_dump()
        data["_id"] = data.get("user_id")  # MongoDB automatically handles _id
        return data
