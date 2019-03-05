# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count, Q
from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.views import APIView

from records.models import Country, Keyword, Director, FilmLibraryRecord
from records.serializers import CountrySerializer, KeywordSerializer, DirectorSerializer, FilmLibraryRecordSerializer


class CountryListView(ListAPIView):
    serializer_class = CountrySerializer
    pagination_class = None
    queryset = Country.objects.all().order_by('country')


class KeywordListView(ListAPIView):
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all().order_by('keyword')
    pagination_class = None


class DirectorListView(ListAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all().order_by('director')
    pagination_class = None


class FilmLibraryRecordFilterClass(filters.FilterSet):
    keyword = filters.ModelChoiceFilter(label='Keyword', queryset=Keyword.objects.all(), method='filter_keyword')
    country = filters.ModelChoiceFilter(label='Country', queryset=Country.objects.all(), method='filter_country')
    date_from = filters.NumberFilter(label='Temporal Coverage From', method='filter_date_from')
    date_to = filters.NumberFilter(label='Temporal Coverage To', method='filter_date_to')

    def filter_country(self, queryset, name, value):
        return queryset.filter(countries=value)

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(keywords=value)

    def filter_date_from(self, queryset, name, value):
        return queryset.exclude(
            Q(temporal_coverage_end__lt=value)
        )

    def filter_date_to(self, queryset, name, value):
        return queryset.exclude(
            Q(temporal_coverage_start__gt=value)
        )

    class Meta:
        model = FilmLibraryRecord
        fields = ['country', 'keyword']


class FilmLibraryRecordListView(ListAPIView):
    serializer_class = FilmLibraryRecordSerializer
    queryset = FilmLibraryRecord.objects.all().\
        prefetch_related('countries', 'directors', 'keywords').order_by('title')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = FilmLibraryRecordFilterClass


class FilmDateRangeView(APIView):
    def get(self, request, format=None):
        earliest_film = FilmLibraryRecord.objects.filter(temporal_coverage_start__isnull=False).order_by('temporal_coverage_start').first()
        latest_film = FilmLibraryRecord.objects.filter().order_by('-temporal_coverage_end').first()
        return Response({'earliest': earliest_film.temporal_coverage_start, 'latest': latest_film.temporal_coverage_end})