# myapp/management/commands/load_airports.py

import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from flights_api.models import Airport

logger = logging.getLogger('myapp')

class Command(BaseCommand):
    help = 'Load airports from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'data/data.csv'
        batch_size = 1000
        airports = []

        logger.info('Starting to load airport data from %s', file_path)

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                airports.append(
                    Airport(
                        code=row['code'],
                        name=row['name'],
                        city=row['city'],
                        country=row['country']
                    )
                )
                if len(airports) >= batch_size:
                    self._bulk_insert(airports)
                    logger.info('Inserted a batch of %d airports', len(airports))
                    airports = []

            if airports:
                self._bulk_insert(airports)
                logger.info('Inserted the final batch of %d airports', len(airports))

        logger.info('Successfully loaded all airport data')

    def _bulk_insert(self, airports):
        with transaction.atomic():
            Airport.objects.bulk_create(airports, batch_size=len(airports))
            for airport in airports:
                logger.debug('Loaded airport: %s', airport)