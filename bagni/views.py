from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.translation import ugettext as _

from models import Bagno, Service
from search import search

class BagniView(ListView):
    """View for a list of bagni
    """
    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagniView, self).get_context_data(**kwargs)
        return context

class BagnoView(DetailView):
    """Detail view for a single bagno
    """
    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagnoView, self).get_context_data(**kwargs)
        return context

class ServiceView(DetailView):
    """Detail view for a single service
    """
    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        return context


class SearchView(TemplateView):
    """
    Simple search view, which accepts search queries via url, like google.
    Use something like ?q=this+is+the+serch+term
    """

    template_name = "bagni/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        facets = ['city', 'services']
        q = self.request.GET.get('q', None)
        #fs = self.request.GET.getlist('f', None)
        fs = self.request.GET.getlist('f', None)
        filters = []
        for f in fs:
            filters.append(f.split(":",1))
        if q:
            query = q.replace('+', ' AND ').replace(' -', ' NOT ')
            context['hits'], context['facets'] = search(query, filters, facets)
            context['query'] = q
            context['filtered'] = fs
            context['old_qs'] = self.request.GET.urlencode(safe=":")
            return context
        messages.add_message(self.request, messages.WARNING,
                             _("Inserisci del testo nel box di ricerca"))
        return {}
