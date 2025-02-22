from django.db import transaction
import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from api.models import Country
from ...models import LocalUnit, LocalUnitType


class Command(BaseCommand):
    help = "Import LocalUnits data from CSV"
    missing_args_message = "Filename is missing. Filename / path to CSV file required. Required headers in CSV: distr_code, GOadm2code, ADM2"

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options['filename'][0]
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                # Without positions we can't use the row:
                if not row['LONGITUDE'] or not row['LATITUDE']:
                    continue
                if len(row['POSTCODE']) > 10:
                    row['POSTCODE'] = ''  # better then inserting wrong textual data
                unit = LocalUnit()
                unit.country = Country.objects.get(iso3=row['ISO3'])
                if   row['TYPECODE'] == 'NS0': row['TYPECODE'] = 1
                elif row['TYPECODE'] == 'NS1': row['TYPECODE'] = 2
                elif row['TYPECODE'] == 'NS2': row['TYPECODE'] = 3
                elif row['TYPECODE'] == 'NS3': row['TYPECODE'] = 4
                else: row['TYPECODE'] = int(row['TYPECODE'])
                unit.type, created = LocalUnitType.objects.all().get_or_create(
                    level=row['TYPECODE'],
                    # name=row['TYPENAME'] -- we should create it in advance, not this way.
                )
                if created:
                    print(f'New LocalUnitType created: {unit.type.name}')

                unit.local_branch_name = row['NAME_LOC']
                unit.english_branch_name = row['NAME_EN']
                unit.postcode = row['POSTCODE'].strip()[:10]
                unit.address_loc = row['ADDRESS_LOC']
                unit.address_en = row['ADDRESS_EN']
                unit.city_loc = row['CITY_LOC']
                unit.city_en = row['CITY_EN']
                unit.focal_person_loc = row['FOCAL_PERSON_LOC']
                unit.focal_person_en = row['FOCAL_PERSON_EN']
                unit.phone = row['TELEPHONE'].strip()[:30]
                unit.email = row['EMAIL']
                unit.link = row['WEBSITE']
                unit.source_en = row['SOURCE_EN']
                unit.source_loc = row['SOURCE_LOC']
                unit.location = Point(float(row['LONGITUDE']), float(row['LATITUDE']))
                unit.save()
                name = unit.local_branch_name if unit.local_branch_name else unit.english_branch_name
                city = unit.city_loc if unit.city_loc else unit.city_en
                if name:
                    print(f'{i} | {name} saved')
                elif city:
                    print(f'{i} | ** {city} city location saved')
                else:
                    print(f'{i} | *** entity with ID saved')
