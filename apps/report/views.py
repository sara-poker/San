from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Avg
from django.shortcuts import redirect

from persiantools.jdatetime import JalaliDate

from web_project import TemplateLayout

from apps.test.models import Test, Isp
from apps.report.serializers import GetAllIspAPISerializer, PROVINCES_FA

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

        tests = Test.objects.all().order_by('-id')

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

        isp = Isp.objects.filter(pk=self.kwargs['pk']).first()

        speed_test = Test.objects.filter(isp_id=self.kwargs['pk'])

        success_speed_test_list = speed_test.filter(status="Without Filter")
        success_speed_test = success_speed_test_list.count()
        fail_speed_test = speed_test.count() - success_speed_test

        # success_speed_test_percent = round((success_speed_test * 100) / speed_test.count(), 2)
        # fail_speed_test_percent = round((100 - success_speed_test_percent), 2)



        unique_users_ids = speed_test.values_list('user', flat=True).distinct()
        User = get_user_model()
        unique_users = User.objects.filter(id__in=unique_users_ids)


        context['isp'] = isp


        context['test_count'] = speed_test.count()
        context['success_speed_test'] = success_speed_test
        context['fail_speed_test'] = fail_speed_test
        context['success_speed_test_percent'] = 0
        context['fail_speed_test_percent'] = 0


        context['max_download_speed'] = 0
        context['min_download_speed'] = 0
        context['avg_download_speed'] = 0


        context['max_upload_speed'] = 0
        context['min_upload_speed'] = 0
        context['avg_upload_speed'] = 0


        context['max_ping_speed'] = 0
        context['min_ping_speed'] = 0
        context['avg_ping_speed'] = 0


        context['max_jitter_speed'] = 0
        context['min_jitter_speed'] = 0
        context['avg_jitter_speed'] = 0

        context['ips_count'] = 0
        context['unique_ips'] = list([])

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


