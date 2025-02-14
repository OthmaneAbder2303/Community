from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,User 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Iyas.2020@localhost:5432/community'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'othmaneskey'

db.init_app(app)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        log = request.form.get('login')
        password = request.form.get('password')
        usr = User.query.filter_by(login=log).first()

        if usr and check_password_hash(usr.password, password):
            session['user_id'] = usr.id
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
    return "Welcome to the chat!"

# Create the tables in the database (run once)
with app.app_context():
    db.create_all()
    
print("Database Created Successfully")

app.run(debug = True) 
