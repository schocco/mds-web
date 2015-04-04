from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

DEFAULT_GROUP_NAME = "default_user"

def get_or_create_default_group():
    '''
    Returns the default user group. Creates a new group with permissions
    for UDHscale UXCscale and Trail if no such group exists.
    '''
    group, created = Group.objects.get_or_create(name=DEFAULT_GROUP_NAME)
    if(created):
        trail_ct = ContentType.objects.get(app_label="trails", model="trail")
        udh_ct = ContentType.objects.get(app_label="muni_scales", model="udhscale")
        uxc_ct = ContentType.objects.get(app_label="muni_scales", model="uxcscale")
    
        udh_perms = Permission.objects.filter(content_type=udh_ct)
        uxc_perms = Permission.objects.filter(content_type=uxc_ct)
        trail_perms = Permission.objects.filter(content_type=trail_ct)
        
        group.permissions.add(*udh_perms)
        group.permissions.add(*uxc_perms)
        group.permissions.add(*trail_perms)
        group.save()
    return group

def set_permissions(sender, **kw):
    user = kw["instance"]
    if kw.pop("created", False):
        user = kw.pop("instance")
        default_group = get_or_create_default_group()
        user.groups.add(default_group)
        user.save()
