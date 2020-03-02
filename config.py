import os

class Config(object): SECRET_KEY =os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# edit and use this config if you are running app in docker
class DockerDevConfig(object):
    SECRET_KEY = "my super secret key".encode('utf8')
    MYSQL_DATABASE_HOST = 'testapp-mysql'
    MYSQL_DATABASE_USER = 'user'
    MYSQL_DATABASE_PASSWORD = 'password'
    MYSQL_DATABASE_DB = 'testapp'
    DEBUG = True

# edit and use this config if you are running app locally
class DevConfig(object):
    SECRET_KEY = "my super secret key".encode('utf8')
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_USER = 'christopherwright'
    MYSQL_DATABASE_PASSWORD = 'Blagger11'
    MYSQL_DATABASE_DB = 'transportdb'
    DEBUG = True
