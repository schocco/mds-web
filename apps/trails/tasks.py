from __future__ import absolute_import

import os

from celery import shared_task
from django.contrib.gis.geos.collections import MultiLineString

from apps.trails.load2 import GPXReader, GPXImportError


@shared_task(throws=(GPXImportError))
def get_linestring(tmpath):
    try:
        ls = GPXReader(tmpath)
        response = MultiLineString(ls.to_linestring().simplify(tolerance=0.00002)).geojson
        return response
    finally:
        os.remove(tmpath)

