from django.conf import settings
from django.core.cache import cache
from django.db.models import Exists, OuterRef

from apps.test.models import Test, Isp
from apps.report.serializers import PROVINCES_FA

import json
import requests

from web_project.template_helpers.theme import TemplateHelper

API_BASE = settings.BASE_URL


menu_file = {
    "menu": [
        {
            "name": "پیشخوان",
            "icon": "menu-icon tf-icons ti ti-layout-dashboard",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "index",
                    "name": "نمای کلی",
                    "slug": "dashboard-analytics"
                }
            ]
        },
        {
            "name": "تست اتصال",
            "icon": "menu-icon tf-icons ti ti-plug-connected",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "tests_table",
                    "name": "لیست تست ها",
                    "slug": "tests_table"
                }
            ]
        },
        {
            "name": "نرم افزار ها و اپراتور ها",
            "icon": "menu-icon tf-icons ti ti-stack",
            "slug": "setting",
            "submenu": [
                {
                    "url": "app",
                    "name": "لیست اپلیکیشن ها",
                    "slug": "app",
                    "pk": 1
                },
{
                    "url": "isp",
                    "name": "لیست اپراتور ها",
                    "slug": "isp",
                    "pk": 1
                }

            ]
        },
        {
            "name": "تنظیمات",
            "icon": "menu-icon tf-icons ti ti-settings",
            "slug": "setting",
            "submenu": [
                {
                    "url": "profile",
                    "name": "پروفایل",
                    "slug": "profile",
                },
                {
                    "url": "usersTable",
                    "name": "جدول کاربران",
                    "slug": "users_table"
                }
            ]
        },
        {
            "name": "پشتیبانی",
            "icon": "menu-icon tf-icons ti ti-help",
            "slug": "support",
            "submenu": [
                {
                    "url": "support",
                    "name": "ارسال تیکت",
                    "slug": "support"
                }
            ]
        }
    ]
}

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON
        menu_data = menu_file

        # Updated context with menu_data
        context.update({"menu_data": menu_data})
