from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from apps.report.utils import *


# مدل‌ها یا توابعی که محاسبات سنگین انجام میدن رو اینجا ایمپورت کن
# from your_app.utils import get_dashboard_stats, get_monthly_report

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("⏳ Calculating dashboard data...")

        # اجرای محاسبات سنگین
        data = calculate_report_dashboard_data()

        # ذخیره در کش برای ۲۴ ساعت
        cache.set("report:dashboard_data", data, timeout=86400)

        self.stdout.write(self.style.SUCCESS("✅ Dashboard cache rebuilt!"))
