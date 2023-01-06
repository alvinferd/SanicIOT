from sanic import response
from auth import check_token,jsonify
import jwt

async def deletenode(request, id_node: int):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]  
        id_user,isadmin = authtoken["id_user"],authtoken["isadmin"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            sql = '''
                    SELECT id_user from node where id_node = {0}; 
                '''.format(id_node)
            rows = await conn.fetch(sql)
            if(bool(rows)):
                iduser = jsonify(rows)[0]["id_user"]
                if(id_user == iduser or isadmin == 1):
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


async def addnode(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]
        data = request.json 
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            try:
                if (data["name"] and data["location"] and str(data["id_hardware_node"]).isdigit()):

                    ## VALIDATE id_hardware_node type should be for node
                    sql = """
                        SELECT hardware.type from hardware WHERE id_hardware = {0};
                        """.format(str(data["id_hardware_node"]))
                    rows = await conn.fetch(sql)
                    if(bool(rows)):
                        res_hardware = jsonify(rows)[0]
                        if(res_hardware["type"] == "single-board computer" or res_hardware["type"] == "microcontroller unit"):
                            valid = 1
                        else :
                            return response.json({"description": "Bad Request",'status': 400, "message": "Hardware node type not match, type should be single-board computer or microcontroller unit"}, status=400)                               
                    else:   
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware for node not found"}, status=400)                           
                else:
                    return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
            except Exception as e:
                return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
            try:
                if(data["is_public"]):
                    public=True
                else:
                    public=False
            except:
                public=False
            try:
                ## VALIDATE id_hardware_sensor exist and should be type sensor
                if(data["id_hardware_sensor"]):
                    arraysensor=data["id_hardware_sensor"]
                    dt_sensor = arraysensor.replace('{','').replace('}','').split(',')
                    for x in dt_sensor:
                        if(x != 'NULL'):
                            sql = """
                                SELECT hardware.type from hardware WHERE id_hardware = {0};
                                """.format(str(x))
                            rows = await conn.fetch(sql)
                            if(bool(rows)):
                                res_hardware = jsonify(rows)[0]
                                if(res_hardware["type"] == "sensor"):
                                    valid = 1
                                else:
                                    return response.json({"description": "Bad Request",'status': 400, "message": "Hardware sensor type not match, type should be sensor. id = {0}".format(str(x))}, status=400)                               
                            else:
                                return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware for sensor not found. id = {0}".format(str(x))}, status=400)                           
                else:
                    arraysensor='{NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL}'
            except:
                arraysensor='{NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL}'
            try:
                ## VALIDATE the field should be registered on existed sensor column
                if(data["field_sensor"]):
                    arrayfield=data["field_sensor"]
                    dt_field = arrayfield.replace('{','').replace('}','').split(',')
                    for x in range(len(dt_field)):
                        if(dt_field[x] != 'NULL'):
                            if(dt_sensor[x] != 'NULL'):
                                valid = 1
                            else:
                                return response.json({"description": "Bad Request",'status': 400, "message": "Field sensor is empty. field = {0}".format(str(x))}, status=400)                           
                else:
                    arrayfield='{NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL}'
            except:
                arrayfield='{NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL}'
            id_user = authtoken["id_user"]

            ## INSERT value
            sql = """
                INSERT into node (name, location, id_hardware_node,id_user,is_public,id_hardware_sensor,field_sensor) values ('{0}','{1}',{2},{3},{4},'{5}','{6}')
            """.format(data["name"], data["location"], str(data["id_hardware_node"]), str(id_user),public,arraysensor,arrayfield)
            rows = await conn.execute(sql)
            return response.json({"description": "Created",'status': 201, 'message':'Successfully add new node'}, status=201)        
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
                    SELECT * from node where id_node = {0}; 
                '''.format(id_node)
            rows = await conn.fetch(sql)
            if(bool(rows)):
                res_cur_node = jsonify(rows)[0]
                iduser = res_cur_node["id_user"]
                if(id_user == iduser or authtoken["isadmin"] == 1):
                    try:
                        if (data["name"] and data["location"] and str(data["id_hardware_node"]).isdigit()):
        
                            ## VALIDATE id_hardware_node type should be for node
                            sql = """
                                SELECT hardware.type from hardware WHERE id_hardware = {0};
                                """.format(str(data["id_hardware_node"]))
                            rows = await conn.fetch(sql)
                            if(bool(rows)):
                                res_hardware = jsonify(rows)[0]
                                if(res_hardware["type"] == "single-board computer" or res_hardware["type"] == "microcontroller unit"):
                                    valid = 1
                                else :
                                    return response.json({"description": "Bad Request",'status': 400, "message": "Hardware node type not match, type should be single-board computer or microcontroller unit"}, status=400)                               
                            else:   
                                return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware for node not found"}, status=400)                           
                        else:
                            return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
                    except Exception as e:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)

                    try:
                        if(data["is_public"]):
                            public=True
                        else:
                            public=False
                    except:
                        public=False
                    try:
                        ## VALIDATE id_hardware_sensor exist and should be type sensor
                        if(data["id_hardware_sensor"]):
                            arraysensor=data["id_hardware_sensor"]
                            dt_sensor = arraysensor.replace('{','').replace('}','').split(',')
                            for x in dt_sensor:
                                if(x != 'NULL'):
                                    sql = """
                                        SELECT hardware.type from hardware WHERE id_hardware = {0};
                                        """.format(str(x))
                                    rows = await conn.fetch(sql)
                                    if(bool(rows)):
                                        res_hardware = jsonify(rows)[0]
                                        if(res_hardware["type"] == "sensor"):
                                            valid = 1
                                        else:
                                            return response.json({"description": "Bad Request",'status': 400, "message": "Hardware sensor type not match, type should be sensor. id = {0}".format(str(x))}, status=400)                               
                                    else:
                                        return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware for sensor not found. id = {0}".format(str(x))}, status=400)                           
                        else:
                            arraysensor= res_cur_node["id_hardware_sensor"]
                    except:
                        arraysensor= res_cur_node["id_hardware_sensor"]
                    try:
                        ## VALIDATE the field should be registered on existed sensor column
                        if(data["field_sensor"]):
                            arrayfield=data["field_sensor"]
                            dt_field = arrayfield.replace('{','').replace('}','').split(',')
                            for x in range(len(dt_field)):
                                if(dt_field[x] != 'NULL'):
                                    if(dt_sensor[x] != 'NULL' or res_cur_node["id_hardware_sensor"][x] != None):
                                        valid = 1
                                    else:
                                        return response.json({"description": "Bad Request",'status': 400, "message": "Field sensor is empty. field = {0}".format(str(x))}, status=400)                           
                        else:
                            arrayfield= res_cur_node["field_sensor"]
                    except:
                        arrayfield= res_cur_node["field_sensor"]

        
                    ## INSERT value
                    sql = """
                        UPDATE node
                        SET name = '{0}', location = '{1}', id_hardware_node = {2}, is_public = {3}, id_hardware_sensor = '{4}', field_sensor = '{5}'
                        WHERE id_node = {6};
                    """.format(data["name"], data["location"], str(data["id_hardware_node"]),public,arraysensor,arrayfield, str(id_node))
                    rows = await conn.execute(sql)
                    return response.json({"description": "Created",'status': 201, 'message':'Successfully edit node, ID : {0}'.format(id_node)}, status=201)                        
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "Can't edit other user's node"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def mynode(request):
    try:
        limits = request.args["limit"][0]
    except:
        limits = 50
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]    
        pool = request.app.config['pool']
        id_userx = authtoken["id_user"]
        async with pool.acquire() as conn:
            sql = '''
                    SELECT * from node
                    where node.id_user = '{0}'; 
                '''.format(id_userx)
            rows = await conn.fetch(sql)
            res = jsonify(rows)
            for x in range(len(res)):
                sql = '''
                            SELECT feed.time, feed.value from feed
                            left join node on feed.id_node = node.id_node
                            where feed.id_node = {0} ORDER BY time DESC limit {1}; 
                        '''.format(res[x]["id_node"],limits)
                try:
                    dmp = jsonify(await conn.fetch(sql))
                    res[x]["feed"] = dmp
                    for xx in res[x]["feed"]:
                        xx["time"] = str(xx["time"])
                except:
                    res[x]["feed"] = "{}"
            return response.json({'status': 200, 'data': res}, status=200)
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def detailnode(request, id_node: int):
    try:
        limits = request.args["limit"][0]
    except:
        limits = 50
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
                iduser,ispublic = res["id_user"],res["is_public"]
                if(id_user == iduser or authtoken["isadmin"] == 1 or ispublic == True):
                    rowsFinal = res
                    sql = '''
                            SELECT feed.time, feed.value from feed
                            left join node on feed.id_node = node.id_node
                            where feed.id_node = {0} ORDER BY time DESC limit {1}; 
                        '''.format(id_node,limits)
                    try:
                        dmp = jsonify(await conn.fetch(sql))
                        rowsFinal["feed"] = dmp
                        for x in rowsFinal["feed"]:
                            x["time"] = str(x["time"])
                    except:
                        rowsFinal["feed"] = "{}"
                    return response.json({'status': 200, 'data': rowsFinal}, status=200)
                else:
                    return response.json({"description": "Forbidden",'status': 403, "message": "You can't see other user's node"}, status=403)                                                              
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                              
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

def add_routes_node(app):
    app.add_route(addnode, "/node", methods=['POST'])    
    app.add_route(mynode, "/node", methods=['GET'])
    app.add_route(detailnode, "/node/<id_node:int>", methods=['GET'])    
    app.add_route(editnode, "/node/<id_node:int>", methods=['PUT'])    
    app.add_route(deletenode, "/node/<id_node:int>", methods=['DELETE'])
