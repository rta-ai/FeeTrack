import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fee_management.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

# Register blueprints
from blueprints.dashboard import dashboard_bp
from blueprints.courses import courses_bp
from blueprints.students import students_bp
from blueprints.expenses import expenses_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(courses_bp, url_prefix='/courses')
app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(expenses_bp, url_prefix='/expenses')

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
