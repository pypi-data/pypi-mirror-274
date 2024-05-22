import logging

from django.core.exceptions import ValidationError

import requests


from openlxp_P1_notification.management.utils.p1ps_configuration import (
    SetCookies, TokenAuth, get_P1PS_base_endpoint, get_P1PS_team_ID)
from openlxp_P1_notification.serializer import TemplateSerializer

logger = logging.getLogger('dict_config_logger')

headers = {'Content-Type': 'application/json'}


"""
    Requests set up to verify using Platform One Postal Service (P1PS)
    API Specification (1.0.0)

"""


def SendResponse(response):
    """Function to return response and error catches"""

    if response.status_code in [400, 401, 404, 500]:
        logger.error(response.json())
        return False
    elif response.status_code in [200, 201]:
        try:
            logger.info(response.json())
        except requests.RequestException:
            logger.warning(requests.RequestException)
        return True


def get_team():
    """Request to verify user is a part team and check permissions"""
    base_endpoint = get_P1PS_base_endpoint()
    team_id = get_P1PS_team_ID()
    team_id_list = []

    url = base_endpoint + "/api/teams"

    response = requests.get(url=url, headers=headers,
                            auth=TokenAuth(), cookies=SetCookies())
    response_success = SendResponse(response)
    if response_success:
        for team in response.json():
            """iterating through different teams to find matching teams"""
            if 'team_id' in team:
                team_id_list += [team['team_id']]

        if team_id not in team_id_list:
            raise ValidationError("User does not have permission "
                                  "to use Team ID ")


def get_team_templates():
    """Request to get templates associated with team """
    base_endpoint = get_P1PS_base_endpoint()
    team_id = get_P1PS_team_ID()

    url = base_endpoint + "/api/teams/" + team_id + "/templates"

    response = requests.get(url=url, headers=headers,
                            auth=TokenAuth(), cookies=SetCookies())
    response_success = SendResponse(response)
    if response_success:
        for template in response.json()['data']:
            serializer = TemplateSerializer(data=template)

            if not serializer.is_valid():
                # If not received send error and bad request status
                logger.error(serializer.errors)
            else:
                # If received save record in templates
                logger.info(serializer)
                serializer.save()


"""
    Requests set up using Platform One Postal Service (P1PS)
    API Specification (1.0.0)

"""


def overall_health():
    """Request to perform P1PS health check """
    base_endpoint = get_P1PS_base_endpoint()

    url = base_endpoint + "/api/health"

    response = requests.get(url=url, headers=headers,
                            auth=TokenAuth(), cookies=SetCookies())
    response_success = SendResponse(response)
    if response_success:
        get_team()


def send_email(body_data, template_type):
    """Request to send email via P1PS"""

    # Check user Permissions to use team

    base_endpoint = get_P1PS_base_endpoint()
    team_id = get_P1PS_team_ID()

    url = base_endpoint + "/api/teams/" + team_id + "/emails/" + template_type

    response = requests.post(url=url, headers=headers,
                             data=body_data, auth=TokenAuth(),
                             cookies=SetCookies())
    SendResponse(response)


def get_email_request(request_id):
    """Retrieves an Email request based on the requested ID."""
    base_endpoint = get_P1PS_base_endpoint()
    team_id = get_P1PS_team_ID()

    url = base_endpoint + "/api/teams/" + team_id + "/emails/" + request_id
    response = requests.get(url=url, headers=headers,
                            auth=TokenAuth(), cookies=SetCookies())
    return response
