import sanic
from sanic import response
from sanic.response import *
from functools import wraps
import email.message
import smtplib, ssl
import hashlib
import json
import jwt

def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    list_return = []
    for r in records:
        itens = r.items()
        list_return.append({i[0]: i[1].rstrip() if type(
            i[1]) == str else i[1] for i in itens})
    return list_return


def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(
            request.token, request.app.config.SECRET, algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)
            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:               
                return sanic.response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)
        return decorated_function
    return decorator(wrapped)

async def login(request):
    data = request.json
    pool = request.app.config['pool']
    try:
        async with pool.acquire() as conn:
            sql = '''
                    SELECT *
                    FROM user_person where username='{0}'; 
                '''.format(data["username"])    
            rows = await conn.fetch(sql)
            if(bool(rows)):
                res = (jsonify(rows)[0])
                iduser, username, realpass, isactive, isadmin = res["id_user"], res["username"], res["password"], res["status"], res["is_admin"]
                hashpass = hashlib.sha256(data['password'].encode()).hexdigest()
                if(hashpass == realpass):
                    if(isactive):
                        token = res["token"]
                        #token = jwt.encode({"username":username,"is_admin":isadmin}, request.app.config.SECRET)
                        return response.json({"description": "OK",'status': 200, 'token': token}, status=200)
                    else:
                        return response.json({"description": "Forbidden",'status': 403, 'message': "Account have not active yet"}, status=403)
                else:
                    return response.json({"description": "Unauthorized",'status': 401, 'message': "Username or password incorrect"}, status=401)
            else:
                return response.json({"description": "Unauthorized",'status': 401, 'message': "Username or password incorrect"}, status=401)
    except:
        return response.json({"description": "Bad Request",'status': 400, "message": "Username or password empty"}, status=400)


async def register(request):
    data = request.json
    pool = request.app.config['pool']
    try:
        if (data["username"] and data["email"] and data["username"]):
            check=1
        else:
            return response.json({"description": "Bad Request",'status': 400, "message": "Empty body request"}, status=400)
    except:
        return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
    try:
        async with pool.acquire() as conn:
            token = jwt.encode({"username":data["username"],"is_admin":0}, request.app.config.SECRET)
            sql = '''
                        insert into user_person (username,email,password)
                        values ('{0}','{1}','{2}'); 
                    '''.format(data["username"],data["email"],hashlib.sha256(data["password"].encode()).hexdigest())    
            rows = await conn.execute(sql)
            #print(rows, bool(rows))
            if(bool(rows)):
                urlCode = "http://localhost:8000/user/activation?token="+token
                email_content = """ 
                <html>                           
                <head>>
                  <title>Activation Message</title>
                </head>
                <body>
                
                  <h1>Activation Message</h1>
                  <h4>Dear """+data["username"]+"""</h4>
                  <p>We have accepted your registration. 
                  <p>Click <a href="""+urlCode+""">here</a> to activate your account</p>
                  <p><h5>Thank you</h5></p>     
                </body>
                </html> 
                """
                msg = email.message.Message()
                msg['Subject'] = 'Activation Message'
                msg['From'] = 'RepairingDevice001@gmail.com'
                msg['To'] = data["email"]
                password = "wgwmwhnktnmvyxwm"
                msg.add_header('Content-Type', 'text/html') 
                msg.set_payload(email_content)
                s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                s.login(msg['From'], password) 
                s.sendmail(msg['From'], [msg['To']], msg.as_string())            
                return response.json({"description": "OK",'status': 200, 'message': "User created. Please check email for activation"}, status=200)
            else:
                return response.json({"description": "Internal Server Error",'status': 500}, status=500)        
    except:
        return response.json({"description": "Conflict",'status': 409, 'message': "Email or username already exist"}, status=409)


def add_routes_auth(app):
    app.add_route(login, '/auth/login', methods=['POST'])
    app.add_route(register, '/auth/register', methods=['POST'])
