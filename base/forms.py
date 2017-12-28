# django
from django import forms
from django.forms import HiddenInput

# forms
from form_utils.forms import BetterModelForm
from parler.forms import TranslatableModelForm


setattr(
    forms.fields.Field, 'is_checkbox',
    lambda self: isinstance(self.widget, forms.CheckboxInput)
)


def get_widget_class(widget):
    """
    Returns a widget's corresponding class
    """
    if isinstance(widget, forms.widgets.DateInput):
        widget.attrs['class'] = (
            'date-picker form-control vDateField'
        )
    elif isinstance(widget, forms.widgets.DateTimeInput):
        return 'datetime-picker form-control'
    elif isinstance(widget, forms.widgets.Textarea):
        return 'form-control'
    elif isinstance(widget, forms.widgets.EmailInput):
        return 'form-control'
    elif isinstance(widget, forms.widgets.TextInput):
        return 'form-control'
    else:
        return 'form-control'


class BaseModelForm(BetterModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = get_widget_class(field.widget)

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()


class TranslatableModelForm(TranslatableModelForm):
    def __init__(self, *args, **kwargs):
        super(TranslatableModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = get_widget_class(field.widget)

    def hide_field(self, field_name):
        self.fields[field_name].widget = HiddenInput()
