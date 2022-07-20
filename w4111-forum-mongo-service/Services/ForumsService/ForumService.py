
from Services.DataServices.MongoDBTable import MongoDBTable

class ForumsService():

    default_data_service_info = None

    def __init__(self, forum_name, config_info=None, key_columns=None):

        if config_info is None or config_info.get("db_connect_info", None) is None:

            # self._db_connect_info = {
            #     "HOST": "localhost",
            #     "PORT": 27017,
            #     # "DB": "trials"
            #     "DB": "Forums"
            # }
            self._db_connect_info = {
                    "mongodb_url": "XXXX",
                    "DB": "new_forum"
                }

        else:
            self._db_connect_info = config_info.get("db_connect_info")

        self._data_service = MongoDBTable(
            forum_name,
            self._db_connect_info,
            key_columns=key_columns
        )

    def insert_forum(self, forum_dto):
        res = self._data_service.insert(forum_dto)
        return res

    def find_by_template(self, template, fields=None):
        res = self._data_service.find_by_template(template, fields)
        return res

    def update_by_key(self, key, template=None):
        res = self._data_service.update_by_key(key, template)
        return res