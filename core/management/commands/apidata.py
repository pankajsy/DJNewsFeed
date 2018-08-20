from django.core.management.base import BaseCommand, CommandError
import os, csv, json
from collections import OrderedDict

os.environ['DJANGO_SETTINGS_MODULE'] = 'ftsearch.settings'
from djauth.tasks import *

class Command(BaseCommand):
    help = "My test command"

    def handle(self, *args, **options):
        # testcsv()
        # apicollectdata.apply_async((), queue='cronjob')
        apicollectdata()
