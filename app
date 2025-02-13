from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db,user 

app = Flask(__name__)
app.secret_key = 'othmaneskey'

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        log = request.form.get('login')
        password = request.form.get('password')
        usr = user.query.filter_by(login=log).first()

        if usr and check_password_hash(usr.password, password):
            session['name'] = usr.name
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
        hashed_password = generate_password_hash(password, method='sha256')
        usr = user(name=name, login=log, email=email, password=hashed_password)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')



app.run(debug = True) 
