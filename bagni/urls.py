from django.conf.urls import patterns, url
from views import BagniView
from views import BagnoView
from views import ServiceView
from views import ServicesView
from views import SearchView
from views import HomepageView
from views import MunicipalityView
from views import MunicipalitiesView
from views import DistrictView
from views import DistrictsView
from views import GlobalMapView
from views import BenveView
from views import Benve2View
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns(
    '',
    url(r'^$',
        HomepageView.as_view(),
        name="homepage",),
    url(_(r'^bagni/$'),
        BagniView.as_view(),
        name="bagni",),
    url(_(r'^bagno/(?P<slug>[-\w]+)/$'),
        BagnoView.as_view(),
        name="bagno"),
    url(_(r'^search/$'),
        SearchView.as_view(),
        name="search"),
    url(_(r'^services/$'),
        ServicesView.as_view(),
        name="services"),
    url(_(r'^services/(?P<slug>[-\w]+)/$'),
        ServiceView.as_view(),
        name="service"),
    url(_(r'^municipality/(?P<slug>[-\w]+)/$'),
        MunicipalityView.as_view(),
        name="municipality"),
    url(_(r'^municipalities/$'),
        MunicipalitiesView.as_view(),
        name="municipalities"),
    url(_(r'^district/(?P<slug>[-\w]+)/$'),
        DistrictView.as_view(),
        name="district"),
    url(_(r'^districts/$'),
        DistrictsView.as_view(),
        name="districts"),
    url(_('^globalmap/$'),
        GlobalMapView.as_view(),
        name="globalmap"),
    url(_('^benve/$'),
        BenveView.as_view(),
        name="benve"),
    url(_('^benve2/$'),
        Benve2View.as_view(),
        name="benve2"),
)
