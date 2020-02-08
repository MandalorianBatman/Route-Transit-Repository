from django.http.response import HttpResponse
from tablib import Dataset
from django.shortcuts import redirect
from django.contrib import messages

from .models import Route, Stop
from .resources import RouteResource, StopResource, RouteResourceImport


class Facade:

    @classmethod
    def get_all_stops(cls):
        return Stop.objects.all()

    @classmethod
    def get_all_routes(cls):
        routes = Route.objects.all()
        for route in routes:
            route.list_of_stops = route.list_of_stops.split(',')
        return routes

    @classmethod
    def get_stop_by_id(cls, stop_id):
        try:
            return Stop.objects.get(id=stop_id)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_stop_by_name(cls, stop_name):
        try:
            return Stop.objects.get(name=stop_name)
        except Exception as e:
            print(e)
            return None

    @classmethod
    def get_route_by_id(cls, route_id):
        try:
            route = Route.objects.get(id=route_id)
            route.list_of_stops = route.list_of_stops.split(',')
            return route
        except Exception as e:
            print(e)
            return None

    @classmethod
    def export_route(cls, export_type):
        route_resource = RouteResource()
        dataset = route_resource.export()
        if export_type == 'csv':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Routes.csv"'
        else:
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Routes.xls"'
        return response

    @classmethod
    def export_stop(cls, export_type):
        stop_resource = StopResource()
        dataset = stop_resource.export()
        if export_type == 'csv':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stops.csv"'
        else:
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Stops.xls"'
        return response

    @classmethod
    def import_routes(cls, route_file):

        route_resource = RouteResourceImport()
        dataset = Dataset()
        imported_routes = dataset.load(route_file.read().decode('utf-8')[1:], format='csv')
        result = route_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            route_resource.import_data(dataset, dry_run=False)
            return True
        else:
            messages.warning(request, 'Upload error!!')
            return redirect('/routes')

    @classmethod
    def import_stops(cls, stop_file):
        stop_resource = StopResource()
        dataset = Dataset()
        imported_stops = dataset.load(stop_file.read().decode('utf-8'))
        result = stop_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            stop_resource.import_data(dataset, dry_run=False)
            return True
        else:
            messages.warning(request, 'Upload error!!')
            return redirect('/stops')

    @classmethod
    def delete_route_by_id(cls, route_id):
        return Route.objects.get(id=route_id).delete()

    @classmethod
    def delete_stop_by_id(cls, stop_id):
        return Stop.objects.get(id=stop_id).delete()

    @classmethod
    def get_multiple_routes_by_ids(cls, id_list):
        routes = Route.objects.filter(id__in=id_list)
        for route in routes:
            route.list_of_stops = route.list_of_stops.split(',')
        return routes
