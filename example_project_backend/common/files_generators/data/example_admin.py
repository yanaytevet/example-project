from common.admin_utils.register_models_to_admin import ModelRegisterer
from example_app import models

ModelRegisterer(models).register()
