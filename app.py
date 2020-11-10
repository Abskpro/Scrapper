#!/usr/bin/env python3 
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

mydb = myclient["uploads"]
mycol = mydb["uploads.files"]

dblist = myclient.list_database_names()

mydict = { "name": "John", "address": "Highway 37" }

if "uploads" in dblist:
    print("the database exists")

# for x in mycol.find():
#     print(x)

x = mycol.insert_one(mydict)
