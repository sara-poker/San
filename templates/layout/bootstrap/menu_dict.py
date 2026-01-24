menu_manager = {
    "menu": [
        {
            "url": "index",
            "name": "پیشخوان",
            "icon": "menu-icon tf-icons ti ti-layout-dashboard",
            "slug": "dashboard-analytics"
        },
        {
            "name": "لیست اطلاعات",
            "icon": "menu-icon tf-icons ti ti-report",
            "slug": "reports",
            "submenu": [
                {
                    "url": "tests_table",
                    "name": "لیست تست ها",
                    "slug": "tests_table"
                },
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
            "name": "مدیریت سامانه",
            "icon": "menu-icon tf-icons ti ti-settings",
            "slug": "setting",
            "submenu": [
                {
                    "url": "#",
                    "external": True,
                    "name": "مدیریت اپراتور ها",
                    "slug": "test",
                },
                {
                    "url": "#",
                    "external": True,
                    "name": "مدیریت نرم افزار ها",
                    "slug": "test",
                },
                {
                    "url": "usersTable",
                    "name": "جدول کاربران",
                    "slug": "users_table"
                }
            ]
        },
        {
            "name": "حساب من",
            "icon": "menu-icon tf-icons ti ti-user-circle",
            "slug": "support",
            "submenu": [
                {
                    "url": "profile",
                    "name": "نمای کاربری",
                    "slug": "profile",
                },
                {
                    "url": "support",
                    "name": "ارسال تیکت",
                    "slug": "support"
                }
            ]
        }
    ]
}

menu_admin = {
    "menu": [
        {
            "url": "index",
            "name": "پیشخوان",
            "icon": "menu-icon tf-icons ti ti-layout-dashboard",
            "slug": "dashboard-analytics"
        },
        {
            "name": "لیست اطلاعات",
            "icon": "menu-icon tf-icons ti ti-report",
            "slug": "reports",
            "submenu": [
                {
                    "url": "tests_table",
                    "name": "لیست تست ها",
                    "slug": "tests_table"
                },
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
            "name": "حساب من",
            "icon": "menu-icon tf-icons ti ti-user-circle",
            "slug": "support",
            "submenu": [
                {
                    "url": "profile",
                    "name": "نمای کاربری",
                    "slug": "profile",
                },
                {
                    "url": "support",
                    "name": "ارسال تیکت",
                    "slug": "support"
                }
            ]
        }
    ]
}

menu_user = {
    "menu": [
        {
            "url": "index",
            "name": "پیشخوان",
            "icon": "menu-icon tf-icons ti ti-layout-dashboard",
            "slug": "dashboard-analytics"
        },
        {
            "name": "لیست اطلاعات",
            "icon": "menu-icon tf-icons ti ti-report",
            "slug": "reports",
            "submenu": [
                {
                    "url": "tests_table",
                    "name": "لیست تست ها",
                    "slug": "tests_table"
                },
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
            "name": "حساب من",
            "icon": "menu-icon tf-icons ti ti-user-circle",
            "slug": "support",
            "submenu": [
                {
                    "url": "profile",
                    "name": "نمای کاربری",
                    "slug": "profile",
                },
                {
                    "url": "support",
                    "name": "ارسال تیکت",
                    "slug": "support"
                }
            ]
        }
    ]
}
