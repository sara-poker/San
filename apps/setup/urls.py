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
