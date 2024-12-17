from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB URI and database name from environment variables
uri = os.getenv('MONGODB_CONNECTION_STRING')
database_name = os.getenv('DATABASE_NAME')

# Create a new Motor client and connect to the server asynchronously
client = AsyncIOMotorClient(uri)

# Define the database
db = client[database_name]

# List of collections to ensure they exist
collections_to_check = ["Accounts", "Users", "Transactions", "Categories", "Receipts"]

# Check if the collections exist, and create them if not
async def create_collections():
    for collection_name in collections_to_check:
        if collection_name not in await db.list_collection_names():
            # Create the collection explicitly if it doesn't exist
            await db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")

# Call the function to create collections if they don't exist (This needs to be awaited somewhere)
# await create_collections()  # Uncomment if you need to ensure collections exist
