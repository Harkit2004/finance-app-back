from fastapi import APIRouter, HTTPException
from models.users import User
from db.connection import db
from bson import ObjectId
from utils.password_utils import hash_password

user_router = APIRouter()

# Create a user
@user_router.post("/")
async def create_user(user: User):
    # Check if email exists
    if await db["Users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password using bcrypt
    user.password = hash_password(user.password)

    # Convert the User model to a dictionary (ensure 'model_dump' is correct)
    user_data = user.dict(exclude={"user_id"})  # Use dict() method from Pydantic models
    result = await db["Users"].insert_one(user_data)
    
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

# Retrieve a user by email
@user_router.get("/{email}")
async def get_user_by_email(email: str):
    try:
        # Search for user by email
        user = await db["Users"].find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert the ObjectId to string for response
        user["user_id"] = str(user["_id"])
        del user["_id"], user["password"]  # Exclude sensitive data
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Retrieve a user by user_id
@user_router.get("/user_id/{user_id}")
async def get_user_by_user_id(user_id: str):
    try:
        # Ensure user_id is a valid ObjectId format
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user_id format")

        # Search for user by user_id
        user = await db["Users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert the ObjectId to string for response
        user["user_id"] = str(user["_id"])
        del user["_id"], user["password"]  # Exclude sensitive data
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
