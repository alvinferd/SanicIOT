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
                if (data["value"] and str(data["id_sensor"]).isdigit()):
                    sql = '''
                            SELECT node.id_user from node Inner join sensor on node.id_node = sensor.id_node 
                            WHERE sensor.id_sensor = {0}; 
                        '''.format(str(data["id_sensor"]))
                    try:
                        rows = await conn.fetch(sql)
                        iduser = jsonify(rows)[0]["id_user"]
                        if(id_user == iduser or authtoken["is_admin"] == 1):
                            valid =1
                        else:
                            return response.json({"description": "Forbidden",'status': 403, "message": "You can't send channel to another user's sensor"}, status=403)                                                              
                    except:
                        return response.json({"description": "Bad Request",'status': 400, "message": "Id sensor not found"}, status=400)                                                                   
                else:
                    return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
            except:
                return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
            sql = """
                INSERT into channel (time, value, id_sensor) values
                (current_timestamp,'{0}',{1});
            """.format(str(data["value"]), str(data["id_sensor"]))
            rows = await conn.execute(sql)
            return response.json({"description": "Created",'status': 201, 'message':'Successfully add new channel'}, status=201)        
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


def add_routes_channel(app):
    app.add_route(addchannel, "/channel", methods=['POST'])    
