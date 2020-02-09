from import_export import resources
from .models import Stop, Route


class StopResource(resources.ModelResource):
    class Meta:
        model = Stop


class RouteResource(resources.ModelResource):
    class Meta:
        model = Route

