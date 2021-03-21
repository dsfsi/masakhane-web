from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os, sqlite3

db = SQLAlchemy()
migrate = Migrate()
