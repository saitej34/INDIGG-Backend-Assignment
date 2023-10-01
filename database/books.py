from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://indigg:1pCg2vB6M0fNSHLq@cluster0.lu1eimu.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.indigg

books = db["Books"]

