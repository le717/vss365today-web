import os

from dotenv import dotenv_values, find_dotenv
from sqlalchemy import create_engine

# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


alchemy = SQLAlchemy()
csrf = CSRFProtect()
db = None
# email = Mail()


def init_extensions(app):
    global db

    # Load the variables from the .env file into the app config
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        app.config[key] = (value if value != "" else None)

    # Load app exensions
    csrf.init_app(app)
    # email.init_app(app)

    # Set the database connection
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/vss365"
    alchemy.init_app(app)
    db = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    db.connect()
