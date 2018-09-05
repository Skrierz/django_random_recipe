from django.shortcuts import get_list_or_404
from django.http import Http404
from django.views import generic
from recipes.models import Dish


class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'search_result'

    def get_queryset(self):
        if self.request.method == 'GET':
            search_request = self.request.GET.get('search_box')
            if search_request is None:
                raise Http404
            try:
                search_result = get_list_or_404(Dish,
                                                name__icontains=search_request)
            except Http404:
                search_result = 'Not found'
            print(search_request)
            return search_result
