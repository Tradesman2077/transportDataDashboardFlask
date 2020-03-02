# Test flask-mysql app

This is a skeleton Flask-MySQL application.

## Installation

First rename `config.py.example` -> `config.py`

### With Docker

To run the app with Docker you need docker-compose version 3,

+ Open `config.py` and edit `DockerDevConfig` with your MySQL credentials
+ Save and close the file
+ Now do,

		docker-compose up -d

+ To stop the containers,

		docker-compose stop

### Without Docker

To run it from a local Python environment and local MySQL database install, 

1. Install dependencies in your python environment

		pip3 install -r requirements.txt

2. Ensure you have a MySQL database install running on port 3306
3. Open `config.py` and edit `DevConfig` with your MySQL credentials
4. Open `__init__.py` and change `DockerDevConfig` to `DevConfig`
5. Then do,

		python run.py

Other configuration options are possible if you edit `config.py` with a new configuration.

**Do not commit/push your `config.py` file.**