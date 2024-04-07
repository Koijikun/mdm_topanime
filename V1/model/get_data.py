import argparse
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient

def get_mongo_data():
    parser = argparse.ArgumentParser(description='Create Model')
    parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
    args = parser.parse_args()

    mongo_uri = args.uri
    mongo_db = "projectone"
    mongo_collection = "anime"

    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    collection = db[mongo_collection]

    cursor = collection.find({})
    data = list(cursor)

    df = pd.DataFrame(data)

    return(df)

