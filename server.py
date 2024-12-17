from db.connection import db
import os

# Helper to test the database connection
def test_database_connection():
    try:
        # Check if the connection works by listing collections
        collections = db.list_collection_names()
        print(f"Connected to database: {db.name}")
        print(f"Existing collections: {collections}")
    except Exception as e:
        print("Failed to connect to the database:", e)

# Optionally run the test when this script is executed directly
if __name__ == "__main__":
    test_database_connection()
