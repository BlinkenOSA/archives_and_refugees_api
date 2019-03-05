import os
import shutil

import gspread
from django.conf import settings
from django.core.management import BaseCommand
from oauth2client.service_account import ServiceAccountCredentials

from records.models import FilmLibraryRecord, Country, Director, Keyword


class Command(BaseCommand):
    help = 'Organize thumbnails.'

    def handle(self, *args, **options):
        scope = ['https://spreadsheets.google.com/feeds']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            os.path.join(os.path.dirname(__file__), 'OSA - RefugeeVideos-0f7505da22e7.json'), scope)

        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('18VdrBZhbsVynHbsvMz3HdpnzYgZrUJruYdpXJh14WiI')
        worksheet = sheet.worksheet('Film Library')

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
                if row[columns.index('thumbnail')] != "":
                    fl = FilmLibraryRecord.objects.filter(title=row[columns.index('title')]).first()
                    source = os.path.join(settings.MEDIA_ROOT, 'thumbnail', 'withName', row[columns.index('thumbnail')])
                    destination = os.path.join(settings.MEDIA_ROOT, 'thumbnail', '%04d.jpg' % fl.id)

                    if os.path.exists(source):
                        shutil.move(source, destination)
                        print('File %s was moved' % source)
                        fl.thumbnail.name = os.path.join('thumbnail', '%04d.jpg' % fl.id)
                    else:
                        print('Wrong source file: %s' % source)
