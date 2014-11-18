from django.contrib.auth.models import User
from models import *
from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.base import LookupBase


class RecipeLookup(ModelLookup):
    model = Recipe
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(RecipeLookup, self).get_query(request, term)
        category1 = request.GET.get('category1', '')
        category2 = request.GET.get('category2', '')
        if category1:
        	results = results.filter(category1=category1)

        if category2:
            results = results.filter(category2=category2)

        return results

    def get_item_label(self, item):
        return item.name

    def get_item_value(self, item):
        return item.name

registry.register(RecipeLookup)
