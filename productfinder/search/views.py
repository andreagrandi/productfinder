import requests
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from .client import get_products


class SearchIndexView(TemplateView):
    template_name = "search.html"

    def post(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        search_terms = request.POST.get('search-terms', None)

        if search_terms:
            search_terms = search_terms.split(' ')
            results = get_products(search_terms)
            context = {'search_results': results}
            return render_to_response('results.html', context=context)
