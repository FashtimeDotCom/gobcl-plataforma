# django
from django import forms
from django.forms import HiddenInput

# forms
from form_utils.forms import BetterModelForm
from parler.forms import BaseTranslatableModelForm


setattr(
    forms.fields.Field, 'is_checkbox',
    lambda self: isinstance(self.widget, forms.CheckboxInput)
)


class BaseModelForm(BetterModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.DateInput):
                field.widget.attrs['class'] = (
                    'date-picker form-control vDateField')
            elif isinstance(field.widget, forms.widgets.DateTimeInput):
                field.widget.attrs['class'] = 'datetime-picker form-control'
            elif isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.EmailInput):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.widgets.TextInput):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()


class TranslatableModelForm(BaseModelForm, BaseTranslatableModelForm):
    pass
