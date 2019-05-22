from django.core.management import BaseCommand

from records.models import FilmLibraryRecord


class Command(BaseCommand):
    help = 'Make embed URLs to video trailers.'

    def handle(self, *args, **options):
        fl_records = FilmLibraryRecord.objects.all()
        for fl_record in fl_records:
            if not fl_record.trailer_embed_url:
                if 'youtube' in fl_record.trailer_url:
                    fl_record.trailer_embed_url = fl_record.trailer_url.replace('https://www.youtube.com/watch?v=',
                                                                                'https://www.youtube.com/embed/')
                    fl_record.save()
                if 'vimeo' in fl_record.trailer_url:
                    fl_record.trailer_embed_url = fl_record.trailer_url.replace('https://vimeo.com',
                                                                                 'https://player.vimeo.com/video')
                    fl_record.save()