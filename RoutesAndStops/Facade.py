from django.http.response import HttpResponse
from tablib import Dataset
from django.shortcuts import redirect
from django.contrib import messages

from .models import Route, Stop
from .resources import RouteResource, StopResource


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
    def import_routes(cls, route_file, file_type):
        route_resource = RouteResource()
        dataset = Dataset()
        if file_type == 'csv':
            imported_routes = dataset.load(route_file.read().decode('utf-8'))
            result = route_resource.import_data(dataset, dry_run=True)  # Test the data import
        elif file_type == 'xls':
            imported_routes = dataset.load(route_file.read())
            result = route_resource.import_data(dataset, dry_run=True)  # Test the data import
        else:
            return False
        if not result.has_errors():
            route_resource.import_data(dataset, dry_run=False)
            return True
        else:
            return False

    @classmethod
    def import_stops(cls, stop_file, file_type):
        stop_resource = StopResource()
        dataset = Dataset()
        if file_type == 'csv':
            imported_stops = dataset.load(stop_file.read().decode('utf-8'))
            # result = stop_resource.import_data(dataset, dry_run=True)
        elif file_type == 'xls':
            imported_routes = dataset.load(stop_file.read())
        result = stop_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            stop_resource.import_data(dataset, dry_run=False)
            return True
        else:
            return False

    @classmethod
    def delete_route_by_id(cls, route_id):
        return Route.objects.get(id=route_id).delete()

    @classmethod
    def delete_stop_by_name(cls, stop_name):
        return Stop.objects.get(name=stop_name).delete()

    @classmethod
    def get_multiple_routes_by_ids(cls, id_list):
        routes = Route.objects.filter(id__in=id_list)
        for route in routes:
            route.list_of_stops = route.list_of_stops.split(',')
        return routes

    @classmethod
    def update_stop_in_routes(cls, old_name, new_name):
        try:
            for route in Route.objects.all():
                stops = route.list_of_stops.split(',')
                if old_name in stops:
                    for n, s in enumerate(stops):
                        if s == old_name:
                            stops[n] = new_name
                    Route.objects.filter(pk=route.pk).update(list_of_stops=','.join(stops))
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def check_stop_in_routes(cls, stop_name):
        routes = Route.objects.all()
        for route in routes:
            if stop_name in route.list_of_stops:
                return True
        return False
