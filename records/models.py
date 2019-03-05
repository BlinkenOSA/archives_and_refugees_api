# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class FilmLibraryRecord(models.Model):
    id = models.AutoField(primary_key=True)
    trailer_url = models.URLField(blank=True, null=True)
    trailer_embed_url = models.URLField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails/', null=True)
    title = models.CharField(max_length=300)
    abstract = models.TextField(blank=True, null=True)
    temporal_coverage_start = models.IntegerField(blank=True, null=True)
    temporal_coverage_end = models.IntegerField(blank=True, null=True)
    catalog_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    countries = models.ManyToManyField('records.Country')
    directors = models.ManyToManyField('records.Director')
    keywords = models.ManyToManyField('records.Keyword', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'film_library_records'


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=150, unique=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.country

    class Meta:
        db_table = 'countries'


class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'keywords'


class Director(models.Model):
    id = models.AutoField(primary_key=True)
    director = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.director

    class Meta:
        db_table = 'directors'
