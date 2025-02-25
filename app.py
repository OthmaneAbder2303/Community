from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Message
from flask_socketio import SocketIO, send, emit
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Iyas.2020@localhost:5432/community'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('othmaneskey', 'fallback_secret_key')

db.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        log = request.form.get('login')
        password = request.form.get('password')
        usr = User.query.filter_by(login=log).first()

        if usr and check_password_hash(usr.password, password):
            session['user_id'] = usr.id
            session['username'] = usr.name

            usr.is_online = True
            db.session.commit()

            return redirect(url_for('chat'))
        else:
            print('Not Authorized')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/logout")
def logout():
    user_id = session.get("user_id")
    if user_id:
        usr = User.query.get(user_id)
        if usr:
            usr.is_online = False
            db.session.commit()

    session.pop("user_id", None)
    session.pop("username", None)

    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        log = request.form.get('login')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        usr = User(name, log, email, hashed_password)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    if 'user_id' not in session:
        return False

    username = session.get('username')
    connected_users[username] = request.sid

    emit("update_users", list(connected_users.keys()), broadcast=True)
    print(f"✅ {username} is now online.")

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in connected_users:
        del connected_users[username]

    emit("update_users", list(connected_users.keys()), broadcast=True)
    print(f"❌ {username} is now offline.")

@socketio.on('message')
def handle_message(data):
    sender = session.get('username')
    message_text = data['msg']

    if not sender or not message_text:
        return

    timestamp = datetime.utcnow()

    # Save message in database
    message = Message(sender=sender, message=message_text, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()

    # Send message to all users
    send({'msg': message_text, 'username': sender, 'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')}, broadcast=True)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Retrieve all past messages."""
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    messages = Message.query.order_by(Message.timestamp).all()

    return jsonify([
        {'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for msg in messages
    ])

# Create tables in the database
with app.app_context():
    db.create_all()
print("Database Created Successfully")

if __name__ == '__main__':
    socketio.run(app, debug=True)
