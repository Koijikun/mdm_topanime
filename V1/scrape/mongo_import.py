import argparse
import data_scrape as ds
from pymongo import MongoClient


class JsonLinesImporter:

    def __init__(self, data, mongo_uri, batch_size=30, db='projectone', collection='anime'):
        self.data = data
        self.batch_size = batch_size
        self.client = MongoClient(mongo_uri)
        self.db = db
        self.collection = collection

    def save_to_mongodb(self):
        db = self.client[self.db]
        collection = db[self.collection]
        for idx, batch in enumerate(self.split_into_batches()):
            print("inserting batch", idx)
            collection.insert_many(batch)

    def split_into_batches(self):
        for i in range(0, len(self.data), self.batch_size):
            yield self.data[i:i + self.batch_size]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
    parser.add_argument('-c', '--collection', required=True, help="name of the mongodb collection where the tracks should be stored")
    args = parser.parse_args()

    # Create data list
    data = []
    for i in range(len(ds.name)):
        document = {
            "name": ds.name[i],
            "episodes": ds.episodes[i],
            "airing": ds.airing[i],
            "members": ds.members[i],
            "ratings": ds.ratings[i],
            "timespans": ds.timespans[i]
        }
        data.append(document)

    # Initialize importer and save to MongoDB
    importer = JsonLinesImporter(data, collection=args.collection, mongo_uri=args.uri)
    importer.save_to_mongodb()
