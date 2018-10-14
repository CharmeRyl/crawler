import sys
import getopt
import json
from crawler import utils
import time
from crawler.master import Master
from crawler.slave import Slave

__config_file__ = "config-distributed.json"


def main(argv):
    run_type = parse_args(argv)
    configs = load_configs()
    if run_type == "master":
        conf_master = configs["master"]
        conf_server = conf_master["server"]
        conf_params = conf_master["params"]
        master = Master(conf_server["address"], conf_server["port"])
        master.put_tasks(conf_params["stock_ids"], conf_params["period"])
        master.dispatch()
    elif run_type == "slave":
        conf_slave = configs["slave"]
        conf_host = conf_slave["host"]
        conf_database = conf_slave["database"]
        slave = Slave(int(time.time()), conf_host["address"], conf_host["port"])
        slave.run(conf_database["address"], conf_database["port"])


def parse_args(argv):
    opts, args = getopt.getopt(argv[1:], "", ["master", "slave"])
    run_type = "slave"
    for opt_key, opt_value in opts:
        if opt_key == "--master":
            run_type = "master"
            continue
        if opt_key == "--slave":
            run_type = "slave"
            continue
    return run_type


def load_configs():
    with open(__config_file__, 'r') as file_conf:
        configs = json.load(file_conf)
        configs["master"]["params"]["period"] = \
            utils.parse_str_array(configs["master"]["params"]["period"])
        configs["master"]["params"]["stock_ids"] = \
            utils.parse_str_array(configs["master"]["params"]["stock_ids"])
    return configs


if __name__ == '__main__':
    main(sys.argv)
