
class Config():
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SECRET_KEY = "thisissecret"
    SECURITY_PASSWORD_SALT = 'salt'
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    timezone='Asia/Kolkata'
    REDIS_URL = "redis://localhost:6379"
    broker_connection_retry_on_startup=True
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3   
    
class DevelopmentConfig(Config):
    DEBUG = True