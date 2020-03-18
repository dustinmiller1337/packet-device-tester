import pymysql.cursors
import json
from flask import request
from flask import Response


def main():
    token = '222b7564-a0f8-4d90-84a9-5a9f4684b3ea'
    x_auth_token = request.headers['X-Auth-Token']
    try:
        # Validating JSON
        body = json.loads(request.get_data().decode('utf-8'))
    except Exception as e:
        return Response('{"error":"Body must be valid JSON", "raw_error": "' + e.args[0] + '"}',
                        status=404, mimetype='application/json')
    if x_auth_token != token:
        resp = Response('{"Unauthorized": "Check your X-Auth-Token"}')
        resp.status_code = 401
        return resp

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
