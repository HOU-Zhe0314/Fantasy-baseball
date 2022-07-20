import json

import logging

from datetime import datetime

from flask import Flask, Response, ctx
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

import utils.rest_utils as rest_utils

from Services.DataServices.Neo4JDataTable import HW3Graph as HW3Graph
from Services.FantasyService.FantasyTeam import FantasyTeam as FantasyTeam
from Services.FantasyService.FantasyManager import FantasyManager as FantasyManager
from Services.FantasyService.FantasyPlayer import FantasyPlayer as FantasyPlayer
from Services.FantasyService.FantasyLeague import FantasyLeague as FantasyLeague

# from Services.LahmanService.PersonService import PersonService as PersonService
# from Services.LahmanService.TeamService import TeamService as TeamService

#
_service_factory = {
    "fantasy_player": FantasyPlayer({
        "db_name": "HW3_s21",
        "table_name": "fantasy_player",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["playerID"]
    }),
    "fantasy_league": FantasyLeague({
        "db_name": "HW3_s21",
        "table_name": "fantasy_league",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["leagueID"]
    }),
    "fantasy_team": FantasyTeam({
        "db_name": "HW3_s21",
        "table_name": "fantasy_team",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["teamID"]
    }),
    "fantasy_manager": FantasyManager({
        "db_name": "HW3_s21",
        "table_name": "fantasy_manager",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["uni"]
    }),
    "person": PersonService({
        "db_name": "HW3_s21",
        "table_name": "people",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["playerID"]
    }),
    "teams": TeamService({
        "db_name": "HW3_s21",
        "table_name": "recent_teams",
        "db_connect_info": {
            "host": "",
            "user": "admin",
            "password": "dbuserdbuser",
            "db": "HW3_s21"
        },
        "key_columns": ["teamID", "yearID"]
    })

}


# Given the "resource"
def _get_service_by_name(s_name):
    result = _service_factory.get(s_name, None)
    return result


app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp


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


@app.route("/api/<resource>/count", methods=["GET"])
def get_resource_count(resource):
    """
    Currently not implemented. Need to revise.
    """
    rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp

    """
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_count", inputs)

        service = _get_service_by_name(resource)

        if service is not None:
            res = service.get_count()
            if res is not None:
                res = {"count": res}
                res = json.dumps(res, default=str)
                rsp = Response(res, status=200, content_type="application/JSON")
            else:
                rsp = Response("NOT FOUND", status=404, content_type="text/plain")
        else:
            rsp = Response("NOT FOUND", status=404)

    except Exception as e:
      
        print("/api/" + resource + "/count, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp
    """


@app.route("/api/people/<player_id>/career_batting", methods=["GET"])
def get_career_batting(player_id):
    rsp = Response("NOT IMPLEMENTED", status=501)
    return rsp

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_count", inputs)

        service = _get_service_by_name("player_performance")

        if service is not None:
            if inputs.method == "GET":
                res = service.get_career_batting(player_id)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")
            else:
                rsp = Response("NOT IMPLEMENTED", status=501)
        else:
            rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    except Exception as e:

        print("/api/players/<player_id>/career_batting, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/<resource>", methods=["GET", "POST"])
