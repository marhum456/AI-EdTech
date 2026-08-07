from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings

# MongoDB Client
client = None

# Database Object
db = None


def connect_to_mongodb():
    """
    Establish connection with MongoDB Atlas
    """

    global client, db

    try:
        # Create MongoDB client
        client = MongoClient(settings.MONGODB_URI)

        # Verify connection
        client.admin.command("ping")

        # Select database
        db = client[settings.DATABASE_NAME]

        print("\n✅ Connected to MongoDB Atlas Successfully!")
        print(f"📂 Database: {settings.DATABASE_NAME}\n")

    except ConnectionFailure as e:
        print("❌ MongoDB Connection Failed")
        print(e)


def close_mongodb_connection():
    """
    Close MongoDB connection
    """

    global client

    if client:
        client.close()
        print("🔒 MongoDB Connection Closed")