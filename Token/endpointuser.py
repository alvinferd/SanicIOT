from sanic import response
from auth import check_token,jsonify
import hashlib
import jwt
import smtplib
import email.message
import re, random, string

async def healthcheck(request):
    return response.json({"description": "OK",'status': 200, 'message': "working"}, status=200)

async def activation(request):
    pool = request.app.config['pool']
    try:
        token = jwt.decode(
                request.args["token"][0], request.app.config.SECRET, algorithms=["HS256"]
            )
        async with pool.acquire() as conn:
            sql = '''
                    SELECT *
                    FROM user_person where username='{0}'; 
                '''.format(token["username"])    
            res = jsonify(await conn.fetch(sql))[0]
            if(res["status"] != 1):
                new_token = jwt.encode({"id_user":res["id_user"], "username":res["username"],"is_admin":0}, request.app.config.SECRET)
                sql = '''
                    UPDATE user_person set status = true, token = '{0}' where username = '{1}';
                    '''.format(new_token,token["username"])
                activate = await conn.execute(sql)
                return response.json({"description": "OK",'status': 200, 'message': 'Your account has been activated successfully'}, status=200)
            else:
                return response.json({"description": "Bad Request",'status': 400, 'message': 'Your account has already activated'}, status=200)                
    except:
        return response.json({"description": "Bad Request",'status': 400, 'message': 'Invalid token'}, status=200)           

async def changepassword(request):
    authentication = check_token(request)
    if(authentication[0]):
        authtoken = authentication[1]    
        data = request.json 
        id_user = authtoken["id_user"]
        pool = request.app.config['pool']
        try:
            if ( data["old_password"] and data["new_password"] ):
                async with pool.acquire() as conn:
                    sql = '''
                            SELECT password
                            FROM user_person where id_user={0}; 
                        '''.format(id_user)    
                    oldpass = jsonify(await conn.fetch(sql))[0]["password"]
                    old_pass = hashlib.sha256(data['old_password'].encode()).hexdigest()
                    new_pass = hashlib.sha256(data['new_password'].encode()).hexdigest()
                    if(old_pass == oldpass):
                        sql = """ 
                        UPDATE user_person set password = '{0}' where id_user = {1}
                        """.format(new_pass,id_user)
                        ex = await conn.execute(sql)
                        return response.json({"description": "OK",'status': 200, 'message': 'Successfully change password'}, status=200)
                    else:   
                        return response.json({"description": "Forbidden",'status': 403, 'message': 'Old password is incorect'}, status=403)                
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
        except:
            return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)
    else:
        return response.json({"description": "Forbidden",'status': 403, 'message': "You are unauthorized, invalid token."}, status=403)

async def resetpass(request):
    data = request.json 
    pool = request.app.config['pool']
    try:
        if ( data["username"] and data["email"] ):
            regex = r'[\w!#$%&\'*+-/=?^_`{|}~.]+@[\w\.-]+'
            if re.search(regex, data["email"]):                 
                async with pool.acquire() as conn:
                    sql = """
                    SELECT status from user_person where email = '{0}' and username = '{1}';
                    """.format(data["email"],data["username"])
                    rows = await conn.fetch(sql)
                    if(bool(rows)):
                        stat = jsonify(rows)[0]["status"]
                        if(stat):
                            newPassword = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                            passHash = hashlib.sha256(newPassword.encode()).hexdigest()
                            email_content = """ 
                            <html>
                              <head>
                              </head>
                              <body>
                                <h3>Dear """+data["username"]+""". </h3>
                                <p>We have accepted your forget password request. Use this password for log in.</p>
                                <p><h4>"""+newPassword+"""</h4></p>
                                <p>Thank You</p>
                              </body
                            </html>
                            """
                            msg = email.message.Message()
                            msg['Subject'] = 'New Password'
                            msg['From'] = 'RepairingDevice001@gmail.com'
                            msg['To'] = data["email"]
                            password = "wgwmwhnktnmvyxwm"
                            msg.add_header('Content-Type', 'text/html') 
                            msg.set_payload(email_content)
                            s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            s.login(msg['From'], password) 
                            s.sendmail(msg['From'], [msg['To']], msg.as_string())            
                            sql = """
                            UPDATE user_person set password = '{0}' where username = '{1}';
                            """.format(passHash,data["username"]) 
                            ex = await conn.execute(sql) 
                            return response.json({"description": "OK",'status': 200, 'message': 'Forget password request sent. Check email for new password'}, status=200)
                        else:
                           return response.json({"description": "Forbidden",'status': 403, "message": "Your account is inactive. Check your email for activation"}, status=403)         
                    else:
                       return response.json({"description": "Bad Request",'status': 400, "message": "Username or email incorrect"}, status=400)         
            else:
                return response.json({"description": "Bad Request",'status': 400, "message": "Email format is incorrect"}, status=400)         
        else:
            return response.json({"description": "Bad Request",'status': 400, "message": "Empty request body"}, status=400)         
    except:
        return response.json({"description": "Bad Request",'status': 400, "message": "Missing parameter"}, status=400)


def add_routes_user(app):
    app.add_route(healthcheck, '/healthcheck/', methods=['GET'])
    app.add_route(activation, '/user/activation/', methods=['GET'])    
    app.add_route(changepassword, '/user/change-password/', methods=['PUT'])    
    app.add_route(resetpass, '/user/forget-password/', methods=['POST'])    
