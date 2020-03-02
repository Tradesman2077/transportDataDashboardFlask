from flask import Flask
from config import DevConfig, Config
from flaskext.mysql import MySQL

# instantiate flask app
app = Flask(__name__)

# apply configuration
app.config.from_object(DevConfig)

# instantiate a MySQL database server object
mysql = MySQL()
# configure access to the database server
mysql.init_app(app)

# import routes
from app import routes
