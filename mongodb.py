import pymongo
import utils


class MongoDb:
    __mongo_client__ = None
    __collection__ = None

    def __init__(self, addr, port):
        self.__mongo_client__ = pymongo.MongoClient("mongodb://{0}:{1}/".format(addr, port))
        database = self.__mongo_client__["PyDataMining"]
        self.__collection__ = database["StockData"]

    def __del__(self):
        self.__mongo_client__.close()

    def put_one(self, data):
        query = self.__collection__.find_one({"_id": data['_id']})
        if query is None:
            return self.__collection__.insert_one(data)
        return None

    def append_one(self, data):
        query = self.__collection__.find_one({"_id": data['_id']})
        if query is None:
            return self.__collection__.insert_one(data)
        query["data"] = utils.combine_dict_list(query["data"], data["data"])
        return self.__collection__.update_one({"_id": data['_id']}, {"$set": query})
