from sanic import response
from auth import check_token,jsonify
import jwt

async def addsensor(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]      
        data = request.json 
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            try:
                if (data["name"] and data["unit"] and str(data["id_hardware"]).isdigit() and str(data["id_node"]).isdigit()):
                    sql = """
                        SELECT hardware.type from hardware WHERE id_hardware = {0};
                        """.format(str(data["id_hardware"]))
                    rows = await conn.fetch(sql)
                    if(bool(rows)):
                        res_hardware = jsonify(rows)[0]
                        if(res_hardware["type"] == "Sensor"):
                            valid = 1
                        else :
                            return response.json({"description": "Bad Request",'status': 400, "message": "Hardware type not match, type should be sensor"}, status=400)                               
                    else:   
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware not found"}, status=400)                           
                    sql = """
                        SELECT id_user from node where id_node = {0} 
                    """.format(data["id_node"])
                    try:
                        user = jsonify(await conn.fetch(sql))[0]["id_user"]                    
                    except:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                                   
                    if(id_user == user or authtoken["is_admin"] ==1 ):
                        valid = 1
                    else:
                        return response.json({"description": "Forbidden",'status': 403, "message": "You can't user other user's node"}, status=403)                                                              
                else:
                    return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
            except:
                return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
            sql = """
                INSERT into sensor (name, unit, id_hardware, id_node) values ('{0}','{1}',{2},{3})
            """.format(data["name"], data["unit"], str(data["id_hardware"]), str(data["id_node"]))
            rows = await conn.execute(sql)
            return response.json({"description": "Created",'status': 201, 'message':'Successfully add new sensor'}, status=201)        
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def listsensor(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]     
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT sensor.id_sensor, sensor.name, sensor.unit, sensor.id_hardware, sensor.id_node from sensor 
                    left join node on sensor.id_node = node.id_node 
                    where node.id_user = {0}; 
                '''.format(id_user)
            rows = await conn.fetch(sql)
            return response.json({'status': 200, 'data': jsonify(rows)}, status=200)
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def detailsensor(request, id_sensor: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]       
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT node.id_user from node Inner join sensor on node.id_node = sensor.id_node 
                    WHERE sensor.id_sensor = {0}; 
                '''.format(str(id_sensor))
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    sql = '''
                            SELECT * from sensor 
                            where id_sensor = {0}; 
                        '''.format(id_sensor)
                    rowsFinal = jsonify(await conn.fetch(sql))[0]
                    sql = '''
                            SELECT channel.time, channel.value from channel
                            left join sensor on sensor.id_sensor = channel.id_sensor
                            where sensor.id_sensor = {0}; 
                        '''.format(id_sensor)
                    x = await conn.fetch(sql)
                    if(bool(x)):
                        y = jsonify(x)
                        for i in y:
                            i["time"] = i["time"].isoformat()
                        rowsFinal["channel"] = y
                    else:
                        rowsFinal["channel"] = "{}"
                    return response.json({'status': 200, 'data': rowsFinal}, status=200)
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "You can't see other user's sensor"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id sensor not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def editsensor(request, id_sensor: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]    
        data = request.json 
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT node.id_user from node Inner join sensor on node.id_node = sensor.id_node 
                    WHERE sensor.id_sensor = {0}; 
                '''.format(str(id_sensor))
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    try:
                        if (data["name"] and data["unit"]):
                            valid = 1
                        else:
                            return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
                    except:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
                    sql = """
                        UPDATE sensor
                        SET name = '{0}', unit = '{1}' 
                        WHERE id_sensor = {2};
                    """.format(data["name"], data["unit"], str(id_sensor))
                    rows = await conn.execute(sql)
                    return response.json({"description": "Created",'status': 201, 'message':'Successfully edit sensor, ID : {0}'.format(id_sensor)}, status=201)                        
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "Can't edit other user's sensor"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id sensor not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def deletesensor(request, id_sensor: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]     
        data = request.json 
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT node.id_user from node Inner join sensor on node.id_node = sensor.id_node 
                    WHERE sensor.id_sensor = {0}; 
                '''.format(str(id_sensor))
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    sql = """
                        DELETE from sensor WHERE id_sensor = {0};
                    """.format(str(id_sensor))
                    rows = await conn.execute(sql)
                    return response.json({"description": "OK",'status': 200, 'message':'Successfully delete sensor data'}, status=200)                        
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "Can't delete other user's sensor"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id sensor not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


def add_routes_sensor(app):
    app.add_route(addsensor, "/sensor", methods=['POST'])    
    app.add_route(listsensor, "/sensor", methods=['GET'])
    app.add_route(detailsensor, "/sensor/<id_sensor:int>", methods=['GET'])    
    app.add_route(editsensor, "/sensor/<id_sensor:int>", methods=['PUT'])    
    app.add_route(deletesensor, "/sensor/<id_sensor:int>", methods=['DELETE'])
