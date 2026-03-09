from flask import Flask
from flask_socketio import SocketIO
from flask_wtf.csrf import ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app)

@socketio.on('connect')
def connect(auth):
    raise ConnectionRefusedError('invalid_csrf')

if __name__ == '__main__':
    socketio.run(app, port=9999)
