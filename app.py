from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,User
from flask_socketio import SocketIO, join_room, leave_room, send
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Iyas.2020@localhost:5432/community'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('othmaneskey', 'fallback_secret_key')

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        log = request.form.get('login')
        password = request.form.get('password')
        usr = User.query.filter_by(login=log).first()

        if usr and check_password_hash(usr.password, password):
            session['user_id'] = usr.id
            session['username'] = usr.name
            return redirect(url_for('chat'))
        else:
            print('Not Authorized')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        log = request.form.get('login')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        usr = User(name=name, login=log, email=email, password=hashed_password)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

# SocketIO Event Handlers

@socketio.on('connect')
def handle_connect():
    if 'user_id' not in session:
        return False  # Refuse la connexion
    print(f"User {session.get('username')} connected.")


@socketio.on('message')
def handle_message(data):
    """Broadcast messages to all clients"""
    print(f"Received message: {data['msg']} from {session.get('username')}")
    send({'msg': data['msg'], 'username': session.get('username')}, broadcast=True)

@socketio.on('join')
def handle_join(data):
    """Handles users joining a chat room"""
    room = data['room']
    join_room(room)
    send({'msg': f"{session.get('username')} has joined the room {room}."}, to=room)

@socketio.on('leave')
def handle_leave(data):
    """Handles users leaving a chat room"""
    room = data['room']
    leave_room(room)
    send({'msg': f"{session.get('username')} has left the room {room}."}, to=room)

@socketio.on('disconnect')
def handle_disconnect():
    print(f"User {session.get('username')} disconnected.")


# Create the tables in the database (run once)
with app.app_context():
    db.create_all() 
print("Database Created Successfully")

app.run(debug = True) 
