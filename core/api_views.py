import json

from django.contrib.auth import authenticate, login, logout
from django.db import OperationalError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


def _user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }


def _error_response(message, status=400):
    return JsonResponse({"success": False, "message": message}, status=status)


def _database_unavailable_response():
    return _error_response("Authentication service is temporarily unavailable.", status=503)


@require_POST
def api_login(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return _error_response("Invalid JSON payload.")

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not username or not password:
        return _error_response("Username and password are required.")

    try:
        user = authenticate(request, username=username, password=password)
    except OperationalError:
        return _database_unavailable_response()

    if user is None:
        return _error_response("Invalid username or password.", status=401)
    if not user.is_active:
        return _error_response("This account is inactive.", status=403)
    if not user.is_staff:
        logout(request)
        return _error_response("You do not have dashboard access.", status=403)

    login(request, user)
    return JsonResponse(
        {
            "success": True,
            "message": "Login successful",
            "user": _user_payload(user),
        }
    )


@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse(
        {
            "success": True,
            "message": "Logout successful",
        }
    )


@require_GET
@ensure_csrf_cookie
def api_me(request):
    try:
        user = request.user
        is_authenticated = user.is_authenticated
    except OperationalError:
        return _database_unavailable_response()
    if not is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required",
            },
            status=401,
        )
    try:
        if not user.is_active or not user.is_staff:
            logout(request)
            return JsonResponse(
                {
                    "success": False,
                    "message": "You do not have dashboard access.",
                },
                status=403,
            )
    except OperationalError:
        return _database_unavailable_response()

    return JsonResponse(
        {
            "success": True,
            "user": _user_payload(user),
        }
    )


@require_GET
@ensure_csrf_cookie
def api_health(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "ReqFlow AI",
            "message": "Server is running",
        }
    )
