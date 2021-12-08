from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.app_config")

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from commands import db_commands
    app.register_blueprint(db_commands)

    from controllers import registrable_controllers
    for controller in registrable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return jsonify(error.messages), 400

    return app
