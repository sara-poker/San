from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.report.utils import *
from apps.test.models import Isp # مطمئن شو این ایمپورت درسته

class Command(BaseCommand):
    help = "Clears old cache and rebuilds stats for Dashboard and ISPs"

    def handle(self, *args, **options):
        # ۱. پاکسازی کامل کش قبل از شروع
        self.stdout.write("🧹 Clearing old cache...")
        cache.clear()
        self.stdout.write(self.style.SUCCESS("✅ Cache cleared!"))

        # ۲. کش کردن داشبورد کل
        self.stdout.write("⏳ Rebuilding global dashboard cache...")
        try:
            global_data = calculate_report_dashboard_data()
            cache.set("global:dashboard_data", global_data, timeout=86400)
            self.stdout.write(self.style.SUCCESS("✅ Dashboard cache rebuilt!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error in dashboard cache: {e}"))

        # ۳. کش کردن تک‌تک ISPها
        isps = Isp.objects.all()
        for isp in isps:
            self.stdout.write(f"⏳ Caching stats for ISP: {isp.name}")
            try:
                isp_data = calculate_isp_stats(isp.id)
                if isp_data:
                    cache_key = f"isp:stats:{isp.id}"
                    cache.set(cache_key, isp_data, timeout=86400)
                    self.stdout.write(self.style.SUCCESS(f"✅ Cached stats for ISP: {isp.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error in ISP {isp.name}: {e}"))

        self.stdout.write(self.style.SUCCESS("🚀 All caches rebuilt successfully at 2:00 AM!"))
