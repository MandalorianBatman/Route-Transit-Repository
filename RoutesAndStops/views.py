from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
import json


from .Facade import Facade
from .forms import StopsForm, RouteForm


def home_view(request):
    return render(request, 'RoutesAndStops/homepage.html')


def stops(request, stop_id=None):
    try:
        facade = Facade()
        facade.get_all_stops()
        context = dict()
        if request.method == 'POST':
            if stop_id:
                stop_instance = facade.get_stop_by_id(stop_id)
                form = StopsForm(request.POST, instance=stop_instance)
            else:
                form = StopsForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                context['form'] = form
        elif stop_id:
            stop_instance = facade.get_stop_by_id(stop_id)
            context['form'] = StopsForm(instance=stop_instance)
        else:
            context['form'] = StopsForm()
        return render(request, 'RoutesAndStops/stops.html', context=context)
    except Exception as e:
        print(e)
        return redirect('/views_stops')


def routes(request, route_id=None):
    try:
        facade = Facade()
        context = dict()
        if request.method == 'POST':
            is_instance = request.POST.get('instance_id')
            route_instance = None
            if is_instance:
                route_instance = facade.get_route_by_id(int(is_instance))
            form = RouteForm(request.POST, instance=route_instance)
            if form.is_valid():
                form.instance.list_of_stops = request.POST['stops_in_sequence']
                form.save()
                return redirect('/views')
            else:
                context['form'] = form
                context['list_of_stops'] = request.POST['stops_in_sequence'].split(',')
        elif route_id:
            route_instance = facade.get_route_by_id(route_id)
            context['form'] = RouteForm(instance=route_instance)
            context['list_of_stops'] = route_instance.list_of_stops
            context['instance_id'] = route_id
        else:
            context['form'] = RouteForm()
        return render(request, 'RoutesAndStops/routes.html', context=context)
    except Exception as e:
        print(e)


def views(request):
    try:
        context = dict()
        facade = Facade()
        context['Routes'] = facade.get_all_routes()
        return render(request, 'RoutesAndStops/views.html', context=context)
    except Exception as e:
        print(e)


def view_stops(request):
    try:
        context = dict()
        facade = Facade()
        context['Stops'] = facade.get_all_stops()
        return render(request, 'RoutesAndStops/view_stops.html', context=context)
    except Exception as e:
        print(e)


def export_routes(request, export_type):
    try:
        facade = Facade()
        response = facade.export_route(export_type)
        return response
    except Exception as e:
        print(e)


def export_stops(request, export_type):
    try:
        facade = Facade()
        response = facade.export_stop(export_type)
        return response
    except Exception as e:
        print(e)


def import_routes(request):
    try:
        if request.method == 'POST':
            if Facade.import_routes(request.FILES['routes.csv']):
                messages.success(request, 'Data uploaded successfully')
                return redirect('/routes')
        else:
            messages.warning(request, 'Upload error!!')
            return redirect('/routes')
    except Exception as e:
        messages.warning(request, 'Upload error!!')
        return redirect('/routes')


def import_stops(request):
    try:
        if request.method == 'POST':
            if Facade.import_stops(request.FILES['stops.csv']):
                messages.success(request, 'Data uploaded successfully')
                return redirect('/stops')
        else:
            messages.warning(request, 'Upload error!!')
            return redirect('/stops')
    except Exception as e:
        print(e)
        messages.warning(request, 'Upload error!!')
        return redirect('/stops')


def delete_route(request, route_id):
    facade = Facade()
    facade.delete_route_by_id(route_id)
    return redirect('/views')


def delete_stop(request, stop_id):
    facade = Facade()
    facade.delete_stop_by_id(stop_id)
    return redirect('/views_stops')


def get_map(request, route_id):
    facade = Facade()
    route = facade.get_route_by_id(route_id)
    way_points = []
    for stop in route.list_of_stops:
        stop_instance = facade.get_stop_by_name(stop)
        way_points.append({'lat': str(stop_instance.latitudes), 'lng': str(stop_instance.longitudes)})
    context = dict()
    context['route_name'] = route.name
    context['way_points'] = json.dumps(way_points)

    return render(request, 'RoutesAndStops/maps.html', context)

def get_map_polyline(request):
    return render(request, 'RoutesAndStops/all_routes_polyline.html')