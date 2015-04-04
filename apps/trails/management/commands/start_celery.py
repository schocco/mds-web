from celery.bin import celery
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    'Starts the celery service for local testing'
    help = 'Starts the celery service for local testing. Celery connects to local amqp.'

    def handle(self, *args, **options):
        argv = ["--app=mds_website", "worker", "-l", "info"]
        celery.main(argv)
        