import json

from Services.DataServices.MongoDBTable import MongoDBTable
from Services.ForumsService.ForumService import ForumsService


c_info = {
    "db_connect_info": {
        "HOST": "localhost",
        "PORT": 27017,
        "DB": "new_forum"
    }
}

t_info = {
    "db_connect_info": {
        "HOST": "localhost",
        "PORT": 27017,
        "DB": "HW4"
    }
}

o_info = {
    "db_connect_info": {
        "HOST": "localhost",
        "PORT": 27017,
        "DB": "classic_models"
    }
}


def t1():
    mt = MongoDBTable("got_forums", c_info["db_connect_info"], key_columns=["forum_id"])
    forum_dto = {
        "forum_id": "1234",
        "forum_name": "Cool"
    }
    fs = ForumsService("GotForums", c_info)
    fs.insert_forum(forum_dto)


def t2():
    mt = MongoDBTable("trials", t_info["db_connect_info"], key_columns=["post_id"])
    fs = ForumsService("trials", c_info, key_columns=["post_id"])

    # res = mt.find_by_template({'post_id': '00014f99-a9cc-47ba-9370-a26936aa44f5'},
    #                            ["email", "content"])
    res = mt.find_by_template({'post_id': '00014f99-a9cc-47ba-9370-a26936aa44f5'},
                                ["length"])
    for r in res:
        print(json.dumps(r, indent=2, default=str))


def t3():
    mt = MongoDBTable("trials", t_info["db_connect_info"], key_columns=["post_id"])
    fs = ForumsService("trials", t_info, key_columns=["post_id"])

    res = fs.find_by_template({'post_id': "00014f99-a9cc-47ba-9370-a26936aa44f5"})
    print(res)
    for r in res:
        print(json.dumps(r, indent=2, default=str))


# t1()
# t2()
# t3()


def t():
    mt = MongoDBTable("trials", t_info["db_connect_info"], key_columns=["_id"])
    fs = ForumsService("forum", c_info, key_columns=["post_id"])

    # res = mt.find_by_template({'post_id': '00014f99-a9cc-47ba-9370-a26936aa44f5'},
    #                            ["email", "content"])
    res = mt.find_by_template({'length': '10000'},
                              ["length"])
    print(mt)
    for r in res:
        print(json.dumps(r, indent=2, default=str))

# t()
#
# mt = MongoDBTable("trials", t_info["db_connect_info"], key_columns=["post_id"])
# print(mt._collection)

