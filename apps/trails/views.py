from django.contrib.gis.geos import MultiLineString
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
import os
import tempfile

from apps.trails.load import GPXReader


#TODO: auhtorization
def load_gpx(request):
    if request.method == 'POST':
        gpx_file = request.FILES['gpx']
        ls = None
        # return object serialized to whatever is specified using tastypie functions
        if(gpx_file.name.lower().endswith(".gpx") or gpx_file.name.lower().endswith(".xml")
           and gpx_file.size < 10000):        
            filehandle, tmpath = tempfile.mkstemp(suffix=".gpx")
            with open(tmpath, 'wb+') as destination:
                for chunk in gpx_file.chunks():
                    destination.write(chunk)
            #get linestring
            ls = GPXReader(tmpath)
            # clean up
            os.remove(tmpath)      
            return HttpResponse(MultiLineString(ls.to_linestring().simplify(tolerance=0.00002)).geojson)
    # raise http error
    return HttpResponseBadRequest("only gpx/xml files smaller than 10,000 bytes are allowed.")
    
#def user_detail(request, username):
#    ur = UserResource()
#    user = ur.obj_get(username=username)
#
#    # Other things get prepped to go into the context then...
#
#    ur_bundle = ur.build_bundle(obj=user, request=request)
#    return render_to_response('myapp/user_detail.html', {
#        # Other things here.
#        "user_json": ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json'),
#    })