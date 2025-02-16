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

# Stocker les utilisateurs connectés
connected_users = {}

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
        return False  # Refuse the connection

    username = session.get('username')
    connected_users[username] = request.sid

    # Update user status in DB
    user = User.query.filter_by(name=username).first()
    if user:
        user.is_online = True
        db.session.commit()

    emit("update_users", list(connected_users.keys()), broadcast=True)
    print(f"✅ {username} is now online.")

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username in connected_users:
        del connected_users[username]

        # Update user status in DB
        user = User.query.filter_by(name=username).first()
        if user:
            user.is_online = False
            db.session.commit()

        emit("update_users", list(connected_users.keys()), broadcast=True)
        print(f"❌ {username} is now offline.")


@socketio.on('join')
def handle_join(data):
    """Handles users joining a private chat room"""
    user1 = session.get('username')  # The current logged-in user
    user2 = data.get('username')  # The recipient

    if not user1:
        return  # Prevent unauthorized users from joining

    if not user2 or user1 == user2:
        return  # Prevent joining an invalid room (self-chat not needed)

    # Create a unique room ID
    room = f"{user1}_{user2}" if user1 < user2 else f"{user2}_{user1}"
    
    join_room(room)
    print(f"{user1} joined the room {room}")

    # Notify both users
    send({'msg': f"{user1} has joined the room."}, to=room)


from models import db, Message  # Import the Message model

@socketio.on('message')
def handle_message(data):
    """Handles sending messages to a specific room (private chat)"""
    user1 = session.get('username')  # The current logged-in user
    user2 = data['username']  # The recipient user
    message_text = data['msg']  # The actual message

    if not user1 or not user2:
        return

    # Create a unique room name
    room = f"{user1}_{user2}" if user1 < user2 else f"{user2}_{user1}"

    # Save message in database
    message = Message(sender=user1, recipient=user2, room=room, message=message_text)
    db.session.add(message)
    db.session.commit()

    # Send message to the chat room
    send({'msg': message_text, 'username': user1}, to=room)

@app.route('/get_messages/<username>', methods=['GET'])
def get_messages(username):
    """Retrieve past messages between the logged-in user and another user"""
    if 'username' not in session:
        return {"error": "Unauthorized"}, 401

    user1 = session['username']
    user2 = username  # The other user in the chat

    # Generate the correct room name
    room = f"{user1}_{user2}" if user1 < user2 else f"{user2}_{user1}"

    # Fetch messages from the database
    messages = Message.query.filter_by(room=room).order_by(Message.timestamp).all()
    
    return [{'sender': msg.sender, 'message': msg.message, 'timestamp': msg.timestamp} for msg in messages]



@socketio.on('leave')
def handle_leave(data):
    """Handles users leaving a chat room"""
    room = data.get('room')  # Ensure we safely get the room

    # Check if the room exists and if the user is in the room
    if room and session.get('username'):
        leave_room(room)  # Let the user leave the room

        # Broadcast a message to the room that the user left
        send({'msg': f"{session.get('username')} has left the room {room}."}, to=room)
        print(f"❌ {session.get('username')} has left the room {room}.")
    else:
        print("Error: Room or username not found.")



# Create the tables in the database (run once)
with app.app_context():
    db.create_all() 
print("Database Created Successfully")

if __name__ == '__main__':
    socketio.run(app, debug=True)
