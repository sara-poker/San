from django.http import Http404
from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Exists, OuterRef, Avg, Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.core.cache import cache

from persiantools.jdatetime import JalaliDate

from web_project import TemplateLayout

from apps.test.models import Test, Isp, App
from apps.report.serializers import *
from apps.report.utils import *

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework import status as drf_status


class HasValidSecretKey(BasePermission):
    message = "Invalid or missing secret key."

    def has_permission(self, request, view):
        secret = request.headers.get("X-SECRET-KEY")

        if not secret:
            return False

        return secret == 'IZIQ3PI5M3M7QoLT7nQEoz5-aEGj_fDxJpdriSeWx1XsWgXiPPaqCGLIHdQKm6WODcS2qVSkUtj8SIZlQjOfmCJ2itcT'


def convert_date(date):
    date = date.replace(" ", "")
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    return year + month + day


def convert_date2(date):
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return year + "/" + month + "/" + day


def filter_date(date, queryset):
    selected_date_str = date.split("تا")
    if len(selected_date_str) == 2:
        start_date = convert_date(selected_date_str[0])
        end_date = convert_date(selected_date_str[1])
    else:
        start_date = convert_date(selected_date_str[0])
        end_date = start_date

    return queryset.filter(date__range=(start_date, end_date)).order_by('date')


def filter_date_year(date, queryset):
    date = int(date)
    if date == 0:
        return queryset
    start_date = date
    end_date = start_date + 10000

    return queryset.filter(date__gte=start_date, date__lte=end_date).order_by('date')


def filter_vpn(vpn, queryset):
    if vpn == "0":
        return queryset
    return queryset.filter(vpn_id=vpn)


def filter_country_server(country_server, queryset):
    if country_server == "0":
        return queryset
    return queryset.filter(server_country=country_server)


def filter_province(province, queryset):
    return queryset.filter(city=province)


def filter_country(country, queryset):
    if country == "0":
        return queryset
    return queryset.filter(vpn__vpn_country=country)


def filter_operator(oprator, queryset):
    return queryset.filter(oprator__in=oprator)


# Create your views here.
class ReportDashboardsView(TemplateView):
    template_name = "your_template.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        cached_data = cache.get("report:dashboard_data")

        if not cached_data:
            cached_data = calculate_report_dashboard_data()
            cache.set("report:dashboard_data", cached_data, timeout=86400)

        context.update(cached_data)

        return context


class TestTableView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        tests = Test.objects.all().order_by('-date')

        context['tests'] = tests
        return context


class TestDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        test = Test.objects.get(pk=self.kwargs['pk'])

        context['test'] = test
        context["speed_MBps"] = 80
        context["upload_speed_MBps"] = 20
        return context


class IspView(TemplateView):
    template_name = "isp.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        isp_id = self.kwargs['pk']

        cache_key = f"isp:stats:{isp_id}"

        cached_data = cache.get(cache_key)

        if not cached_data:
            cached_data = calculate_isp_stats(isp_id)
            if cached_data:
                cache.set(cache_key, cached_data, timeout=86400)
            else:
                raise Http404("No data for this ISP")

        print("isp cached_data>>", cached_data)

        context.update(cached_data)

        context['isp'] = get_object_or_404(Isp, pk=isp_id)

        return context

        return context


class AppView(TemplateView):
    template_name = "app.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        app = get_object_or_404(App, pk=self.kwargs['pk'])
        test = Test.objects.filter(app_id=self.kwargs['pk'])

        filter_test_list = test.filter(status="Filter")
        fliter_test_count = filter_test_list.count()
        without_fliter_test_count = test.count() - fliter_test_count

        filter_test_percent = round((fliter_test_count * 100) / test.count(), 2)
        without_fliter_test_percent = round((100 - filter_test_percent), 2)

        unique_users_ids = test.values_list('user', flat=True).distinct()
        User = get_user_model()
        unique_users = User.objects.filter(id__in=unique_users_ids)

        unique_isp_ids = test.values_list('isp', flat=True).distinct()
        unique_isps = Isp.objects.filter(id__in=unique_isp_ids)

        context['app'] = app

        context['test_count'] = test.count()
        context['success_speed_test'] = fliter_test_count
        context['fail_speed_test'] = without_fliter_test_count
        context['success_speed_test_percent'] = filter_test_percent
        context['fail_speed_test_percent'] = without_fliter_test_percent

        context['isp_count'] = unique_isps.count()
        context['unique_isp'] = list(unique_isps)

        context['users_count'] = unique_users.count()
        context['unique_users'] = list(unique_users)

        return context


class GetAllIspAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        isp_with_test = Test.objects.filter(
            isp=OuterRef('pk')
        )

        isp = Isp.objects.annotate(
            has_test=Exists(isp_with_test)
        ).filter(has_test=True).order_by('id')

        serializer = GetAllIspAPISerializer(isp, many=True)
        return Response(serializer.data)


class GetAllAppAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        app = App.objects.filter().order_by('name')

        serializer = GetAllAppAPISerializer(app, many=True)
        return Response(serializer.data)


class GetEndRecordAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        end_test = Test.objects.all().order_by('-id')[:50]
        end_test = end_test[::-1]
        end_test_serializer = EndTestSerializer(end_test, many=True)
        return Response(end_test_serializer.data)


class AddRecordAPIView(APIView):
    permission_classes = [HasValidSecretKey]

    @transaction.atomic
    def post(self, request):
        serializer = AddRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        app_name = serializer.validated_data["app"]
        isp_name = serializer.validated_data["isp"]
        city = serializer.validated_data["city"]
        record_status = serializer.validated_data["status"]

        # --- App (case-insensitive, race-safe)
        app_obj = (
            App.objects
            .select_for_update()
            .filter(name__iexact=app_name)
            .first()
        )
        if not app_obj:
            app_obj = App.objects.create(name=app_name)

        # --- ISP (case-insensitive, race-safe)
        isp_obj = (
            Isp.objects
            .select_for_update()
            .filter(name__iexact=isp_name)
            .first()
        )
        if not isp_obj:
            isp_obj = Isp.objects.create(name=isp_name)

        # --- Create Test record
        test = Test.objects.create(
            date=timezone.now(),
            city=city,
            status=record_status,
            app=app_obj,
            isp=isp_obj,
            user_id=2,
        )

        return Response(
            {
                "id": test.id,
                "date": test.date,
                "city": test.city,
                "status": test.status,
                "app": {
                    "id": app_obj.id,
                    "name": app_obj.name,
                },
                "isp": {
                    "id": isp_obj.id,
                    "name": isp_obj.name,
                },
                "user_id": 2,
            },
            status=drf_status.HTTP_201_CREATED,
        )
