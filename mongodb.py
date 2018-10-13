import pymongo

__host_addr__ = "localhost"
__host_port__ = 27017


class MongoDb:
    __collection__ = None

    def __init__(self, addr=__host_addr__, port=__host_port__):
        mongo_client = pymongo.MongoClient("mongodb://{0}:{1}/".format(addr, port))
        database = mongo_client["PyDataMining"]
        self.__collection__ =  database["StockData"]

    def put_one(self, data):
        self.__collection__.insert_one(data)
