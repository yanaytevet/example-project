from django.db.models import CharField, JSONField
from django.forms import MultipleChoiceField, CheckboxSelectMultiple


class ListFieldWithChoices(JSONField):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', [])
        self.default = kwargs.get('default')
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': MultipleChoiceField,
            'choices': self.choices,
            'widget': CheckboxSelectMultiple,
            'initial': self.default,
            **kwargs
        }
        return super(self).formfield(**defaults)
