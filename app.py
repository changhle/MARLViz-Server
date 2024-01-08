import socketio
from sanic import Sanic
import asyncio
import time
import pprint
import logging
from importlib import reload
import processing.data_process as dp
reload(dp)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.INFO)

port = 8664
sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins=[])
app = Sanic('Smart-Logistics-Server')
app.enable_websocket(True)
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
sio.attach(app)

pp = pprint.PrettyPrinter(indent=4, depth=10)

# Session
session_dict = {}


@sio.on('connect')
async def connect(sid, environ):
    global session_dict
    session = {}
    session_dict[sid] = session
    print('connect', '(sid : ' + sid + ')')
    await sio.emit('connection_response', 'handshake success', room=sid)


@sio.on('disconnect')
async def disconnect(sid):
    del session_dict[sid]
    print('disconnect', '(sid : ' + sid + ')')


@sio.on('user')
async def send_user_info(sid):
    packet = {
        'snake_list': dp.snake_list
    }
    await sio.emit('user', packet, room=sid)


@sio.on('user_workout_matrix')
async def send_user_workout_matrix(sid, data):
    packet = dp.get_workout_matrix_info(data)
    await sio.emit('user_workout_matrix', packet, room=sid)


if __name__ == '__main__':
    dp.preprocess()
    app.run(host="0.0.0.0", port=port)
