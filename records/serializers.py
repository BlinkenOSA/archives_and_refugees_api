from rest_framework import serializers
from records.models import FilmLibraryRecord, Country, Keyword, Director
import urllib2
from bs4 import BeautifulSoup


class CountrySerializer(serializers.ModelSerializer):
    total_number_of_films = serializers.IntegerField(
        source='filmlibraryrecord_set.count',
        read_only='true'
    )

    class Meta:
        model = Country
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class FilmLibraryRecordSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True)
    keywords = KeywordSerializer(many=True)
    directors = DirectorSerializer(many=True)

    class Meta:
        model = FilmLibraryRecord
        fields = ['id', 'trailer_url', 'trailer_embed_url', 'thumbnail_url', 'thumbnail', 'title', 'abstract',
                  'temporal_coverage_start', 'temporal_coverage_end',
                  'catalog_url', 'notes', 'countries', 'keywords', 'directors']





