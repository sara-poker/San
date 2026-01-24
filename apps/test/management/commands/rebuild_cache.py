import time
from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.report.utils import *
from apps.test.models import Isp, App


class Command(BaseCommand):
    help = "Clears all cache and rebuilds stats for Dashboard, ISPs, and Apps"

    def handle(self, *args, **options):
        start_time = time.time()

        # ۱. پاکسازی کامل (Wipe out everything)
        self.stdout.write("🧹 Cleaning up the cache table...")
        cache.clear()
        self.stdout.write(self.style.SUCCESS("✅ Cache is now empty."))

        # ۲. ریبیلد داشبورد کل
        self.stdout.write("⏳ Calculating Global Dashboard...")
        try:
            global_data = calculate_report_dashboard_data()
            cache.set("global:dashboard_data", global_data, timeout=86400)
            self.stdout.write(self.style.SUCCESS("✅ Global Dashboard cached."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Global Cache Failed: {e}"))

        # ۳. ریبیلد ISPها
        isps = Isp.objects.all()
        for isp in isps:
            try:
                isp_data = calculate_isp_stats(isp.id)
                if isp_data:
                    cache.set(f"isp:stats:{isp.id}", isp_data, timeout=86400)
                    self.stdout.write(f"   ✔ ISP: {isp.name} cached.")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ✘ ISP: {isp.name} failed: {e}"))

        # ۴. ریبیلد Appها
        apps = App.objects.all()
        for app in apps:
            try:
                app_data = calculate_app_stats(app.id)
                if app_data:
                    cache.set(f"app:stats:{app.id}", app_data, timeout=86400)
                    self.stdout.write(f"   ✔ App: {app.name} cached.")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ✘ App: {app.name} failed: {e}"))

        end_time = time.time()
        duration = round(end_time - start_time, 2)
        self.stdout.write(self.style.SUCCESS(f"🚀 Done! Rebuild completed in {duration} seconds."))
