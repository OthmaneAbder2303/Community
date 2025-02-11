from flask import Flask, request, redirect, url_for, render_template
from models import db,user

app = Flask(__name__)   # Flask constructor 
  
@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'login':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('register'))
        
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__': 
   app.run(debug = True) 
