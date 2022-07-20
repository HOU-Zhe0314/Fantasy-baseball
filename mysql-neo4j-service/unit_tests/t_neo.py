import json

from Services.DataServices.Neo4JDataTable import HW3Graph as HW3Graph


def t1():
    hw3g = HW3Graph()


def t2():
    q = "match (n:Person {name: 'Tom Hanks'}) return n"
    hw3g = HW3Graph()
    res = hw3g.run_q(q, args=None)
    print("t2 -- res =", res)

    tmp = {"label": "Person", "template": {"name": "Tom Hanks"}}
    res2 = hw3g.find_nodes_by_template(tmp)
    print("t2 -- res =", res2)


def my_t2():
    q = "match (n:manager {uni: 'hf2431'}) return n"
    hw3g = HW3Graph()
    res = hw3g.run_q(q, args=None)
    print("t2 -- res =", res)

    tmp = {"label": "manager", "template": {"uni": "hf2431"}}
    res2 = hw3g.find_nodes_by_template(tmp)
    print("t2 -- res =", res2)


my_t2()


def my_t(resource_id):
    q = "match (m:manager) -[:follows] - (t:team) where m.uni = '" + resource_id + "' return t"
    hw3g = HW3Graph()
    res = hw3g.run_q(q, args=None)
    res = json.dumps(res, default=str)
    rsp = Response(res, status=200, content_type="application/JSON")
    return res._result


# print(my_t("hf2431"))


def t3():
    hw3g = HW3Graph()
    res = hw3g.create_node(label="Person", name="Fred Astaire", nconst='nm0000001', firstName='Fred',
                           lastName='Astaire')
    print("t3 -- res = ", res)

# t2()
# t3()
