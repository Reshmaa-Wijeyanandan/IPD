from pymongo import MongoClient

MONGO_URI = "mongodb+srv://reshiwijey:nJB4xyVD372cc4Yg@cluster0.aeqqp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["EmotiGlucoDB"]
    print("MongoDB Connected Successfully!")
    print("Collections:", db.list_collection_names())  # List existing collections
except Exception as e:
    print("Connection Failed:", e)
