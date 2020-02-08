from django import forms
from RoutesAndStops.models import Route, Stop


class RouteForm(forms.ModelForm):
    # stops = [(stop.name, stop.name) for stop in Stop.objects.all()]
    list_of_stops = forms.ModelMultipleChoiceField(queryset=Stop.objects.all(), required=False)
    # list_of_stops = forms.MultipleChoiceField(choices=[(stop.name, stop.name) for stop in Stop.objects.all()], required=False)

    class Meta:
        model = Route
        fields = ('name', 'direction', 'status', 'type')

    # def __init__(self, *args, **kwargs):
    #     super().__init__()
    #     self.fields['name'].widget = forms.TextInput(attrs={
    #         'id': 'route_name_id',
    #         'name': 'route'
    #     })


class StopsForm(forms.ModelForm):
    class Meta:
        model = Stop
        fields = '__all__'
