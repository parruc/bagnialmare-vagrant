from django.conf.urls import patterns, url
from views import BagniView, BagnoView, ServiceView, SearchView, HomepageView, CityView
from django.utils.translation import ugettext_lazy as _


urlpatterns = patterns(
    '',
    url(r'^$',
        HomepageView.as_view(),
        name="homepage",
        ),
    url(_(r'^bagni/$'),
        BagniView.as_view(),
        name="bagni",
        ),
    url(_(r'^bagno/(?P<slug>[-\w]+)/$'),
        BagnoView.as_view(),
        name="bagno"
        ),
    url(_(r'^search/$'),
        SearchView.as_view(),
        name="search"
        ),
    url(_(r'^services/(?P<slug>[-\w]+)/$'),
        ServiceView.as_view(),
        name="service"
        ),
    url(_(r'^city/(?P<slug>[-\w]+)/$'),
        CityView.as_view(),
        name="city"
        ),
)
