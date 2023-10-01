from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from routes.route import lib
uri = "mongodb+srv://indigg:1pCg2vB6M0fNSHLq@cluster0.lu1eimu.mongodb.net/?retryWrites=true&w=majority"
app = FastAPI()


app.include_router(lib)


client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your db deployment connected successfully")
except Exception as e:
    print(e)


#test api
@app.get('/api')
def getApi():
    return {"status":"Hey I am API for Libraray management System"}


