
from example_project_backend.settings import *

DATABASES['default']['HOST'] = 'example_db'
CACHEOPS_REDIS['host'] = 'redis'
CELERY_BROKER_URL = 'amqp://rabbitmq'

LOGS_LOCATION = '/var/log/example-project/'
LOG_VIEWER_FILES_DIR = '//var/log/example-project/'
LOGGING['handlers']['file']['filename'] = f'{LOGS_LOCATION}/info.log'
LOGGING['handlers']['celery_file']['filename'] = f'{LOGS_LOCATION}/info.log'
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [('redis', 6379)]
