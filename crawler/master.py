import socket
import json

__MAX_SLAVES__ = 50


class Master:
    __tasks_waiting__ = None
    __tasks_pending__ = None
    __tasks_period__ = None
    __socket__ = None

    def __init__(self, addr, port):
        self.__tasks_waiting__ = list()
        self.__tasks_pending__ = list()
        self.__tasks_period__ = list()
        self.__socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket__.bind((addr, int(port)))
        self.__socket__.listen(__MAX_SLAVES__)

    def __del__(self):
        # TODO: save(task_queue)
        self.__socket__.close()

    def dispatch(self):
        print("Waiting for slaves...")
        while True:
            if self.__is_tasks_list_empty():
                print("All tasks done!")
                break
            conn, addr = self.__socket__.accept()
            try:
                conn.settimeout(10)
                msg = json.loads(conn.recv(1024).decode("utf-8"))
                if msg["cmd"] == "get":
                    res = dict(
                        status="ok",
                        data=dict(
                            ids=self.__get_task__(),
                            period=self.__tasks_period__
                        )
                    )
                    conn.send(json.dumps(res).encode("utf-8"))
                    print("Dispatch stock {0} to slave {1}".format(res["data"], msg["id"]))
                elif msg["cmd"] == "done":
                    self.__done_task__(msg["data"])
                    res = dict(
                        status="ok"
                    )
                    conn.send(json.dumps(res).encode("utf-8"))
                    print("Slave {0} done fetching stock {1}".format(msg["id"], msg["data"]))
            except socket.timeout:
                print("Connection timeout")
            conn.close()

    def put_tasks(self, stock_ids, period):
        self.__tasks_waiting__.extend(stock_ids)
        self.__tasks_period__.extend(period)

    def __get_task__(self):
        if len(self.__tasks_waiting__) == 0:
            return -1
        stock_id = self.__tasks_waiting__.pop()
        self.__tasks_pending__.append(stock_id)
        return stock_id

    def __done_task__(self, stock_id):
        self.__tasks_pending__.remove(int(stock_id))

    def __is_tasks_list_empty(self):
        if len(self.__tasks_waiting__) + len(self.__tasks_pending__) == 0:
            return True
        return False
