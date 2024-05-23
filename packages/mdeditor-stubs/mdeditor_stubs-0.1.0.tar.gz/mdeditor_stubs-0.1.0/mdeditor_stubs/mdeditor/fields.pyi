from .widgets import MDEditorWidget as MDEditorWidget
from _typeshed import Incomplete
from django import forms
from django.db import models

class MDTextFormField(forms.fields.CharField):
    def __init__(self, config_name: str = 'default', *args, **kwargs) -> None: ...

class MDTextField(models.TextField):
    config_name: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def formfield(self, **kwargs): ...
