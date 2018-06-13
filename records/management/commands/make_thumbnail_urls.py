import urllib2

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from records.models import FilmLibraryRecord


class Command(BaseCommand):
    help = 'Make thumbnail URLs to video trailers.'

    def handle(self, *args, **options):
        fl_records = FilmLibraryRecord.objects.all()
        for fl_record in fl_records:
            if 'youtube' in fl_record.trailer_url:
                yt_id = fl_record.trailer_url.replace('https://www.youtube.com/watch?v=', '')
                fl_record.thumbnail_url = "https://img.youtube.com/vi/%s/hqdefault.jpg" % yt_id
            elif 'vimeo' in fl_record.trailer_url:
                vimeo_id = fl_record.trailer_url.replace('https://vimeo.com/', '')
                vimeo_api_url = 'http://vimeo.com/api/v2/video/%s.json' % vimeo_id
                r = requests.get(vimeo_api_url)
                if r.status_code == 200:
                    data = r.json()[0]
                    fl_record.thumbnail_url = data["thumbnail_large"]
                else:
                    print("Check video: %s - %s" % (fl_record.title, vimeo_id))
            else:
                page = urllib2.urlopen(fl_record.catalog_url)
                soup = BeautifulSoup(page, 'html.parser')
                cover = soup.find('img', attrs={'class': 'cover-image'})
                fl_record.thumbnail_url = "http://catalog.osaarchivum.org" + cover.get('src')
            fl_record.save()