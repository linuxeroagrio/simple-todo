import os
from dotenv import load_dotenv

load_dotenv()


def build_database_uri():
    """Construye la URI de la base de datos a partir de variables de entorno individuales."""
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '5432')
    db_name = os.environ.get('DB_NAME')
    
    if all([db_user, db_password, db_name]):
        return f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return None


class Config:
    """Configuración base de la aplicación."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuración para ambiente de desarrollo con SQLite."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = build_database_uri() or 'sqlite:///todo.db'


class ProductionConfig(Config):
    """Configuración para ambiente de producción con PostgreSQL."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    
    @classmethod
    def init_app(cls, app):
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise ValueError(
                'Las variables DB_USER, DB_PASSWORD y DB_NAME son requeridas en producción'
            )


class TestingConfig(Config):
    """Configuración para pruebas con SQLite en memoria."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtiene la configuración según la variable de entorno FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
