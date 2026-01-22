from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from apps.test.models import Test


class Command(BaseCommand):
    help = "Generate fake Test data and insert into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Number of fake records to generate",
        )

    def handle(self, *args, **options):
        count = options["count"]

        base_date = timezone.make_aware(
            datetime(2023, 1, 20, 7, 22, 7)
        )

        max_days_after = 7

        objects = []

        for _ in range(count):
            random_date = base_date + timedelta(
                days=random.randint(0, max_days_after),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )

            status = "Filter" if random.random() < 0.9 else "Without Filter"

            objects.append(
                Test(
                    date=random_date,
                    city="تهران",
                    status=status,
                    app_id=random.choice([1, 2]),
                    isp_id=random.choice([1, 2]),
                    user_id=random.choice([1, 2]),
                )
            )

        Test.objects.bulk_create(objects, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} fake Test records successfully created."
            )
        )
