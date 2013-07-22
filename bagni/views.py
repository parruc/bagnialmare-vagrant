from django.http import Http404
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


class CityView(ListView):
    """Detail view for a single city
    """
    template_name = "bagni/city.html"
    model = Bagno
    allow_empty = False

    def _get_city(self):
        return self.kwargs.get('city', "")

    def get_queryset(self):
        city = self._get_city()
        if city:
            return self.model.objects.filter(city=city)
        raise Http404(_("No city specified"))

    def get_context_data(self, **kwargs):
        context = super(CityView, self).get_context_data(**kwargs)
        context.update({'city': self._get_city()})
        return context


class HomepageView(TemplateView):
    """Homepage view with search form that points to the SearchView
    """

    template_name = "bagni/homepage.html"

    def get_context_data(self, **kwargs):
        pass


class SearchView(TemplateView):
    """Simple search view, which accepts search queries via url, like google.
    accepts 2 params:
     * q is the full text query
     * f is the list of active filters narrowing the search
    """

    #FIXME: i would move this into urls.py - but maybe I'm wrong
    template_name = "bagni/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        groups = ['city', 'services']
        q = self.request.GET.get('q', None)
        filters = self.request.GET.getlist('f', [])
        new_query_string = self.request.GET.copy()
        if q == '':
            messages.add_message(self.request, messages.WARNING,
                                 _("Inserisci del testo nel box di ricerca"))
            return {}
        if q is not None:
            query = q.replace('+', ' AND ').replace(' -', ' NOT ')

            hits, facets = search(q=query, filters=filters, groups=groups,
                                  query_string=new_query_string)
            context.update({'query': q, 'facets': facets, 'hits': hits, 'count': len(hits)})
            return context
        return {}
