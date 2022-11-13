from sanic import response
from auth import check_token,jsonify
import datetime
import jwt

async def addchannel(request):
    data = request.json 
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        async with pool.acquire() as conn:
            try:
                if (data["value"] and str(data["id_node"]).isdigit()):
                    sql = '''
                            SELECT * from node WHERE id_node = {0}; 
                        '''.format(str(data["id_node"]))
                    rows = await conn.fetch(sql)
                    if(bool(rows)):
                        res = jsonify(rows)[0]
                        iduser = res["id_user"]
                        if(id_user == iduser or authtoken["isadmin"] == 1):
                            valid =1
                        else:
                            return response.json({"description": "Forbidden",'status': 403, "message": "You can't send channel to another user's sensor"}, status=403)                                                              
                    else:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id node not found"}, status=400)                                                                   
                else:
                    return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
            except Exception as e:
                print(e)
                return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
            
            ## Validate each field already have name and sensor before inserted a value
            arrayvalue=data["value"]
            dt_value = arrayvalue.replace('{','').replace('}','').split(',')
            for x in range(len(dt_value)):
                if(dt_value[x] != 'NULL'):
                    print(res["field_sensor"])
                    if(res["field_sensor"][x] and res["field_sensor"][x] != 'NULL'):
                        valid = 1                        
                    else:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Field sensor is empty. field = {0}".format(str(x))}, status=400)                           

            sql = """
                INSERT into feed (time, value, id_node) values
                (current_timestamp,'{0}',{1});
            """.format(arrayvalue, str(data["id_node"]))
            rows = await conn.execute(sql)
            return response.json({"description": "Created",'status': 201, 'message':'Successfully add new channel'}, status=201)        
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


def add_routes_channel(app):
    app.add_route(addchannel, "/channel", methods=['POST'])    
