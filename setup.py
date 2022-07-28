from flask import Flask
from db_paths import path


def create_app():
    app = Flask(__name__)
    
    ENV = 'dev'

    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = path["gradebook"]
        app.config['SQLALCHEMY_BINDS'] = {
            'login':    path["login"],
            'utility':  path["utility"]
        }
    elif ENV == 'prod':
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'webaddress'
        app.config['SQLALCHEMY_BINDS'] = {
            'login':    'sqlite:///login-flask.db',
            'utility':  'sqlite:///utility.db'
        }
    else :
        print(f"Please select an environment:  developement or production.")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app