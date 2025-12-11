from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Avg
from django.shortcuts import redirect, get_object_or_404

from persiantools.jdatetime import JalaliDate

from web_project import TemplateLayout

from apps.test.models import Test, Isp, App
from apps.report.serializers import GetAllIspAPISerializer, PROVINCES_FA, GetAllAppAPISerializer , EndTestSerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        province_data = {}
        context['province_data'] = province_data

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


class ProvinceView(TemplateView):
    template_name = "province.html"

    def dispatch(self, request, *args, **kwargs):
        province = kwargs.get("pk")

        if province not in PROVINCES_FA:
            return redirect("/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        province = self.kwargs["pk"]
        speed_test = getattr(self.request, "_speed_test", {})

        test_success = Test.filter(status="Without Filter")

        name = PROVINCES_FA.get(province, province)

        data = []

        context["province"] = name
        return context


class IspView(TemplateView):
    template_name = "isp.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        isp = get_object_or_404(Isp, pk=self.kwargs['pk'])

        speed_test = Test.objects.filter(isp_id=self.kwargs['pk'])

        success_speed_test_list = speed_test.filter(status="Filter")
        success_speed_test = success_speed_test_list.count()
        fail_speed_test = speed_test.count() - success_speed_test

        success_speed_test_percent = round((success_speed_test * 100) / speed_test.count(), 2)
        fail_speed_test_percent = round((100 - success_speed_test_percent), 2)

        unique_users_ids = speed_test.values_list('user', flat=True).distinct()
        User = get_user_model()
        unique_users = User.objects.filter(id__in=unique_users_ids)

        unique_apps_ids = speed_test.values_list('app', flat=True).distinct()
        unique_apps = App.objects.filter(id__in=unique_apps_ids)

        context['isp'] = isp

        context['test_count'] = speed_test.count()
        context['success_speed_test'] = success_speed_test
        context['fail_speed_test'] = fail_speed_test
        context['success_speed_test_percent'] = success_speed_test_percent
        context['fail_speed_test_percent'] = fail_speed_test_percent

        context['apps_count'] = unique_apps.count
        context['unique_apps'] = list(unique_apps)

        context['users_count'] = unique_users.count()
        context['unique_users'] = list(unique_users)

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
