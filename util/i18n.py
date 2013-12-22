from django.utils.encoding import force_unicode
from django.utils.functional import Promise
from django.utils import simplejson
from django.core.serializers import json
from tastypie.serializers import Serializer


class CustomJSONSerializer(Serializer):
    def to_json(self, data, options=None):
        options = options or {}

        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder)

    def from_json(self, content):
        data = simplejson.loads(content)
        return data