from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('MONGODB_CONNECTION_STRING')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect: {e}")

# Define the database
db = client[os.getenv('DATABASE_NAME')]

# Access the 'Users' collection
users_collection = db['Users']  # 'Users' is the name of your MongoDB collection
