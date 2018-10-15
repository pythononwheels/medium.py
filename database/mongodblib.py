#
# base connection for TinyDB 
#
from medium.config import database
#from pymongo import MongoClient
import pymongo

if not database["mongodb"]["atlas"]:
    # normal mongodb server (local or remote)
    conn_str = "mongodb://" + database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]) + "/"    
    print(" ... setting it up for mongoDB: " + conn_str)
    client = pymongo.MongoClient(database["mongodb"]["host"], database["mongodb"]["port"])
    #db = client[database["mongodb"]["dbname"]]
    #collection=db[database["mongodb"]["dbname"]]

else:
    # go cloudy &  set it up for atlas use
    conn_str=database["mongodb"]["atlas_conn_str"]
    print(" ... setting it up for mongoDB: " + conn_str)
    client = pymongo.MongoClient(conn_str)

db = client[database["mongodb"]["dbname"]]
collection=db[database["mongodb"]["dbname"]]

    
