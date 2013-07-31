from apps.trails.load import gpx_to_linestring
from django.http import HttpResponse
import os
import tempfile

#TODO: auhtorization
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