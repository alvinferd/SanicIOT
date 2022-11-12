from sanic import response
from auth import check_token, jsonify
import jwt

async def addhardware(request):
	authentication = check_token(request)
	if(authentication[0]):
		authtoken = authentication[1]
		data = request.json	
		try:
			if (data["name"] and data["type"] and data["description"]):
				if(data["type"] == "single-board computer" or data["type"] == "microcontroller unit" or data["type"] == "sensor"):
					valid=1
				else:	
					return response.json({"description": "Bad Request",'status': 400, "message": "Type must single-board computer, microcontroller unit, or sensor"}, status=400)							
			else:
				return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)			
		except:
			return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
	
		pool = request.app.config['pool']
		async with pool.acquire() as conn:
			sql = """
				INSERT into hardware (name, type, description) values ('{0}', '{1}', '{2}')
			""".format(data["name"], data["type"], data["description"])
			rows = await conn.execute(sql)
			return response.json({"description": "Created",'status': 201, 'message':'Successfully add new hardware'}, status=201)		
	else:
		return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def edithardware(request, id_hardware: int):
	authentication = check_token(request)
	if(authentication[0]):
		authtoken = authentication[1]
		data = request.json	
		try:
			if (data["name"] and data["type"] and data["description"]):
				if(data["type"] == "single-board computer" or data["type"] == "microcontroller unit" or data["type"] == "sensor"):
					valid=1
				else:	
					return response.json({"description": "Bad Request",'status': 400, "message": "Type must single-board computer, microcontroller unit, or sensor"}, status=400)							
			else:
				return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)			
		except:
			return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
	
		pool = request.app.config['pool']
		async with pool.acquire() as conn:
			sql = """
				UPDATE hardware 
				set name = '{0}', type = '{1}', description = '{2}'
				where id_hardware = {3};
			""".format(data["name"], data["type"], data["description"],str(id_hardware))
			rows = await conn.execute(sql)
			return response.json({"description": "OK",'status': 200, 'message':'Successfully edit hardware, id: {0}'.format(str(id_hardware))}, status=200)		
	else:
		return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def deletehardware(request, id_hardware: int):
	authentication = check_token(request)
	if(authentication[0]):
		authtoken = authentication[1]	
		pool = request.app.config['pool']
		async with pool.acquire() as conn:
			sql = '''
					DELETE from hardware where id_hardware = {0}; 
				'''.format(id_hardware)
			rows = await conn.execute(sql)
			if(bool(rows)):
				if(rows=="DELETE 1"):
					return response.json({'status': 200, 'data': "Successfully delete hardware, id: {0}".format(str(id_hardware))}, status=200)
				else:
					return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware not found"}, status=400)	 															
			else:
				return response.json({"description": "Bad Request",'status': 400, "message": "Can't delete, hardware is still in used"}, status=400)	 			
	else:
		return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)


async def detailhardware(request, id_hardware: int):
	authentication = check_token(request)
	if(authentication[0]):
		authtoken = authentication[1]	
		pool = request.app.config['pool']
		async with pool.acquire() as conn:
					sql = '''
							SELECT * from hardware 
							where id_hardware = {0}; 
						'''.format(id_hardware)
					valid = await conn.fetch(sql)
					if(bool(valid)):			   
						rowsFinal = jsonify(valid)[0]
						if(rowsFinal["type"] == "sensor"):
							sql = '''
									SELECT name, unit from sensor 
									where id_hardware = {0}; 
								'''.format(id_hardware)
							rowsFinal["sensor"] = jsonify(await conn.fetch(sql))
						else:
							sql = '''
									SELECT name,location from node 
									where id_hardware = {0}; 
								'''.format(id_hardware)
							rowsFinal["node"] = jsonify(await conn.fetch(sql))
						return response.json({'status': 200, 'data': rowsFinal}, status=200)
					else:
						return response.json({"description": "Bad Request",'status': 400, "message": "Id hardware not found"}, status=400)															  
	else:
		return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)
	
async def userhardware(request):
	authentication = check_token(request)
	if(authentication[0]):
		authtoken = authentication[1]	
		pool = request.app.config['pool']
		async with pool.acquire() as conn:
							sql = '''
									SELECT * from node
									where id_user = {0}; 
								'''.format(id_user)
							resuser = jsonify(await conn.fetch(sql))
							finalres = {}
							try:
								sql = '''
										SELECT * from hardware 
										where id_hardware = {0}; 
									'''.format(resuser[0]["id_hardware"])
								finalres["node"] = jsonify(await conn.fetch(sql))
							except:
								finalres["node"] = []
							try:													   
								sql = '''
										SELECT id_hardware from sensor
										where id_node = {0}; 
									'''.format(resuser[0]["id_node"])
								id_node_hardware = jsonify(await conn.fetch(sql))
								sql = '''
										SELECT * from hardware 
										where id_hardware = {0}; 
									'''.format(id_node_hardware[0]["id_hardware"])								
								finalres["sensor"] = jsonify(await conn.fetch(sql))
							except:
								finalres["sensor"] = []
							return response.json({'status': 200, 'data': finalres}, status=200)
	else:
		return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

def add_routes_hardware(app):
	app.add_route(addhardware, "/hardware", methods=['POST'])
	app.add_route(edithardware, "/hardware/<id_hardware:int>", methods=['PUT'])	
	app.add_route(deletehardware, "/hardware/<id_hardware:int>", methods=['DELETE'])
	app.add_route(detailhardware, "/hardware/<id_hardware:int>", methods=['GET'])   
	app.add_route(userhardware, "/hardware/", methods=['GET'])	   