from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from config import DevelopmentConfig
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

from db import db, ma
from usuario import User
from juego import Juego


@app.route('/')
def index():
    return f'<h1>ApiRest Game Store IPC1<h1>'
    #return User.getUsers()

@app.route('/login', methods=['POST'])
def login():
    
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400

    userreq = request.json['username']
    passreq = request.json['password']
    
    if not userreq:
        return jsonify({"msg": "Se requiere un usuario"}), 400
    if not passreq:
        return jsonify({"msg": "Se requiere una contraseña"}), 400

    userdb = User.query.filter_by(user=userreq).first()

    if not userdb:
        return jsonify({"msg": "Usuario no existe"}), 401

    if not userdb.check_password(passreq):
        return jsonify({"msg": "Password Incorrecto"}), 401

    # Identity can be any data that is json serializable
    token = create_access_token(identity=userdb.user)
    return jsonify(token=token,usuario=userdb.user,rol=userdb.rol), 200

@app.route('/register',methods=['POST'])
def register():

    userreq = request.json.get('username', None)
    userdb = User.query.filter_by(user=userreq).first()

    if userdb is not None and userdb.user:
        return jsonify({"msg": "Usuario ya existe, intente con otro usuario"}), 400

    user = User(
            name=request.json['nombre'],
            last_name=request.json['apellido'],
            user=request.json['username'],
            password=request.json['password'],
            rol='user',
            create_user='system'
            )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.user)
    return jsonify(token=token), 200

@app.route('/recuperarcontrasenia',methods=['POST'])
def recuperarContrasenia():
    if not request.is_json:
        return jsonify({"msg": "Falta JSON en la solicitud"}), 400

    userreq = request.json['username']
    passreq = request.json['password']
    
    if not userreq:
        return jsonify({"msg": "Se requiere un usuario"}), 400
    if not passreq:
        return jsonify({"msg": "Se requiere una contraseña"}), 400

    userdb = User.query.filter_by(user=userreq).first()

    if userdb is None:
        return jsonify({"msg": "Usuario No existe"}), 400
    
    userdb.password = User.nueva_password(passreq)

    db.session.commit()

    return jsonify({"msg": "Password modificado"}), 200

@app.route('/registerAdmin',methods=['POST'])
def registerAdmin():

    userreq = request.json.get('username', None)
    userdb = User.query.filter_by(user=userreq).first()

    if userdb is not None and userdb.user:
        return jsonify({"msg": "Usuario ya existe, intente con otro usuario"}), 400

    user = User(
            name=request.json['nombre'],
            last_name=request.json['apellido'],
            user=request.json['username'],
            password=request.json['password'],
            rol=request.json['rol']
            )

    db.session.add(user)
    db.session.commit()
    
    return jsonify(msg='Usuario creado exitoasamente'), 200

# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/registrarjuego',methods=['POST'])
def registrarJuego():

    juego = Juego(
        nombre = request.json['nombre'],
        anio = request.json['anio'],
        precio = request.json['precio'],
        foto = request.json['foto'],
        banner = request.json['banner'],
        descripcion = request.json['descripcion'],
        create_user = 'admin',
    )

    db.session.add(juego)
    db.session.commit()

    return jsonify(msg='Juego agregado correctamente!!!'), 200

@app.route('/getJuegos',methods=['GET'])
def getJuegos():
    return Juego.getJuegos()

@app.route('/getJuego/<id>',methods=['GET'])
def getJuego(id):
    #idreq = request.json['id']
    return Juego.getJuego(int(id))

db.init_app(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
