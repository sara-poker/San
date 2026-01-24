from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "setup/profile",
        login_required(ProfileView.as_view(template_name="profile.html")),
        name="profile",
    ),
    path(
        "setup/app/<int:pk>",
        login_required(SetupAppView.as_view(template_name="setup_app.html")),
        name="setup_app",
    ),

    path(
        "setup/isp/<int:pk>",
        login_required(SetupIspView.as_view(template_name="setup_isp.html")),
        name="setup_isp",
    ),
    path(
        "setup/users/table",
        login_required(UsersTableView.as_view(template_name="users_table.html")),
        name="usersTable",
    ),
    path(
        "setup/user/detail/<int:pk>/",
        login_required(UserDetailView.as_view(template_name="user_detail.html")),
        name="usersDetail",
    )
]
