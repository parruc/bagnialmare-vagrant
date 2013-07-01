from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
admin.autodiscover()

sqs = SearchQuerySet().facet('services')

urlpatterns = i18n_patterns('',
    #Bagni urls
    url(_(r'^bagni/'), include('bagni.urls')),
    url(_(r'^search/'), include('haystack.urls')),
    url(r'^advanced_search/$', FacetedSearchView(
            template="search/advanced_search.html",
            form_class=FacetedSearchForm,
            searchqueryset=sqs),
        name='haystack.views.haystack_search')
)

urlpatterns += patterns(

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
