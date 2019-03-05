from django.conf.urls import url
from records.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Refugee Docs Map API",
      default_version='v1',
      description="API endpoints for the maps of documentaries.",
      contact=openapi.Contact(email="bonej@ceu.edu"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^countries/$', CountryListView.as_view(), name='countries'),
    url(r'^keywords/$', KeywordListView.as_view(), name='keywords'),
    url(r'^directors/$', DirectorListView.as_view(), name='directors'),
    url(r'^films/$', FilmLibraryRecordListView.as_view(), name='films'),
    url(r'^films/temporal_coverage/$', FilmDateRangeView.as_view(), name='films_temporal_coverage'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

