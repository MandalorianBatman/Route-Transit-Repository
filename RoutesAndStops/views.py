from django.http.response import JsonResponse
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
        context = dict()
        if request.method == 'POST':
            if stop_id:
                stop_instance = Facade.get_stop_by_id(stop_id)
                form = StopsForm(request.POST, instance=stop_instance)
                if stop_instance.name != request.POST['name']:
                    Facade.update_stop_in_routes(stop_instance.name, request.POST['name'])
            else:
                form = StopsForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/views_stops')
            else:
                context['form'] = form
        elif stop_id:
            stop_instance = Facade.get_stop_by_id(stop_id)
            context['form'] = StopsForm(instance=stop_instance)
        else:
            context['form'] = StopsForm()
        return render(request, 'RoutesAndStops/Stops/stops.html', context=context)
    except Exception as e:
        print(e)
        return redirect('/views_stops')


def routes(request, route_id=None):
    try:
        context = dict()
        if request.method == 'POST':
            is_instance = request.POST.get('instance_id')
            route_instance = None
            if is_instance:
                route_instance = Facade.get_route_by_id(int(is_instance))
            form = RouteForm(request.POST, instance=route_instance)
            if form.is_valid():
                form.instance.list_of_stops = request.POST['stops_in_sequence']
                form.save()
                return redirect('/views')
            else:
                context['form'] = form
                context['list_of_stops'] = request.POST['stops_in_sequence'].split(',')
        elif route_id:
            route_instance = Facade.get_route_by_id(route_id)
            context['form'] = RouteForm(instance=route_instance)
            context['list_of_stops'] = route_instance.list_of_stops
            context['instance_id'] = route_id
        else:
            context['form'] = RouteForm()
        return render(request, 'RoutesAndStops/Routes/routes.html', context=context)
    except Exception as e:
        print(e)


def views(request):
    try:
        context = dict()
        context['Routes'] = Facade.get_all_routes()
        return render(request, 'RoutesAndStops/Routes/views.html', context=context)
    except Exception as e:
        print(e)


def view_stops(request):
    try:
        context = dict()
        context['Stops'] = Facade.get_all_stops()
        return render(request, 'RoutesAndStops/Stops/view_stops.html', context=context)
    except Exception as e:
        print(e)


def export_routes(request, export_type):
    try:
        response = Facade.export_route(export_type)
        return response
    except Exception as e:
        print(e)


def export_stops(request, export_type):
    try:
        response = Facade.export_stop(export_type)
        return response
    except Exception as e:
        print(e)


def import_routes(request):
    try:
        if request.method == 'POST':
            file_extension = request.FILES['routes'].name.split('.')[-1]
            if Facade.import_routes(request.FILES['routes'], file_extension):
                messages.success(request, 'Data uploaded successfully')
                return redirect('/routes')
            else:
                messages.warning(request, 'Upload error!!')
                return redirect('/routes')
    except Exception as e:
        print(e)
        messages.warning(request, 'File not Found')
        return redirect('/routes')


def import_stops(request):
    try:
        if request.method == 'POST':
            file_extension = request.FILES['stops'].name.split('.')[-1]
            if Facade.import_stops(request.FILES['stops'], file_extension):
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
    Facade.delete_route_by_id(route_id)
    return redirect('/views')


def delete_stop(request, stop_name):
    Facade.delete_stop_by_name(stop_name)
    return redirect('/views_stops')


def get_map(request, route_id):
    try:
        route = Facade.get_route_by_id(route_id)
        way_points = []
        for stop in route.list_of_stops:
            stop_instance = Facade.get_stop_by_name(stop)
            way_points.append({'lat': str(stop_instance.latitudes), 'lng': str(stop_instance.longitudes)})
        context = dict()
        context['route_name'] = route.name
        context['way_points'] = json.dumps(way_points)
        return render(request, 'RoutesAndStops/Routes/maps.html', context)
    except Exception as e:
        print(e)
        return redirect('/views')


def get_map_for_stop(request, stop_id):
    try:
        stop_instance = Facade.get_stop_by_id(stop_id)
        return render(request, 'RoutesAndStops/Stops/stop_on_map.html', {'stop': stop_instance})
    except Exception as e:
        print(e)
        return redirect('/views')


def get_multiple_routes(request):
    try:
        list_of_route_ids = list(map(int, request.POST.getlist('list_of_routes')))
        routes_list = Facade.get_multiple_routes_by_ids(list_of_route_ids)
        route_paths = dict()
        for route in routes_list:
            way_points = []
            for stop in route.list_of_stops:
                stop_instance = Facade.get_stop_by_name(stop)
                way_points.append({'lat': str(stop_instance.latitudes), 'lng': str(stop_instance.longitudes)})
            route_paths[route.name] = json.dumps(way_points)
        context = dict()
        context['route_paths'] = route_paths

        return render(request, 'RoutesAndStops/Routes/multiple_routes.html', context=context)
    except Exception as e:
        print(e)
        return redirect('/views')


def check_stop_in_routes(request):
    return JsonResponse(Facade.check_stop_in_routes(request.POST['stop']), safe=False)

