# your_app/utils.py
from django.db.models import Count, Q
from apps.test.models import Test, Isp, App
from apps.report.serializers import *


def calculate_report_dashboard_data():
    """محاسبه تمام داده‌های سنگین داشبورد"""
    base_qs = Test.objects.filter(status="Filter")

    # توابع کمکی برای جلوگیری از تکرار کد
    def get_app_by_order(order_by_c):
        app_id = base_qs.values("app").annotate(c=Count("app")).order_by(order_by_c).first()
        if app_id:
            # تبدیل به دیکشنری برای کش شدن بهتر و بهینه‌تر
            app = App.objects.only("id", "name").get(pk=app_id["app"])
            return {"id": app.id, "name": app.name}
        return None

    def get_isp_by_order(order_by_c):
        isp_id = base_qs.values("isp").annotate(c=Count("isp")).order_by(order_by_c).first()
        if isp_id:
            isp = Isp.objects.only("id", "name", "as_number").get(pk=isp_id["isp"])
            return {"id": isp.id, "name": isp.name, "as_number": isp.as_number}
        return None

    # محاسبات اپلیکیشن و ISP
    data = {
        'best_app': get_app_by_order("-c"),
        'bad_app': get_app_by_order("c"),
        'best_isp': get_isp_by_order("-c"),
        'bad_isp': get_isp_by_order("c"),
    }

    # محاسبات نقشه استان‌ها
    qs = (
        Test.objects
        .filter(city__isnull=False)
        .values('city')
        .annotate(
            total_count=Count('id'),
            filter_count=Count('id', filter=Q(status='Filter'))
        )
    )

    def categorize(v):
        if v <= 100:
            return 'very_fast'
        if v <= 75:
            return 'fast'
        if v <= 50:
            return 'middle'
        if v <= 25:
            return 'slow'
        return 'no-data'

    province_data = {}
    for row in qs:
        province_fa = row['city']
        total = row['total_count']
        filtered = row['filter_count']
        if total == 0: continue

        province_en = PROVINCES_FA_REVERSED.get(province_fa)
        if not province_en: continue

        percentage = round((filtered / total) * 100, 2)
        province_data[province_en] = {
            'avg': percentage,
            'category': categorize(percentage)
        }

    data['province_data'] = province_data
    return data
