from django.shortcuts import render
from django.views.generic import TemplateView


class SearchIndexView(TemplateView):
    template_name = "search.html"
