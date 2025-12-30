from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def index_fbv(request):
    return render(request, 'index.html')

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Ali'
        return context