"""
horilla_middlewares.py

This module is used to register horilla's middlewares without affecting the horilla/settings.py
"""

import threading

from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from horilla.settings import MIDDLEWARE

MIDDLEWARE.append("base.middleware.CompanyMiddleware")
MIDDLEWARE.append("horilla.horilla_middlewares.MethodNotAllowedMiddleware")
MIDDLEWARE.append("horilla.horilla_middlewares.ThreadLocalMiddleware")
MIDDLEWARE.append("accessibility.middlewares.AccessibilityMiddleware")
MIDDLEWARE.append("accessibility.middlewares.AccessibilityMiddleware")
MIDDLEWARE.append("base.middleware.ForcePasswordChangeMiddleware")
_thread_locals = threading.local()


sub_apps = {
    'employee':'manage_employee',
    'recruitment':'manage_recruitment',
    'attendance':'manage_attendance',
    'payroll':'payroll_management',
    'leave':'leave_management',
    'asset':'manage_assets',
    'pms':'pms_management',
    'onboarding':'manage_onboarding',
    'offboarding':'manage_Offboarding',
    'helpdesk':'manage_helpdesk',
}

class ThreadLocalMiddleware:
    """
    ThreadLocalMiddleWare
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request

        # التحقق من التطبيق عبر resolver_match
        app_name = request.path.strip('/').split('/')[0]

        app_permission = sub_apps.get(app_name)

        employee_get = getattr(request.user, 'employee_get', None)
        if employee_get and app_permission:
            if not employee_get.sub_has_perm(app_permission):
                return render(request, '403.html')

        response = self.get_response(request)
        return response


class MethodNotAllowedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotAllowed):
            return render(request, "405.html")
        return response
