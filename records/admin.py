# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from records.models import FilmLibraryRecord, Country, Keyword, Director


class CountryRecordAdmin(admin.ModelAdmin):
    list_display = ('country', 'latitude', 'longitude')


class FilmLibraryRecordAdmin(admin.ModelAdmin):
    ordering = ('title',)
    filter_horizontal = ['countries', 'keywords', 'directors']
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    exclude = ('trailer_url', 'thumbnail_url')

admin.site.register(Country, CountryRecordAdmin)
admin.site.register(Keyword)
admin.site.register(Director)
admin.site.register(FilmLibraryRecord, FilmLibraryRecordAdmin)
