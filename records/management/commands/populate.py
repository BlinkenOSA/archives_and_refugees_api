import os

import gspread
from django.core.management import BaseCommand
from oauth2client.service_account import ServiceAccountCredentials

from records.models import FilmLibraryRecord, Country, Director, Keyword


class Command(BaseCommand):
    help = 'Migrate FEC Records.'

    def handle(self, *args, **options):
        # FilmLibraryRecord.objects.all().delete()
        # Keyword.objects.all().delete()
        # Country.objects.all().delete()
        # Director.objects.all().delete()

        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.path.dirname(__file__), 'OSA - RefugeeVideos-0f7505da22e7.json'), scope)

        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('18VdrBZhbsVynHbsvMz3HdpnzYgZrUJruYdpXJh14WiI')
        worksheet = sheet.worksheet('2019 Film Library Additions')

        values = worksheet.get_all_values()

        for row_number in range(1, len(values)):
            columns = [
                'country_double_check',
                'trailer_url',
                'notes_for_trailer',
                'thumbnail',
                'notes_for_thumbnail',
                'title',
                'country',
                'abstract',
                'director',
                'temporal_coverage',
                'keywords',
                'keywords_to_use',
                'catalog',
                'notes'
            ]

            if row_number > 1:
                row = values[row_number]

                # New FL Record
                if row[columns.index('title')] != "":
                    fl, created = FilmLibraryRecord.objects.get_or_create(
                        title=row[columns.index('title')],
                        catalog_url=row[columns.index('catalog')]
                    )
                    fl.trailer_url = row[columns.index('trailer_url')]
                    fl.abstract = row[columns.index('abstract')]
                    fl.catalog_url = row[columns.index('catalog')]
                    fl.notes = row[columns.index('notes')]
                    fl.save()

                    # Director
                    directors = row[columns.index('director')].split(';')
                    for director in directors:
                        drctr, created = Director.objects.get_or_create(director=director.strip())
                        fl.directors.add(drctr)

                    # Keyword
                    keywords = row[columns.index('keywords')].split(';')
                    for keyword in keywords:
                        if keyword != "":
                            kwd, created = Keyword.objects.get_or_create(keyword=keyword.strip())
                            fl.keywords.add(kwd)

                    # Coverage
                    coverages = row[columns.index('temporal_coverage')].split('-')
                    if len(coverages) > 1:
                        if coverages[1] != "":
                            fl.temporal_coverage_end = coverages[1]
                    if coverages[0] != "":
                        fl.temporal_coverage_start = coverages[0]
                    fl.save()

                # Add Countries
                country, created = Country.objects.get_or_create(
                    country=row[columns.index('country')].strip()
                )

                # if country.latitude == 0 or country.latitude is None:
                #     time.sleep(10)
                #     g = geocoder.google(country)
                #     country.latitude, country.longitude = g.latlng if g.latlng else (0, 0)
                #    country.save()

                fl.countries.add(country)
                print("Adding FL title: %s" % unicode(fl.title))