def get_resource_by_query(resource):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name(resource)

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":
            service = _get_service_by_name(resource)
            if service is not None:
                res = service.create(inputs.data)
                if res is not None:
                    # convert all elements in the list to str
                    vals = []
                    for i in res.values():
                        if type(i) != str:
                            vals.append(str(i))
                        else:
                            vals.append(i)
                    key = "_".join(vals)
                    headers = {"location": "/api/" + resource + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/<resource>, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/<resource>/<resource_id>", methods=["GET", "PUT", "DELETE"])
def resource_by_id(resource, resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("resource_by_id", inputs)

        resource_key_columns = rest_utils.split_key_string(resource_id)

        if inputs.method == "GET":
            service = _get_service_by_name(resource)
            if service is not None:
                res = service.find_by_primary_key(resource_key_columns, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":
            service = _get_service_by_name(resource)
            if service is not None:
                res = service.update(resource_key_columns, inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":
            service = _get_service_by_name(resource)
            if service is not None:
                res = service.delete_by_key(resource_key_columns)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/person, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/people/search/<pattern>", methods=["GET"])
def get_person_by_pattern(pattern):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_person_by_pattern", inputs)

        # resource_key_columns = rest_utils.split_key_string(resource_id)

        if inputs.method == "GET":
            service = _get_service_by_name("people")
            if service is not None:
                # implementation not finished
                res = service.get_by_pattern("nameLast", pattern)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/people/pattern, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyPlayer", methods=['GET', 'POST'])
def do_fantasy_player():
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":
            template = inputs.args

            service = _get_service_by_name("fantasy_player")
            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":

            service = _get_service_by_name("fantasy_player")

            if service is not None:
                res = service.create(inputs.data)
                if res is not None:
                    vals = []
                    for i in res.values():
                        if type(i) != str:
                            vals.append(str(i))
                        else:
                            vals.append(i)
                    key = "_".join(vals)
                    headers = {"location": "/api/" + "fantasy_player" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyPlayer, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyTeam", methods=['GET', 'POST'])
def do_fantasy_team():
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":

            service = _get_service_by_name("fantasy_team")
            if service is not None:
                res = service.create(inputs.data)
                if res is not None:
                    key = "_".join(res.values())
                    headers = {"location": "/api/" + "fantasy_team" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyTeam, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager", methods=['GET', 'POST'])
def do_fantasy_manager():
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_manager")
            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":
            service = _get_service_by_name("fantasy_manager")
            if service is not None:
                res = service.create(inputs.data)
                if res is not None:
                    key = "_".join(res.values())
                    headers = {"location": "/api/" + "fantasy_manager" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)

                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyLeague", methods=['GET', 'POST'])
def do_fantasy_league():
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_league")

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "POST":

            service = _get_service_by_name("fantasy_league")
            if service is not None:
                res = service.create(inputs.data)
                if res is not None:
                    key = "_".join(res.values())
                    headers = {"location": "/api/" + "fantasy_league" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)

                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyLeague, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyTeam/<resource_id>/FantasyPlayer", methods=['GET', 'POST'])
def do_fantasy_team_player(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get all players for a particular team
        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_player")
            template['teamID'] = resource_id
            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        # add a player in a particular team
        elif inputs.method == "POST":

            service = _get_service_by_name("fantasy_player")

            if service is not None:
                inputs.data['teamID'] = resource_id
                res = service.create(inputs.data)
                if res is not None:
                    key = "_".join(res.values())
                    headers = {"location": "/api/" + "fantasy_player" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyTeam/<resource_id>/FantasyPlayer, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyLeague/<resource_id>/FantasyTeam", methods=['GET', 'POST'])
def do_fantasy_league_team(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get all teams of a particular league
        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            template['leagueID'] = resource_id
            if service is not None:
                res = service.find_by_template(template, inputs.fields)

                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        # add a team for a particular league
        elif inputs.method == "POST":

            service = _get_service_by_name("fantasy_team")

            if service is not None:
                inputs.data['leagueID'] = resource_id
                res = service.create(inputs.data)
                if res is not None:
                    key = "_".join(res.values())
                    headers = {"location": "/api/" + "fantasy_team" + "/" + key}
                    rsp = Response("CREATED", status=201, content_type="text/plain", headers=headers)
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyLeague/<resource_id>/FantasyTeam, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyTeam/<resource_id>", methods=['GET', 'PUT', 'DELETE'])
def do_fantasy_team_by_source(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get info of a particular team
        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            template['teamID'] = resource_id

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":

            service = _get_service_by_name('fantasy_team')
            # resource_key_columns = rest_utils.split_key_string(resource_id)
            if service is not None:
                res = service.update([resource_id], inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            template['teamID'] = resource_id

            if service is not None:
                res = service.delete(template)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyTeam, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyTeam/<resource_id1>/FantasyPlayer/<resource_id2>", methods=['GET', 'PUT', 'DELETE'])
def do_fantasy_team_player_by_source(resource_id1, resource_id2):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get info of a particular player from a particular team
        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_player")
            template['teamID'] = resource_id1
            template['playerID'] = resource_id2

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":

            service = _get_service_by_name('fantasy_player')
            # resource_key_columns = rest_utils.split_key_string(resource_id)
            if service is not None:
                tup = ('teamID', resource_id1)
                res = service.update_by_template([resource_id2], inputs.data, tup)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":

            template = inputs.args
            service = _get_service_by_name("fantasy_player")
            template['teamID'] = resource_id1
            template['playerID'] = resource_id2

            if service is not None:
                res = service.delete(template)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyTeam/<resource_id1>/FantasyPlayer/<resource_id2>, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager/<resource_id>", methods=['GET', 'PUT', 'DELETE'])
def do_fantasy_manager_by_source(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_manager")
            template['uni'] = resource_id

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":

            service = _get_service_by_name('fantasy_manager')
            # resource_key_columns = rest_utils.split_key_string(resource_id)
            if service is not None:
                res = service.update([resource_id], inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":

            template = inputs.args
            service = _get_service_by_name("fantasy_manager")
            template['uni'] = resource_id

            if service is not None:
                res = service.delete(template)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager/<resource_id1>/FantasyTeam/<resource_id2>", methods=['GET', 'PUT', 'DELETE'])
def do_fantasy_manager_team_by_source(resource_id1, resource_id2):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        # DFF TODO Change this to a DTO/object with properties from a dict.
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            template['uni'] = resource_id1
            template['teamID'] = resource_id2

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":

            service = _get_service_by_name('fantasy_team')
            # resource_key_columns = rest_utils.split_key_string(resource_id)
            if service is not None:
                tup = ('uni', resource_id1)
                res = service.update_by_template([resource_id2], inputs.data, tup)
                # res = service.update([resource_id2], inputs.data)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":

            template = inputs.args
            service = _get_service_by_name("fantasy_team")
            template['uni'] = resource_id1
            template['teamID'] = resource_id2

            if service is not None:
                res = service.delete(template)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager/<resource_id1>/FantasyTeam/<resource_id2>, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager/<resource_id1>/FantasyLeague/<resource_id2>", methods=['GET', 'PUT', 'DELETE'])
def do_fantasy_manager_league_by_source(resource_id1, resource_id2):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        if inputs.method == "GET":

            template = inputs.args
            service = _get_service_by_name("fantasy_league")
            template['adminID'] = resource_id1
            template['leagueID'] = resource_id2

            if service is not None:
                res = service.find_by_template(template, inputs.fields)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "PUT":

            service = _get_service_by_name('fantasy_league')
            # resource_key_columns = rest_utils.split_key_string(resource_id)
            if service is not None:
                tup = ('adminID', resource_id1)
                res = service.update_by_template([resource_id2], inputs.data, tup)
                if res is not None:
                    rsp = Response("OK", status=200, content_type="text/plain")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        elif inputs.method == "DELETE":

            template = inputs.args
            service = _get_service_by_name("fantasy_league")
            template['adminID'] = resource_id1
            template['leagueID'] = resource_id2

            if service is not None:
                res = service.delete(template)
                if res is not None:
                    res = json.dumps(res, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager/<resource_id1>/FantasyLeague/<resource_id2>, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager/<resource_id>/Follows", methods=['GET', 'POST'])
def do_fantasy_manager_follows(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get the teams that are followed by the manager
        if inputs.method == "GET":
            service = HW3Graph()
            if service is not None:
                q = "match (m:manager) -[:follows] -> (t:team) where m.uni = '" + resource_id + "' return t"
                res = service.run_q(q, args=None)

                tmp = []
                for r in res:
                    tmp.append(r)
                if res is not None:
                    res = json.dumps(tmp, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        # create a node (label: team), create a 'follow' relationship
        elif inputs.method == "POST":

            service = HW3Graph()

            if service is not None:
                q = "create (t:team {teamName: '" + inputs.data['teamName']
                q = q + "', uni: '" + resource_id
                q = q + "', leagueID: '" + inputs.data['leagueID']
                q = q + "',  teamID: '" + inputs.data['teamID'] + "'})"
                res = service.run_q(q, args=None)

                q = "MATCH (m:manager), (t:team) where m.uni = '" + resource_id + \
                    "' and t.teamID = '" + inputs.data['teamID'] + "' CREATE (m)-[r:follows]->(t)"
                res = service.run_q(q, args=None)
                if res is not None:
                    rsp = Response("CREATED", status=201, content_type="text/plain")
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager/<resource_id>/Follows e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route("/api/FantasyManager/<resource_id>/Likes", methods=['GET', 'POST'])
def do_fantasy_manager_likes(resource_id):
    rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
    try:

        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_resource_by_query", inputs)

        # get players the manager likes
        if inputs.method == "GET":
            service = HW3Graph()
            if service is not None:
                q = "match (m:manager) -[:likes] -> (p:player) where m.uni = '" + resource_id + "' return p"
                res = service.run_q(q, args=None)
                tmp = []
                for r in res:
                    tmp.append(r)
                if res is not None:
                    res = json.dumps(tmp, default=str)
                    rsp = Response(res, status=200, content_type="application/JSON")
                else:
                    rsp = Response("NOT FOUND", status=404, content_type="text/plain")

        # create player node
        elif inputs.method == "POST":

            service = HW3Graph()

            if service is not None:
                q = "create (p:player {teamID: '" + inputs.data['teamID'] + "', playerID: '" + inputs.data[
                    'playerID'] + "'})"

                res = service.run_q(q, args=None)

                q = "MATCH (m:manager), (p:player) where m.uni = '" + resource_id + \
                    "' and p.playerID = '" + inputs.data['playerID'] + "' CREATE (m)-[r:likes]->(p)"
                res = service.run_q(q, args=None)
                if res is not None:
                    rsp = Response("CREATED", status=201, content_type="text/plain")
                else:
                    rsp = Response("UNPROCESSABLE ENTITY", status=422, content_type="text/plain")

        else:
            rsp = Response("NOT IMPLEMENTED", status=501)

    except Exception as e:

        print("/api/FantasyManager/<resource_id>/Follows e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# q = "create (m:player {teamID: '" + inputs.data['teamID:'] + "', playerID: '"+ inputs.data['playerID:'] + "'})"
#                res = service.run_q(q, args=None)
#                q = "MATCH (m:manager), (p:player) CREATE (m)-[r:likes]->(p)"


if __name__ == '__main__':
    # host, port = ctx.get_host_and_port()

    # app.run(host="0.0.0.0", port=5001, debug = True)
    app.run(debug=True)
