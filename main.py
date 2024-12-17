from fastapi import FastAPI
from routes.user_routes import user_router
from db.connection import db  # Import the db object

app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint to verify the API is running."""
    return {"message": "Welcome to the MongoDB API!"}

@app.get("/test-db")
async def test_db_connection():
    """Test database connection."""
    try:
        # Fetch collections as a basic test
        collections = db.list_collection_names()
        return {"database": db.name, "collections": collections}
    except Exception as e:
        return {"error": str(e)}

# Register user routes
app.include_router(user_router, prefix="/users", tags=["Users"])
