import pymongo
import utils

__host_addr__ = "localhost"
__host_port__ = 27017


class MongoDb:
    __collection__ = None

    def __init__(self, addr=__host_addr__, port=__host_port__):
        mongo_client = pymongo.MongoClient("mongodb://{0}:{1}/".format(addr, port))
        database = mongo_client["PyDataMining"]
        self.__collection__ =  database["StockData"]

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
