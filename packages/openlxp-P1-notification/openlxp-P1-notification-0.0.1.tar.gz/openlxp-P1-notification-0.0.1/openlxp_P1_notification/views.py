from rest_framework.views import APIView
from rest_framework.response import Response

from openlxp_P1_notification.management.utils.p1ps_requests import (
    get_email_request)


class EmailRequestView(APIView):
    """Handles HTTP requests for Email request data from P1PS"""

    def get(self, request, request_id):
        """This method defines an API to fetch email request
        using request ID"""

        email_request_response = get_email_request(request_id)

        return Response(email_request_response.json(),
                        status=email_request_response.status_code)
