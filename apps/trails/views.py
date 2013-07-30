from apps.trails.load import GPXMapping
from apps.trails.models import Trail
from django.http import HttpResponse
from django.contrib.gis.geos import LineString


def load_gpx(request):
    if request.method == 'POST':
        gpx_file = request.FILES['gpx']
        # get file path
        track_mapping = {'waypoints' : 'LINESTRING'}
        lm = GPXMapping(Trail, gpx_file, track_mapping, layer=1)
        lm.model.name = "temp"
        lm.save()
        # return object serialized to whatever is specified using tastypie functions
        return HttpResponse(200)
    else:
        # raise http error
        return HttpResponse(300)
