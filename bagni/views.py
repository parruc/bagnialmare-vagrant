from django.core import paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.gis.geos import Point
from geopy import geocoders
from django.utils.translation import ugettext as _

from models import Bagno, Service, District, Municipality
from search import search


class BagniView(ListView):
    """ View for a list of bagni
    """
    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagniView, self).get_context_data(**kwargs)
        return context


class BagnoView(DetailView):
    """ Detail view for a single bagno
    """
    model = Bagno

    def get_context_data(self, **kwargs):
        context = super(BagnoView, self).get_context_data(**kwargs)
        return context


class ServiceView(DetailView):
    """ Detail view for a single service
    """
    model = Service

    def get_context_data(self, **kwargs):
        context = super(ServiceView, self).get_context_data(**kwargs)
        return context


class MunicipalityView(DetailView):
    """ Detail view for a single municipality
    """
    model = Municipality

    def get_context_data(self, **kwargs):
        context = super(MunicipalityView, self).get_context_data(**kwargs)
        return context


class DistrictView(DetailView):
    """ Detail view for a single district
    """
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictView, self).get_context_data(**kwargs)
        return context


class HomepageView(TemplateView):
    """ Homepage view with search form that points to the SearchView
    """

    template_name = "bagni/homepage.html"

    def get_context_data(self, **kwargs):
        pass


class SearchView(TemplateView):
    """ Search view, which accepts search queries via url, like google.
        accepts 2 params:
        * q is the full text query
        * f is the list of active filters narrowing the search
    """

    template_name = "bagni/search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        groups = ['services', 'languages']
        q = self.request.GET.get('q', "")
        page = self.request.GET.get('p', "1")
        loc = self.request.GET.get('l', "")
        place = point = None
#        if 'q' in self.request.GET and not q:
#            q = ""
#            messages.add_message(self.request, messages.WARNING,
#                                 _("Cant search for empty string"))
#            return {}
        if loc:
            g = geocoders.GoogleV3()
            try:
                matches = g.geocode(loc, exactly_one=False)
                place, (lat, lng) = matches[0]
                point = Point(lng, lat)
            except geocoders.google.GQueryError:
                messages.add_message(self.request, messages.INFO,
                                     _("Cant find place '%s', sorting by relevance" % loc))
            except Exception:
                #TODO: Log errror
                messages.add_message(self.request, messages.ERROR,
                                     _("Error in geocoding"))

        filters = self.request.GET.getlist('f', [])
        new_query_string = self.request.GET.copy()
        query = q or "*"
        raw_hits, facets = search(q=query, filters=filters, groups=groups,
                                  query_string=new_query_string,)
        hits = Bagno.objects.filter(id__in=[h['id'] for h in raw_hits])
        if point:
            hits = hits.distance(point).order_by('distance')
        hits_paginator = paginator.Paginator(hits, 10)
        try:
            hits = hits_paginator.page(page)
        except paginator.PageNotAnInteger:
            # If page is not an integer, deliver first page.
            hits = hits_paginator.page(1)
        except paginator.EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            hits = hits_paginator.page(hits_paginator.num_pages)
        has_get = self.request.method == 'GET'
        context.update({'q': q, 'l':loc, 'place': place, 'facets': facets, 'hits': hits, 'count': len(raw_hits), 'has_get': has_get })
        return context

class GlobalMapView(ListView):
    template_name = "bagni/globalmap.html"
    model = Bagno
    def get_context_data(self, **kwargs):
        context = super(GlobalMapView, self).get_context_data(**kwargs)
        return context

class BenveView(ListView):
    """ Simple view for Service listing everyone with his bagni
        TODO: Will soon be removed
    """
    template_name = "bagni/benve.html"
    model = Service
    def get_context_data(self, **kwargs):
        context = super(BenveView, self).get_context_data(**kwargs)
        return context
