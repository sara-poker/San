from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404

from web_project import TemplateLayout

from apps.test.models import Test, Isp, App
from apps.setup.models import *


class ProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        test_qs = Test.objects.filter(user=self.request.user)

        # تعداد موفق و ناموفق
        success_count = test_qs.filter(status="Without Filter").count()
        fail_count = test_qs.filter(status="Filter").count()

        # اضافه به context
        context['success_count'] = success_count
        context['fail_count'] = fail_count
        context['device_info_list'] = []
        context['network_info_list'] = []

        return context


class SetupAppView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # دریافت اپلیکیشن مورد نظر
        app = get_object_or_404(App, id=self.kwargs['pk'])

        context['app'] = app
        context['countries'] = Country.objects.all()
        context['platforms'] = App.PLATFORM_CHOICE
        context['fees'] = App.CHOICE
        return context

    def post(self, request, *args, **kwargs):
        app = get_object_or_404(App, id=self.kwargs['pk'])

        app.name = request.POST.get('name')
        app.platform = request.POST.get('platform')
        app.maker = request.POST.get('maker')

        country_id = request.POST.get('country')
        if country_id:
            app.country = Country.objects.get(id=country_id)

        app.normal_user_fee = request.POST.get('normal_user_fee')

        app.save()
        return redirect(request.path)


class SetupIspView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # دریافت اطلاعات اپراتور (ISP)
        isp_instance = get_object_or_404(Isp, id=self.kwargs['pk'])

        context['isp'] = isp_instance
        context['countries'] = Country.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        isp_instance = get_object_or_404(Isp, id=self.kwargs['pk'])

        # استخراج داده‌ها از فرم ارسال شده
        isp_instance.name = request.POST.get('name')
        isp_instance.url = request.POST.get('url')
        isp_instance.org = request.POST.get('org')
        isp_instance.as_number = request.POST.get('as_number')
        isp_instance.asname = request.POST.get('asname')

        country_id = request.POST.get('country')
        if country_id:
            isp_instance.country = Country.objects.get(id=country_id)

        isp_instance.save()

        # ریدایرکت به همان صفحه برای مشاهده تغییرات
        return redirect(request.path)


class UserDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        User = get_user_model()
        user = User.objects.filter(id=self.kwargs['pk'])

        test_qs = Test.objects.filter(user=self.kwargs['pk'])

        # تعداد موفق و ناموفق
        success_count = test_qs.filter(status=True).count()
        fail_count = test_qs.filter(status=False).count()

        # اضافه به context
        context['user'] = user[0]
        context['success_count'] = success_count
        context['fail_count'] = fail_count
        context['device_info_list'] = []
        context['network_info_list'] = []

        return context


class UsersTableView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        User = get_user_model()
        users = User.objects.exclude(id=self.request.user.id)

        context['users'] = users
        return context
