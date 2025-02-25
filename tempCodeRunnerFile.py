from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Message
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Iyas.2020@localhost:5432/community'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('othmaneskey', 'fallback_secret_key')

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}