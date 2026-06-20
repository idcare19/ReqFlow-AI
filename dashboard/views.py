from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from functools import wraps

from .forms import (
    AdminCreateForm,
    AdminPasswordChangeForm,
    AdminProfileForm,
    AdminResetPasswordForm,
    AdminUpdateForm,
    DashboardLoginForm,
)

User = get_user_model()


class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_active or not request.user.is_staff:
            messages.error(request, "You do not have permission to access the dashboard.")
            logout(request)
            return redirect("dashboard:login")
        return super().dispatch(request, *args, **kwargs)


def staff_required(view_func):
    @wraps(view_func)
    def wrapped(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('dashboard:login')}?next={request.get_full_path()}")
        if not request.user.is_active or not request.user.is_staff:
            messages.error(request, "You do not have permission to access the dashboard.")
            logout(request)
            return redirect("dashboard:login")
        return view_func(request, *args, **kwargs)

    return wrapped


class AdminLoginView(LoginView):
    template_name = "dashboard/login.html"
    authentication_form = DashboardLoginForm
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active or not user.is_staff:
            messages.error(self.request, "You do not have dashboard access.")
            return self.form_invalid(form)
        login(self.request, user)
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        print("LOGIN POST RECEIVED")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return str(reverse_lazy("dashboard:index"))


@require_POST
@staff_required
def admin_logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("dashboard:login")


@staff_required
def dashboard_home(request: HttpRequest) -> HttpResponse:
    admin_users = User.objects.filter(is_staff=True)
    context = {
        "stats": {
            "total_admins": admin_users.count(),
            "active_admins": admin_users.filter(is_active=True).count(),
            "superusers": admin_users.filter(is_superuser=True).count(),
            "inactive_admins": admin_users.filter(is_active=False).count(),
        },
        "recent_admins": admin_users.order_by("-date_joined")[:5],
    }
    return render(request, "dashboard/index.html", context)


@staff_required
def profile_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AdminProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard:profile")
    else:
        form = AdminProfileForm(instance=request.user)
    return render(request, "dashboard/profile.html", {"form": form})


@staff_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("dashboard:change_password")
    else:
        form = AdminPasswordChangeForm(request.user)
    return render(request, "dashboard/change_password.html", {"form": form})


@staff_required
def admin_list_view(request: HttpRequest) -> HttpResponse:
    admins = User.objects.filter(is_staff=True).order_by("first_name", "username")
    return render(request, "dashboard/admins/list.html", {"admins": admins})


@staff_required
def admin_detail_view(request: HttpRequest, user_id: int) -> HttpResponse:
    admin_user = get_object_or_404(User, pk=user_id, is_staff=True)
    return render(request, "dashboard/admins/detail.html", {"admin_user": admin_user})


@staff_required
def admin_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AdminCreateForm(request.POST, actor=request.user)
        if form.is_valid():
            admin_user = form.save()
            messages.success(request, f"Admin '{admin_user.username}' created successfully.")
            return redirect("dashboard:admin_detail", user_id=admin_user.id)
    else:
        form = AdminCreateForm(actor=request.user, initial={"is_staff": True, "is_active": True})
    return render(request, "dashboard/admins/form.html", {"form": form, "page_title": "Create Admin", "submit_label": "Create Admin"})


@staff_required
def admin_edit_view(request: HttpRequest, user_id: int) -> HttpResponse:
    admin_user = get_object_or_404(User, pk=user_id, is_staff=True)
    if request.method == "POST":
        form = AdminUpdateForm(request.POST, instance=admin_user, actor=request.user)
        if form.is_valid():
            updated_user = form.save()
            messages.success(request, f"Admin '{updated_user.username}' updated successfully.")
            return redirect("dashboard:admin_detail", user_id=updated_user.id)
    else:
        form = AdminUpdateForm(instance=admin_user, actor=request.user)
    return render(request, "dashboard/admins/form.html", {"form": form, "page_title": "Edit Admin", "submit_label": "Save Changes", "admin_user": admin_user})


def _ensure_superuser_action_permission(request: HttpRequest, target: User) -> bool:
    if target.is_superuser and not request.user.is_superuser:
        messages.error(request, "Only superusers can manage another superuser.")
        return False
    return True


@require_POST
@staff_required
def admin_activate_view(request: HttpRequest, user_id: int) -> HttpResponse:
    admin_user = get_object_or_404(User, pk=user_id, is_staff=True)
    if not _ensure_superuser_action_permission(request, admin_user):
        return redirect("dashboard:admin_detail", user_id=admin_user.id)
    admin_user.is_active = True
    admin_user.save(update_fields=["is_active"])
    messages.success(request, f"Admin '{admin_user.username}' activated successfully.")
    return redirect("dashboard:admin_detail", user_id=admin_user.id)


@require_POST
@staff_required
def admin_deactivate_view(request: HttpRequest, user_id: int) -> HttpResponse:
    admin_user = get_object_or_404(User, pk=user_id, is_staff=True)
    if admin_user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("dashboard:admin_detail", user_id=admin_user.id)
    if not _ensure_superuser_action_permission(request, admin_user):
        return redirect("dashboard:admin_detail", user_id=admin_user.id)
    admin_user.is_active = False
    admin_user.save(update_fields=["is_active"])
    messages.success(request, f"Admin '{admin_user.username}' deactivated successfully.")
    return redirect("dashboard:admin_detail", user_id=admin_user.id)


@staff_required
def admin_reset_password_view(request: HttpRequest, user_id: int) -> HttpResponse:
    admin_user = get_object_or_404(User, pk=user_id, is_staff=True)
    if not _ensure_superuser_action_permission(request, admin_user):
        return redirect("dashboard:admin_detail", user_id=admin_user.id)
    if request.method == "POST":
        form = AdminResetPasswordForm(admin_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Password for '{admin_user.username}' reset successfully.")
            return redirect("dashboard:admin_detail", user_id=admin_user.id)
    else:
        form = AdminResetPasswordForm(admin_user)
    return render(request, "dashboard/admins/reset_password.html", {"form": form, "admin_user": admin_user})
