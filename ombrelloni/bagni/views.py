from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import Bagno, Service

class BagniView(ListView):

    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagniView, self).get_context_data(**kwargs)
        return context

class BagnoView(DetailView):

    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagnoView, self).get_context_data(**kwargs)
        return context

class ServiceView(DetailView):

    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        return context
