from .configs import MDConfig as MDConfig
from _typeshed import Incomplete
from django.views import generic

MDEDITOR_CONFIGS: Incomplete

class UploadView(generic.View):
    def dispatch(self, *args, **kwargs): ...
    def post(self, request, *args, **kwargs): ...
