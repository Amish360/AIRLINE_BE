# myapp/management/commands/load_airlines.py

import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from flights_api.models import Airline


logger = logging.getLogger('myapp')

class Command(BaseCommand):
    help = 'Load airlines from a TSV file'

    def handle(self, *args, **kwargs):
        file_path = 'data/data.tsv'
        batch_size = 1000
        airlines = []

        logger.info('Starting to load airline data from %s', file_path)

        with open(file_path, newline='') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter='\t')
            for row in reader:
                airlines.append(
                    Airline(
                        code=row['code'],
                        name=row['name']
                    )
                )
                if len(airlines) >= batch_size:
                    self._bulk_insert(airlines)
                    logger.info('Inserted a batch of %d airlines', len(airlines))
                    airlines = []

            if airlines:
                self._bulk_insert(airlines)
                logger.info('Inserted the final batch of %d airlines', len(airlines))

        logger.info('Successfully loaded all airline data')

    def _bulk_insert(self, airlines):
        with transaction.atomic():
            Airline.objects.bulk_create(airlines, batch_size=len(airlines))
            for airline in airlines:
                logger.debug('Loaded airline: %s', airline)