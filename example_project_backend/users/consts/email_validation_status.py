from common.base_choices import BaseChoices


class EmailValidationStatus(BaseChoices):
    NOT_CHECKED = 'not_checked'
    VALID = 'valid'
    INVALID = 'invalid'
    CATCH_ALL = 'catch_all'
    UNKNOWN = 'unknown'
