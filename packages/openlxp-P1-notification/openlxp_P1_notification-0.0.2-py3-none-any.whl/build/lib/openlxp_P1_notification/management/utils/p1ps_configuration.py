import logging
import os

import requests

from requests.auth import AuthBase

logger = logging.getLogger('dict_config_logger')

headers = {'Content-Type': 'application/json'}


"""
    Functions set up to extract environment values for
    Platform One Postal Service (P1PS) API

"""


def get_P1PS_base_endpoint():
    """Extracts P1PS base endpoint"""
    P1PS_endpoint = "https://" + os.environ.get('P1PS_DOMAIN')

    if P1PS_endpoint[0]:
        logger.info("P1PS endpoint value  is present and set")
    else:
        logger.error("P1PS endpoint value is absent and not set")

    return P1PS_endpoint


def get_P1PS_team_token():
    """Extracts P1PS base endpoint"""
    team_token = os.environ.get('TEAM_TOKEN')

    if team_token[0]:
        logger.info("Team Token value  is present and set")
    else:
        logger.error("Team Token value is absent and not set")

    return team_token


def get_P1PS_team_ID():
    """Extracts P1PS base endpoint"""
    team_id = os.environ.get('TEAM_ID')

    if team_id[0]:
        logger.info("Team ID value  is present and set")
    else:
        logger.error("Team ID value is absent and not set")

    return team_id


"""
    Configuration set up for Platform One Postal Service (P1PS)
    API requests

"""


class TokenAuth(AuthBase):
    """Attaches HTTP Authentication Header to the given Request object."""

    def __call__(self, r, token_name='EMAIL_AUTH'):
        # modify and return the request

        r.headers[token_name] = get_P1PS_team_token()
        return r


def SetCookies():
    """Sets requests cookies jar with P1 authorization cookies"""

    jar = requests.cookies.RequestsCookieJar()
    jar.set(os.environ.get('COOKIE_NAME'),
            os.environ.get('COOKIE_VALUE'),
            domain=os.environ.get('P1PS_DOMAIN'), path='/')

    return jar
