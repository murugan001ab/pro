from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='12345'
    
    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)


    from .idcard import idc
    app.register_blueprint(idc)
    
    from .face import face
    app.register_blueprint(face)
    
    return app

