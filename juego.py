from flask import jsonify
import datetime

from db import db, ma

subs = db.Table('juego_categoria',
                db.Column('juego_id', db.Integer, db.ForeignKey('juego.id')),
                db.Column('categoria_id', db.Integer, db.ForeignKey('categoria.id'))
                )

class Juego(db.Model):
    __tablename__='juego'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    anio = db.Column(db.Integer)
    precio = db.Column(db.Float)
    foto = db.Column(db.String(1000))
    banner = db.Column(db.String(1000))
    descripcion = db.Column(db.Text)
    create_user = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    categorias = db.relationship('Categoria',secondary=subs,backref=db.backref('categorizados',lazy='dynamic'))
    
    def __init__(self,nombre,anio,precio,foto,banner,descripcion,create_user):
        self.nombre = nombre
        self.anio = anio
        self.precio = precio
        self.foto = foto
        self.banner = banner
        self.descripcion = descripcion
        self.create_user = create_user

    def getJuegos():
        mensaje = ''
        try:
            juegos_db = Juego.query.all()
            juego_schema = JuegoSchema(many=True)
            output = juego_schema.dump(juegos_db)
            mensaje = 'Ok'
        except Exception as ex:
            mensaje = 'error: ' + str(ex)
            output = {}
        return jsonify({'mensaje':mensaje,'data':output})

    def getJuego(id):
        mensaje = ''
        try:
            juego_db = Juego.query.filter_by(id=id).first()
            juego_schema = JuegoSchema()
            output = juego_schema.dump(juego_db)
            mensaje = 'Ok'
        except Exception as ex:
            mensaje = 'error: ' + str(ex)
            output = {}
        return jsonify({'mensaje':mensaje,'data':output})

class JuegoSchema(ma.Schema):
    class Meta:
        fields = ('id','nombre','anio','precio','foto','banner','descripcion')


class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100))
    create_user = db.Column(db.String(20))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self,descripcion,create_user):
        self.descripcion = descripcion
        self.create_user = create_user




