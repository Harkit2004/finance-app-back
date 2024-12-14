from db.connection import client
from dotenv import load_dotenv
import os
load_dotenv()

# Define the database
db = client[os.getenv('DATABASE_NAME')]

# Helper to test the connection
def test_database_connection():
    try:
        # Check if the connection works by listing collections
        collections = db.list_collection_names()
        print(f"Connected to database: {db.name}")
        print(f"Existing collections: {collections}")
    except Exception as e:
        print("Failed to connect to the database:", e)

# Run the test when the script is executed directly
if __name__ == "__main__":
    test_database_connection()
