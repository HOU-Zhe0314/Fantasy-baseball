import logging
import json

from Services.DataServices.RDBDataTable import RDBDataTable

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def t1():

    config_info = {
        "user": "admin",
        "password": "",
        "host": "",
        "db": "HW3_s21"
    }

    r_table = RDBDataTable("recent_people", config_info)
    print("t1: Data table = ", r_table)
    keys = r_table.get_key_columns()
    print("t1: Key columns = ", keys)
    tmp = {"nameLast": "Williams", "birthCity": "San Diego"}
    res = r_table.find_by_template(tmp)

    print("t1: rows = \n", json.dumps(res, indent=2, default=str))


def v1():
    config_info = {
        "user": "admin",
        "password": "",
        "host": "",
        # "dbport": "3306",
        "db": "HW3_s21"
    }

    r_table = RDBDataTable("recent_people", config_info)
    tmp = {"nameLast": "Williams", "birthCity": "San Diego"}
    res = r_table.find_by_template(tmp)

    print("t1: rows = \n", json.dumps(res, indent=2, default=str))


v1()

