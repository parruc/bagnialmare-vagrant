from django.conf.urls import patterns, url
from views import BagniView, BagnoView, ServiceView, SearchView
#from django.conf.urls.i18n import i18n_patterns
#from django.utils.translation import ugettext_lazy as _




urlpatterns = patterns('',

    url(r'^$',
        BagniView.as_view(),
        name="bagni",
    ),
    url(r'^search/$',
        SearchView.as_view(),
        name="search"
    ),
    url(r'^servizi/(?P<slug>[-\w]+)/$',
        ServiceView.as_view(),
        name="service"
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        BagnoView.as_view(),
        name="bagno"
    ),
)
