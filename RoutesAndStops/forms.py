from django import forms
from RoutesAndStops.models import Route, Stop
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit


class RouteForm(forms.ModelForm):
    list_of_stops = forms.ModelMultipleChoiceField(queryset=Stop.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-6 mr-3'),
                Column('status', css_class='col-5 ml-3'),
            ),
            Row(
                Column('direction', css_class='col-6 mr-3'),
                Column('type', css_class='col-5 ml-3'),
            ),
            Row(
                Column('list_of_stops', css_class='col-6 mr-4'),
                Column(
                    HTML("""<label for="sort_stops">Selected stops (drag to rearrange)</label>
                        <div id="sort_stops"></div><input hidden name="stops_in_sequence" id="stops_in_sequence">""")
                ),
            ),
            Submit('submit', 'Submit')
        )

    class Meta:
        model = Route
        fields = ('name', 'direction', 'status', 'type')


class StopsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-11 ml-4')
            ),
            Row(
                Column('latitudes', css_class='col-5 mr-5 ml-4'),
                Column('longitudes', css_class='col-5 ml-4')
            ),
            Submit('submit', 'Submit', css_class='ml-4')
        )

    class Meta:
        model = Stop
        fields = '__all__'
