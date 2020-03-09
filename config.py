import os
SECRET_KEY = b'\xca|\xd96\xc33|L\xf7P\x978\xc0\x05\x9e\x980\xd4\xf9\xd9C?\xea\x96'
class Config(object): SECRET_KEY =os.environ.get('SECRET_KEY') 

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
