from django.conf.urls import patterns, url
from views import BagniView, BagnoView, ServiceView
#from django.conf.urls.i18n import i18n_patterns
#from django.utils.translation import ugettext_lazy as _




urlpatterns = patterns('',

    url(r'^$',
        BagniView.as_view(),
        name="bagni",
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        BagnoView.as_view(),
        name="bagno"
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        ServiceView.as_view(),
        name="service"
    ),
)
