import geocoder
import time
from django.core.management import BaseCommand

from records.models import  Country


class Command(BaseCommand):
    help = 'Geocode FEC Records.'

    def handle(self, *args, **options):
        countries = Country.objects.iterator()

        for country in countries:
            if country.latitude == 0 or country.latitude is None:
                # time.sleep(10)
                g = geocoder.arcgis(country.country)
                country.latitude, country.longitude = g.latlng if g.latlng else (0, 0)
                country.save()
                print("Geocoding country: %s" % country.country)
