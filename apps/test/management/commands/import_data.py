from django.core.management.base import BaseCommand
import json
import os
from django.utils import timezone
from datetime import datetime

from config.settings import BASE_DIR
from apps.test.models import Test


class Command(BaseCommand):
    help = 'Import test data from JSON file into the database'

    def handle(self, *args, **options):
        file_path = BASE_DIR / 'data.json'

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File '{file_path}' not found."))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        for item in data:
            # Parse the date string to datetime objec

            Test.objects.create(
                date=item['date'],
                city=item['city'],
                app_id=item['app_id'],
                isp_id=item['isp_id'],
                status=item['status'],
                user_id=item['user_id'],
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Test entry #{created_count} created."))

        self.stdout.write(self.style.SUCCESS(f"Import finished. {created_count} new records added."))
