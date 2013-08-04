from django.conf.urls import patterns, url
from views import set_language

urlpatterns = patterns(
    '',
    url(r'^set_language$',
        set_language,
        name="set_language",
        ),
)
