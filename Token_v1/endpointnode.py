from sanic import response
from auth import check_token,jsonify
import jwt

async def addnode(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]
        data = request.json 
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            try:
                if (data["name"] and data["location"] and str(data["id_hardware"]).isdigit()):
                    sql = """
                        SELECT hardware.type from hardware WHERE id_hardware = {0};
                        """.format(str(data["id_hardware"]))
                    rows = await conn.fetch(sql)
                    if(bool(rows)):
                        res_hardware = jsonify(rows)[0]
                        if(res_hardware["type"] == "single-board computer" or res_hardware["type"] == "microcontroller unit"):
                            valid = 1
                        else :
                            return response.json({"description": "Bad Request",'status': 400, "message": "Hardware type not match, type should be single-board computer or microcontroller unit"}, status=400)                               
                    else:   
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware not found"}, status=400)                           
                else:
                    return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
            except:
                return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
            id_user = authtoken["id_user"]
            sql = """
                INSERT into node (name, location, id_hardware,id_user) values ('{0}','{1}',{2},{3})
            """.format(data["name"], data["location"], str(data["id_hardware"]), str(id_user))
            rows = await conn.execute(sql)
            return response.json({"description": "Created",'status': 201, 'message':'Successfully add new node'}, status=201)        
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def listnode(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]    
        pool = request.app.config['pool']
        id_userx = authtoken["username"]
        async with pool.acquire() as conn:
            sql = '''
                    SELECT node.id_node, node.name, node.location, node.id_hardware, node.id_user from node INNER join user_person on node.id_user = user_person.id_user
                    where user_person.username = '{0}'; 
                '''.format(id_userx)
            rows = await conn.fetch(sql)
            return response.json({'status': 200, 'data': jsonify(rows)}, status=200)
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def detailnode(request, id_node: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]      
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT * from node where id_node = {0}; 
                '''.format(id_node)
            rows = await conn.fetch(sql)
            if(bool(rows)):
                res = jsonify(rows)[0]
                iduser = res["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    rowsFinal = res
                    sql = '''
                            SELECT hardware.name, hardware.type from hardware 
                            left join node on hardware.id_hardware = node.id_hardware 
                            where id_node = {0}; 
                        '''.format(id_node)
                    rowsFinal["hardware"] = jsonify(await conn.fetch(sql))
                    sql = '''
                            SELECT sensor.id_sensor, sensor.name, sensor.unit from sensor
                            left join node on sensor.id_node = node.id_node
                            where sensor.id_node = {0}; 
                        '''.format(id_node)
                    try:
                        rowsFinal["sensor"] = jsonify(await conn.fetch(sql))
                    except:
                        rowsFinal["sensor"] = "{}"
                    return response.json({'status': 200, 'data': rowsFinal}, status=200)
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "You can't see other user's node"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def editnode(request, id_node: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]  
        data = request.json 
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT id_user from node where id_node = {0}; 
                '''.format(id_node)
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    try:
                        if (data["name"] and data["location"] and str(data["id_hardware"]).isdigit()):
                            sql = """
                                SELECT hardware.type from hardware WHERE id_hardware = {0};
                                """.format(str(data["id_hardware"]))
                            rows = await conn.fetch(sql)
                            if(bool(rows)):
                                res_hardware = jsonify(rows)[0]
                                if(res_hardware["type"] == "single-board computer" or res_hardware["type"] == "microcontroller unit"):
                                    valid = 1
                                else :
                                    return response.json({"description": "Bad Request",'status': 400, "message": "Hardware type not match, type should be single-board computer or microcontroller unit"}, status=400)                               
                            else:   
                                return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware not found"}, status=400)                           
                        else:
                            return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
                    except:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
                    sql = """
                        UPDATE node
                        SET name = '{0}', location = '{1}', id_hardware = {2}
                        WHERE id_node = {3};
                    """.format(data["name"], data["location"], str(data["id_hardware"]), str(id_node))
                    rows = await conn.execute(sql)
                    return response.json({"description": "Created",'status': 201, 'message':'Successfully edit node, ID : {0}'.format(id_node)}, status=201)                        
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "Can't edit other user's node"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def deletenode(request, id_node: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]  
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT id_user from node where id_node = {0}; 
                '''.format(id_node)
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or authtoken["is_admin"] == 1):
                    sql = '''
                            DELETE from node where id_node = {0}; 
                        '''.format(id_node)
                    rows = await conn.execute(sql)
                    if(rows=="DELETE 1"):
                        return response.json({'status': 200, 'data': "Successfully delete node, id: {0}".format(str(id_node))}, status=200)
                    else:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                                              
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "Can't delete other user's node"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


def add_routes_node(app):
    app.add_route(addnode, "/node", methods=['POST'])    
    app.add_route(listnode, "/node", methods=['GET'])
    app.add_route(detailnode, "/node/<id_node:int>", methods=['GET'])    
    app.add_route(editnode, "/node/<id_node:int>", methods=['PUT'])    
    app.add_route(deletenode, "/node/<id_node:int>", methods=['DELETE'])
