"""RouteTransitRepository URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from RoutesAndStops import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home_view, name="home"),
    path('stops/', home_views.stops, name='stops'),
    path('stops/<int:stop_id>/', home_views.stops, name='stops_update'),
    path('routes/', home_views.routes, name='routes'),
    path('routes/<int:route_id>/', home_views.routes, name='routes_update'),
    path('views/', home_views.views, name='views'),
    path('views_stops/', home_views.view_stops, name='views_stops'),
    path('export_routes/<str:export_type>', home_views.export_routes, name='export_routes'),
    path('export_stops/<str:export_type>', home_views.export_stops, name='export_stops'),
    path('import_routes/', home_views.import_routes, name='import_routes'),
    path('import_stops/', home_views.import_stops, name='import_stops'),
    path('get_map/<int:route_id>', home_views.get_map),
    path('delete/<int:route_id>', home_views.delete_route),
    path('delete_stop/<int:stop_id>', home_views.delete_stop),
    path('get_map_polyline/', home_views.get_map_polyline),
    path('get_map_for_stop/<int:stop_id>', home_views.get_map_for_stop),


]
