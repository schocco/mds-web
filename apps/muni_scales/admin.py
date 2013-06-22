from models import UXCscale, UDHscale
from django.contrib import admin

class UXCscaleAdmin(admin.ModelAdmin):
    pass

class UDHscaleAdmin(admin.ModelAdmin):
    pass

admin.site.register(UXCscale, UXCscaleAdmin)
admin.site.register(UDHscale, UDHscaleAdmin)