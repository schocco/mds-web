from apps.trails.models import Trail
from django.contrib import admin

class TrailAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trail, TrailAdmin)