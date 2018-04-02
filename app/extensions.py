from flask_restless import APIManager
from flask_assets import Environment
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

api = APIManager()
assets = Environment()
ma = Marshmallow()
sk = SocketIO()
db = SQLAlchemy()