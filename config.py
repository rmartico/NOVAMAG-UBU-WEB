import os

# Configuration parameters in SQLAlchemy

# Change to allow the upload to Heroku with its database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///novamag' # Ojo tengo distintos nombres de base de datos en los equipos.. #TODO
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = False


