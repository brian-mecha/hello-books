from flask_api import FlaskAPI
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from api.models import RevokedTokens, db

from config import config_app

login_manager = LoginManager()
jwt = JWTManager()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config_app['development'])
    # app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    app.config['SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
    app.config['BCRYPT_LOG_ROUNDS'] = 15
    app.config['JWT_SECRET_KEY'] = '\xe3\x8cw\xbdx\x0f\x9c\x91\xcf\x91\x81\xbdZ\xdc$\xedk!\xce\x19\xaa\xcb\xb7~'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']

        return RevokedTokens.is_jti_blacklisted(jti)
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "Login is required to access this feature."


    return app
