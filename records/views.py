# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

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

    def filter_country(self, queryset, name, value):
        return queryset.filter(countries=value)

    def filter_keyword(self, queryset, name, value):
        return queryset.filter(keywords=value)

    class Meta:
        model = FilmLibraryRecord
        fields = ['country', 'keyword']


class FilmLibraryRecordListView(ListAPIView):
    serializer_class = FilmLibraryRecordSerializer
    queryset = FilmLibraryRecord.objects.all().order_by('title')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = FilmLibraryRecordFilterClass
