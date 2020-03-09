from flask import Flask
from config import DevConfig, Config
from flaskext.mysql import MySQL
from flask_wtf.csrf import CsrfProtect


# instantiate flask app
app = Flask(__name__)

# apply configuration
app.config.from_object(DevConfig)

# instantiate a MySQL database server object
mysql = MySQL()

mysql.init_app(app)
csrf = CsrfProtect(app)

# import routes
from app import routes
