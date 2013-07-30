from apps.trails.load import gpx_to_linestring
from django.http import HttpResponse
import os
import tempfile


def load_gpx(request):
    if request.method == 'POST':
        gpx_file = request.FILES['gpx']
        ls = None
        # return object serialized to whatever is specified using tastypie functions
        if(gpx_file.name.endswith(".gpx") or gpx_file.name.endswith(".xml")
           and gpx_file.size < 10000):        
            filehandle, tmpath = tempfile.mkstemp(suffix=".gpx")
            with open(tmpath, 'wb+') as destination:
                for chunk in gpx_file.chunks():
                    destination.write(chunk)
            #get linestring
            ls = gpx_to_linestring(tmpath)
            # clean up
            os.remove(tmpath)    
                  
        return HttpResponse(ls)
    else:
        # raise http error
        return HttpResponse(300)