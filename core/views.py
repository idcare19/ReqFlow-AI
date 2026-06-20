from django.shortcuts import redirect
from django.http import JsonResponse


def home_redirect(request):
    return redirect("dashboard:login")


def health_check(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "ReqFlow AI",
            "message": "Server is running",
        },
        status=200,
    )
