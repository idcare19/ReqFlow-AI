from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

User = get_user_model()


class BootstrapFormMixin:
    def _apply_bootstrap_classes(self):
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            base_class = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            field.widget.attrs["class"] = f"{existing_class} {base_class}".strip()


class DashboardLoginForm(BootstrapFormMixin, forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")
            if not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
            if not self.user_cache.is_staff:
                raise forms.ValidationError("You do not have dashboard access.")

        return cleaned_data

    def get_user(self):
        return self.user_cache


class AdminCreateForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()
        if self.actor and not self.actor.is_superuser:
            self.fields["is_superuser"].disabled = True
            self.fields["is_superuser"].initial = False

    def clean_is_superuser(self):
        value = self.cleaned_data.get("is_superuser", False)
        if value and self.actor and not self.actor.is_superuser:
            raise forms.ValidationError("Only superusers can create another superuser.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        if cleaned_data.get("is_staff") is not True:
            self.add_error("is_staff", "New admins must have staff access.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

    def __init__(self, *args, actor=None, **kwargs):
        self.actor = actor
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()
        self.fields["is_staff"].disabled = True
        if self.actor and not self.actor.is_superuser:
            self.fields["is_superuser"].disabled = True

    def clean_is_superuser(self):
        value = self.cleaned_data.get("is_superuser", False)
        if value and self.actor and not self.actor.is_superuser:
            raise forms.ValidationError("Only superusers can grant superuser access.")
        return value

    def clean_is_staff(self):
        value = self.instance.is_staff
        if value is not True:
            raise forms.ValidationError("Admin users must remain staff members.")
        return value


class AdminProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()


class AdminPasswordChangeForm(BootstrapFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()


class AdminResetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()
