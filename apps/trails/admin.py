from models import Trail, WayPoint
from django.contrib import admin

class TrailAdmin(admin.ModelAdmin):
    pass

class WayPointAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trail, TrailAdmin)
admin.site.register(WayPoint, WayPointAdmin)