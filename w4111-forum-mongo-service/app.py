
import json
import uuid

import logging
from datetime import datetime

from flask import Flask, Response
from flask import Flask, request, render_template, jsonify

# rest_utils provides simplification and isolation for interacting with Flask APIs and object,
# specifically the request object.
import utils.rest_utils as rest_utils

from Services.ForumsService.ForumService import ForumsService


# c_info = {
#     "db_connect_info": {
#         "HOST": "localhost",
#         "PORT": 27017,
#         "DB": "new_forum"
#     }
# }
c_info = {
    "db_connect_info": {
        "mongodb_url": "XXXX",
        "DB": "new_forum"
    }
}

_service_factory = {
    "forum": ForumsService("forum", c_info, key_columns=["post_id"])
}


# Given the "resource" return the implementing class.
def _get_service_by_name(s_name):
    result = _service_factory.get(s_name, None)
    return result


#
# Create the Flask application object.
app = Flask(__name__)


# This path simply echoes to check that the app is working.
# The path is /health REST request, and produces a response indicating what
# the parameters, headers, etc. are.
@app.route("/api/demo/<parameter1>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/api/demo/", methods=["GET", "POST", "PUT", "DELETE"])
def demo(parameter1=None):

    inputs = rest_utils.RESTContext(request, {"parameter1": parameter1})

    r_json = inputs.to_json()
    msg = {
        "/demo received the following inputs": inputs.to_json()
    }
    print("/api/demo/<parameter> received/returned:\n", msg)

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp


@app.route("/api/forum/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    """
    Returns a post with the specified post_id

    """
    try:
        inputs = rest_utils.RESTContext(request, {"parameter1": None})
        rest_utils.log_request("get_post_by_id", inputs)

        service = _get_service_by_name("forum")

        if service is not None:
            rsp = service.find_by_template({"post_id": post_id})
            rsp = json.dumps(rsp, default=str)
            rsp = Response(rsp, status=200, content_type="application/JSON")
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    except Exception as e:
        print("/api/" + "some weird path" + "/count, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/forum", methods=["GET", "POST"])
def get_post_by_id_forum():

    try:
        inputs = rest_utils.RESTContext(request, {"parameter1": None})
        rest_utils.log_request("get_post_by_id", inputs)
        template = inputs.args
        service = _get_service_by_name("forum")
        if inputs.method == "GET":
            if service is not None:
                rsp = service.find_by_template(template)
                rsp = json.dumps(rsp, default=str)
                rsp = Response(rsp, status=200, content_type="application/JSON")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":
            if service is not None:
                # inputs.data["post_id"] = uuid.uuid4().hex
                inputs.data["_id"] = uuid.uuid4().hex
                res = service.insert_forum(inputs.data)

                if res is not None:
                    # key = res.values())
                    headers = {"location": "/api/" + "forum"}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    except Exception as e:

        print("/api/" + "some weird path" + "/count, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/forum/<post_id>/comments", methods=["GET", "POST"])
def get_post_forum_comments(post_id):

    try:
        inputs = rest_utils.RESTContext(request, {"parameter1": None})
        rest_utils.log_request("get_post_by_id", inputs)
        template = inputs.args

        service = _get_service_by_name("forum")
        # Returns the comments relative to the post matching a specific template.
        if inputs.method == "GET":
            # template["post_id"] = post_id
            if service is not None:
                rsp = service.find_by_template({"post_id": post_id})
                rsp = rsp[0]['children']
                res = []
                for r in rsp:
                    flag = True

                    # template is used to filter comments
                    for key in template.keys():
                        if key not in r:
                            flag = False
                        else:
                            if key == "tags":
                                if template[key] in r["tags"]:
                                    continue
                            if template[key] != r[key]:
                                flag = False
                    if flag:
                        res.append(r)

                rsp = json.dumps(res, default=str)
                rsp = Response(rsp, status=200, content_type="application/JSON")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":
            if service is not None:
                # inputs.data["comment_id"] = uuid.uuid4().hex
                inputs.data["parent_id"] = post_id
                # res = service.insert_forum(inputs.data)
                # origin_data = rsp = service.find_by_template({"post_id":post_id})
                # children = origin_data[0]['children']
                # children.append(inputs.data)
                template = {"$push": {"children": inputs.data}}

                # template['children'] = children
                rsp = service.update_by_key([post_id], template)
                if rsp is not None:
                    # key = res.values())
                    headers = {"location": "/api/" + "forum"}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    except Exception as e:

        print("/api/" + "some weird path" + "/count, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/forum/<post_id>/comments/<comment_id>", methods=["GET"])
def get_post_by_id_forum_comments(post_id, comment_id):

    try:
        inputs = rest_utils.RESTContext(request, {"parameter1": None})
        rest_utils.log_request("get_post_by_id", inputs)
        template = inputs.args

        service = _get_service_by_name("forum")
        if inputs.method == "GET":
            template["post_id"] = post_id
            if service is not None:
                # template is used for filter post here
                rsp = service.find_by_template(template)
                rsp = rsp[0]['children']
                res = []
                for r in rsp:
                    if "comment_id" in r:
                        if r["comment_id"] == comment_id:
                            res.append(r)

                rsp = json.dumps(res, default=str)
                rsp = Response(rsp, status=200, content_type="application/JSON")

            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    except Exception as e:

        print("/api/" + "some weird path" + "/count, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


if __name__ == '__main__':
    # host, port = ctx.get_host_and_port()

    app.run(host="0.0.0.0", port=5001, debug=True)
