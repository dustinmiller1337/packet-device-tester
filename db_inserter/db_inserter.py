import pymysql.cursors
import json
from http import client as httplib
from flask import request
from flask import Response


def do_request(action, host, relative_url, headers, body):
    conn = httplib.HTTPSConnection(host)
    if body == "":
        the_json = body
    else:
        the_json = json.JSONEncoder().encode(body)
    conn.request(action, relative_url, the_json, headers)
    response = conn.getresponse()
    return conn, response


def authenticate(x_auth_token, x_consumer_token, x_packet_staff):
    headers = {
        "Accept": "application/json",
        "X-Auth-Token": x_auth_token,
        "X-Consumer-Token": x_consumer_token,
        "X-Packet-Staff": x_packet_staff
    }
    try:
        _, response = do_request("GET", "api.packet.net", "/staff/labels", headers, "")
        if response.status != 200 and response.status != 201:
            return False
    except ValueError:
        return False

    return True


def main():
    try:
        body = json.loads(request.get_data().decode('utf-8'))
    except Exception as e:
        return Response('{"error":"Body must be valid JSON", "raw_error": "' + e.args[0] + '"}',
                        status=404, mimetype='application/json')
    try:
        x_auth_token = request.headers['X-Auth-Token']
        x_consumer_token = request.headers['X-Consumer-Token']
        x_packet_staff = request.headers['X-Packet-Staff']
        authed = authenticate(x_auth_token, x_consumer_token, x_packet_staff)
    except Exception as e:
        return Response('{"Unauthorized": "Check your X-Auth-Token, X-Consumer-Token, & X-Packet-Staff", '
                        '"raw_error": "' + e.args[0] + '"}', status=401, mimetype='application/json')
    if authed is False:
        return Response('{"Unauthorized": "Check your X-Auth-Token, X-Consumer-Token, & X-Packet-Staff"}',
                        status=401, mimetype='application/json')

    connection = pymysql.connect(host='mysql.stats.svc.us-central-1.local',
                                 user='root',
                                 password='hhQYa2wPas',
                                 db='stats',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "INSERT INTO `stats` (`uuid`, `state`, `hostname`, `facility`, `plan`, `operating_system`, " \
              "`created_at`, `updated_at`, `creation_duration`) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (body['uuid'], body['state'], body['hostname'], body['facility'], body['plan'],
                             body['operating_system'], body['created_at'], body['updated_at'],
                             body['creation_duration']))
        connection.commit()
    resp = Response('{"Success": "We made an insert!"}')
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    main()
