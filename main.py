from crawler import Crawler
from mongodb import MongoDb
import json
import utils

__config_file__ = "config.json"


def main():
    configs = load_configs()
    conf_db = configs["database"]
    conf_param = configs["params"]

    crawler = Crawler()
    db = MongoDb(conf_db["address"], conf_db["port"])

    for stock_id in conf_param["stock_ids"]:
        data = crawler.fetch_stock_data(stock_id, conf_param["period"])
        db.append_one(data)


def load_configs():
    with open(__config_file__, 'r') as file_conf:
        configs = json.load(file_conf)
        configs["params"]["period"] = utils.parse_str_array(configs["params"]["period"])
        configs["params"]["stock_ids"] = utils.parse_str_array(configs["params"]["stock_ids"])
    return configs


if __name__ == '__main__':
    main()
