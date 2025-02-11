from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class user(db.Model):
    __tablename__ = "user"
    
    def __init__(self,name,login,email,password):
         self.name = name
         self.email = email
         self.login = login
         self.password = password

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),nullable=False)
    login = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(20),nullable=False)