"""Module with application entry point."""
from os import getenv

from flask import jsonify

from api.middlewares.token_required import token_required
from main import create_app
from config import config
from seeders import seed_db

# get flask config name from env or default to production config
config_name = getenv('FLASK_ENV', default='production')

# create application object
app = create_app(config[config_name])


@app.route('/')
@token_required
def index():
    """Process / routes and returns 'Welcome to the AM api' as json."""
    return jsonify(dict(message='Welcome to the AM api'))

@app.route('/health')
def health_check():
    """Checks the health of application and returns 'Health App Server' as json."""
    return jsonify(dict(message='Healthy App Server')), 200

@app.cli.command()
def seed_database():
    seed_db()


if __name__ == '__main__':
    app.run()
