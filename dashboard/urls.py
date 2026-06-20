from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.AdminLoginView.as_view(), name="login"),
    path("logout/", views.admin_logout_view, name="logout"),
    path("", views.dashboard_home, name="index"),
    path("profile/", views.profile_view, name="profile"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("admins/", views.admin_list_view, name="admin_list"),
    path("admins/create/", views.admin_create_view, name="admin_create"),
    path("admins/<int:user_id>/", views.admin_detail_view, name="admin_detail"),
    path("admins/<int:user_id>/edit/", views.admin_edit_view, name="admin_edit"),
    path("admins/<int:user_id>/activate/", views.admin_activate_view, name="admin_activate"),
    path("admins/<int:user_id>/deactivate/", views.admin_deactivate_view, name="admin_deactivate"),
    path("admins/<int:user_id>/reset-password/", views.admin_reset_password_view, name="admin_reset_password"),
]
