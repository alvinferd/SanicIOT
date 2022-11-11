from sanic import Sanic, response
from asyncpg import create_pool
from endpointuser import *
from endpointhardware import *
from endpointnode import *
from endpointsensor import *
from endpointchannel import *
from auth import *
#import asyncio
#import uvloop


app = Sanic("IOTServer")
add_routes_auth(app)
add_routes_user(app)
add_routes_hardware(app)
add_routes_node(app)
add_routes_sensor(app)
add_routes_channel(app)
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"


#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  ##Do not working on windows

# References listener : https://sanic.dev/en/guide/basics/listeners.html#attaching-a-listener
@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    # pool faster than single connection :
        # https://stackoverflow.com/questions/42242093/asyncpg-connection-vs-connection-pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='postgres', password='postgres', host='localhost',
        port=5432, database='postgres'
    )
    #asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  ##Do not working on windows
    app.config['pool'] = await create_pool(
        dsn=conn,
        # in bytes
        min_size=10,
        # in bytes
        max_size=10,
        # maximum query
        max_queries=50000,
        # maximum idle times
        max_inactive_connection_lifetime=300,
        loop=loop)

@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,
            access_log=True, debug=True)