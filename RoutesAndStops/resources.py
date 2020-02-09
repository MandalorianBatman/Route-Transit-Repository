from import_export import resources, fields
from .models import Stop, Route


class StopResource(resources.ModelResource):
    class Meta:
        model = Stop


class RouteResource(resources.ModelResource):
    type = fields.Field(
        attribute='get_type_display',
        column_name='type'
    )
    direction = fields.Field(
        attribute='get_direction_display',
        column_name='direction'
    )
    status = fields.Field(
        attribute='get_status_display',
        column_name='status'
    )
    class Meta:
        model = Route
        export_order = ['id', 'name', 'direction', 'status', 'list_of_stops', 'type']


class RouteResourceImport(resources.ModelResource):
    class Meta:
        model = Route

