import socket
import json
import time
from crawler.mongodb import MongoDb
from crawler.crawler import Crawler


class Slave:
    __slave_id__ = None
    __server_addr__ = None
    __server_port__ = None

    def __init__(self, slave_id, server_addr, server_port):
        self.__slave_id__ = slave_id
        self.__server_addr__ = server_addr
        self.__server_port__ = int(server_port)

    def run(self, db_addr, db_port):
        while True:
            try:
                stock_id, period = self.__get_task__()
                if stock_id == -1:
                    print("No task to do, will retry after 5 seconds")
                    time.sleep(5)
                    continue
                db = MongoDb(db_addr, db_port)
                crawler = Crawler()
                data = crawler.fetch_stock_data(stock_id, period)
                db.append_one(data)
                self.__done_task__(stock_id)
            except socket.error:
                print("Master is offline, will retry after 5 seconds")
                time.sleep(5)

    def __get_task__(self):
        req = dict(
            id=self.__slave_id__,
            cmd="get"
        )
        msg = self.__send_msg__(req)
        if msg["status"] == "ok":
            return msg["data"]["ids"], msg["data"]["period"]
        return -1, []

    def __done_task__(self, stock_id):
        req = dict(
            id=self.__slave_id__,
            cmd="done",
            data=stock_id
        )
        self.__send_msg__(req)

    def __send_msg__(self, dict_msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_addr__, self.__server_port__))
        sock.send(json.dumps(dict_msg).encode("utf-8"))
        res = json.loads(sock.recv(1024))
        sock.close()
        return res
