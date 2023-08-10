from common.base_choices import BaseChoices


class BounceStatus(BaseChoices):
    BOUNCE = 'bounced'
    NO_BOUNCE = 'did_not_bounce'
