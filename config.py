import os

class Config(object):
    JWT_SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://eaoeqygshsnkgo:3c540987e672a3c656da7b7aeec69d8a8d1927362f3852abeb4e925975671cf4@ec2-107-22-241-205.compute-1.amazonaws.com:5432/d8v3itijlqgc7e'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = 'postgresql://erik:123@localhost:5432/flask_demo'
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'postgresql://erik:123@localhost:5432/flask_demo'