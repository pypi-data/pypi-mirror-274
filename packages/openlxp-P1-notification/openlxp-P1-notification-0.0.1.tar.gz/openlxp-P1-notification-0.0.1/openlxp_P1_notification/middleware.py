from openlxp_P1_notification.management.utils.p1ps_requests import (
    get_team_templates)


class TemplateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.path == "/admin/openlxp_P1_notification/template/":
            get_team_templates()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
