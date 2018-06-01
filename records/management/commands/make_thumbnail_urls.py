import urllib2

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
            else:
                page = urllib2.urlopen(fl_record.catalog_url)
                soup = BeautifulSoup(page, 'html.parser')
                cover = soup.find('img', attrs={'class': 'cover-image'})
                fl_record.thumbnail_url = "http://catalog.osaarchivum.org" + cover.get('src')
            fl_record.save()