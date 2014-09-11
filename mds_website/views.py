from django.views.generic.base import TemplateView

from apps.muni_scales.api import MscaleResource
from apps.auth.api import UserResource


class HomeView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['current_user'] = self.user_detail()
        context['mscale_collection'] = self.get_mscale_collection()
        return context
    
    def get_mscale_collection(self):
        '''
        Returns all MscaleObjects as json string.
        '''
        res = MscaleResource()
        request_bundle = res.build_bundle(request=self.request)
        obj_lst = res.obj_get_list(request_bundle)
        obj_lst = res.apply_sorting(obj_lst)
     
        bundles = []
        for obj in obj_lst:
            bundle = res.build_bundle(obj=obj, request=self.request)
            bundles.append(res.full_dehydrate(bundle, for_list=True))
        json = res.serialize(None, bundles, "application/json")
        return json
        
    def user_detail(self):
        '''
        Return the request user as json string
        '''
        ur = UserResource()
        ur_bundle = ur.build_bundle(obj=self.request.user, request=self.request)
        json = ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')
        return json
