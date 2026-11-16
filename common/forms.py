"""Reusable form building blocks shared by every app."""
from django import forms


class BootstrapFormMixin:
    """Adds Bootstrap CSS classes to every widget of the form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()

    def _apply_bootstrap(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput)):
                continue
            css = 'form-select' if isinstance(widget, (forms.Select, forms.SelectMultiple)) else 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css}".strip()


class ReadOnlyFieldsMixin:
    """Disables the fields listed in `read_only_fields` (all fields if '__all__')."""

    read_only_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        names = self.fields if self.read_only_fields == '__all__' else self.read_only_fields
        for name in names:
            self.fields[name].disabled = True
            self.fields[name].help_text = 'This field cannot be changed.'
