from django.core.management.base import BaseCommand, CommandError
import os, csv, json
from collections import OrderedDict

os.environ['DJANGO_SETTINGS_MODULE'] = 'ftsearch.settings'
from djauth.tasks import topdata_apicollectdata

class Command(BaseCommand):
    help = "My test command"
    def handle(self, *args, **options):
        # apicollectdata.apply_async((), queue='cronjob')
        topdata_apicollectdata()
