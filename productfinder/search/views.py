import requests
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from .client import get_products


class SearchIndexView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        keywords = request.GET.get('keywords', None)

        if keywords:
            keywords = keywords.split(' ')

            try:
                results = get_products(keywords)
            except Exception as e:
                return render_to_response('error.html')

            context = {'search_results': results}
            return render_to_response('results.html', context=context)
        else:
            return render_to_response('search.html')
