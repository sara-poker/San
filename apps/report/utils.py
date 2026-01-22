from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
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
        if v is None:
            return 'no-data'

        if v <= 25:
            return 'slow'
        elif v <= 50:
            return 'middle'
        elif v <= 75:
            return 'fast'
        elif v <= 100:
            return 'very_fast'

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

    print("province_data>>", province_data)

    data['province_data'] = province_data
    return data


def calculate_isp_stats(isp_id):
    """محاسبه آمار اختصاصی برای یک ISP خاص"""
    isp = get_object_or_404(Isp, pk=isp_id)
    speed_test = Test.objects.filter(isp_id=isp_id)

    total_count = speed_test.count()
    if total_count == 0:
        return None

    success_speed_test = speed_test.filter(status="Filter").count()
    fail_speed_test = total_count - success_speed_test

    success_percent = round((success_speed_test * 100) / total_count, 2)
    fail_percent = round((100 - success_percent), 2)

    User = get_user_model()
    unique_users_ids = speed_test.values_list('user', flat=True).distinct()
    unique_users = list(
        User.objects.filter(id__in=unique_users_ids).values('id', 'username','name'))

    unique_apps_ids = speed_test.values_list('app', flat=True).distinct()
    unique_apps = list(App.objects.filter(id__in=unique_apps_ids).values('id', 'name'))

    return {
        'isp_name': isp.name,
        'isp_id': isp.id,
        'test_count': total_count,
        'success_speed_test': success_speed_test,
        'fail_speed_test': fail_speed_test,
        'success_speed_test_percent': success_percent,
        'fail_speed_test_percent': fail_percent,
        'apps_count': len(unique_apps),
        'unique_apps': unique_apps,
        'users_count': len(unique_users),
        'unique_users': unique_users,
    }
