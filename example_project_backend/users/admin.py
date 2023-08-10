from common.admin_utils.register_models_to_admin import ModelRegisterer
from users import models

ModelRegisterer(models).register()

