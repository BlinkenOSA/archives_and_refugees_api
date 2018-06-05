from django.conf.urls import url
from records.views import *

urlpatterns = [
    url(r'^countries/$', CountryListView.as_view(), name='countries'),
    url(r'^keywords/$', KeywordListView.as_view(), name='keywords'),
    url(r'^directors/$', DirectorListView.as_view(), name='directors'),
    url(r'^films/$', FilmLibraryRecordListView.as_view(), name='films'),
    url(r'^films/temporal_coverage/$', FilmDateRangeView.as_view(), name='films_temporal_coverage')
]

