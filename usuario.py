from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask import jsonify

from db import db, ma

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    user = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(100))
    rol = db.Column(db.String(25))
    create_user = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    
    def __init__(self, name, last_name, user, password, rol,create_user):
        self.name = name
        self.last_name = last_name
        self.user = user
        self.password = self.__create_password(password)
        self.rol = rol
        self.create_user = create_user

    def __create_password(self, password):
        return generate_password_hash(password)

    def nueva_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

    def getUsers():
        users_db = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users_db)
        return jsonify({'data':output})

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','last_name','user','rol')


