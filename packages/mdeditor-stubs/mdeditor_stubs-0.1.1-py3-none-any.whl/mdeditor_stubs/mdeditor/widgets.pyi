from .configs import MDConfig as MDConfig
from _typeshed import Incomplete
from django import forms

class MDEditorWidget(forms.Textarea):
    config: Incomplete
    def __init__(self, config_name: str = 'default', *args, **kwargs) -> None: ...
    def render(self, name, value, renderer: Incomplete | None = None, attrs: Incomplete | None = None): ... # type: ignore
    def build_attrs(self, base_attrs, extra_attrs: Incomplete | None = None, **kwargs): ...
    media: Incomplete
