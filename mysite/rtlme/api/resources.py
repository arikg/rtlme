from tastypie.resources import ModelResource
from rtlme.models import Result


class ResultResource(ModelResource):
    class Meta:
        queryset = Result.objects.all()
        allowed_methods = ['get']