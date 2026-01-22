from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from apps.report.utils import *


# مدل‌ها یا توابعی که محاسبات سنگین انجام میدن رو اینجا ایمپورت کن
# from your_app.utils import get_dashboard_stats, get_monthly_report


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ۱. کش کردن داشبورد کل (که قبلاً نوشتیم)
        self.stdout.write("⏳ Rebuilding global dashboard cache...")
        global_data = calculate_report_dashboard_data()
        cache.set("global:dashboard_data", global_data, timeout=86400)

        self.stdout.write(self.style.SUCCESS("✅ Dashboard cache rebuilt!"))

        # ۲. کش کردن تک‌تک ISPها
        isps = Isp.objects.all()
        for isp in isps:
            self.stdout.write(f"⏳ Caching stats for ISP: {isp.name}")
            isp_data = calculate_isp_stats(isp.id)
            if isp_data:
                cache_key = f"isp:stats:{isp.id}"
                cache.set(cache_key, isp_data, timeout=86400)
                self.stdout.write(self.style.SUCCESS(f"✅ Cached stats for ISP: {isp.name}"))

        self.stdout.write(self.style.SUCCESS("✅ All caches rebuilt successfully!"))
