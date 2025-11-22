from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model

from web_project import TemplateLayout

from apps.test.models import Test


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


