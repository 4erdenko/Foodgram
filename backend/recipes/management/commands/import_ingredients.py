import csv

from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Imports ingredients from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', nargs=1, type=str, help='Path to the CSV file'
        )

    def handle(self, *args, **options):
        file_path = options['csv_file'][0]

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    ingredient_name, measurement_unit = row
                    Ingredient.objects.create(
                        name=ingredient_name, measurement_unit=measurement_unit
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully '
                            f'imported "'
                            f'{ingredient_name}"'
                        )
                    )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')
