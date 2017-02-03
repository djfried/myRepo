import pymongo

client = pymongo.MongoClient("mongodb://doug:pwd@35.162.119.179/myDb") # defaults to port 27017

db = client.myDb

# print the number of documents in a collection
print db.mycol.count()