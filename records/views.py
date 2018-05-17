# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from records.models import Country, Keyword, Director, FilmLibraryRecord
from records.serializers import CountrySerializer, KeywordSerializer, DirectorSerializer, FilmLibraryRecordSerializer


class CountryListView(ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all().order_by('country')
    pagination_class = None


class KeywordListView(ListAPIView):
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all().order_by('keyword')
    pagination_class = None


class DirectorListView(ListAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all().order_by('director')
    pagination_class = None


class FilmLibraryRecordListView(ListAPIView):
    serializer_class = FilmLibraryRecordSerializer
    queryset = FilmLibraryRecord.objects.all().order_by('title')
