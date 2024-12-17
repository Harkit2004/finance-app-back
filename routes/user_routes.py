from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.users import User
from db.connection import users_collection
from utils.password_utils import hash_password

user_router = APIRouter()

# Create a user
@user_router.post("/")
async def create_user(user: User):
    # Check if email exists
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    user.password = hash_password(user.password)

    # Insert into MongoDB
    user_data = user.model_dump(exclude={"user_id"})  # Use model_dump() instead of dict()
    result = await users_collection.insert_one(user_data)
    
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

# Retrieve a user by ID
@user_router.get("/{user_id}")
async def get_user(user_id: str):
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user["user_id"] = str(user["_id"])
        del user["_id"], user["password"]  # Exclude sensitive data
        return user
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
