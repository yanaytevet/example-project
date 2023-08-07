
from example_project_backend.settings import *

DATABASES['default']['HOST'] = 'xperiti_db'
CACHEOPS_REDIS['host'] = 'redis'
CELERY_BROKER_URL = 'amqp://rabbitmq'
SELENIUM_BROKER_URL = 'http://selenium:4444/wd/hub'

LOGS_LOCATION = '/var/log/xperiti/'
LOG_VIEWER_FILES_DIR = '/var/log/xperiti/'
LOGGING['handlers']['file']['filename'] = f'{LOGS_LOCATION}/info.log'
LOGGING['handlers']['celery_file']['filename'] = f'{LOGS_LOCATION}/info.log'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [('redis', 6379)]
