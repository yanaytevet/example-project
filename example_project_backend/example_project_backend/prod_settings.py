from example_project_backend.settings import *

DEBUG = False
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://example.yanaytevet.com', 'https://stage-example.yanaytevet.com']

DATABASES['default']['HOST'] = 'example_db'
CACHEOPS_REDIS['host'] = 'redis'
CELERY_BROKER_URL = 'amqp://rabbitmq'

MIDDLEWARE.append('example_project_backend.exception_middleware.ExceptionMiddleware')

# LOGGER
LOGS_LOCATION = '/var/log/example-project/'
LOG_VIEWER_FILES_DIR = '/var/log/example-project/'
LOGGING['handlers']['file']['filename'] = f'{LOGS_LOCATION}/info.log'
LOGGING['handlers']['celery_file']['filename'] = f'{LOGS_LOCATION}/info.log'

# CORS
CORS_ALLOWED_ORIGINS.extend([])
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [('redis', 6379)]
