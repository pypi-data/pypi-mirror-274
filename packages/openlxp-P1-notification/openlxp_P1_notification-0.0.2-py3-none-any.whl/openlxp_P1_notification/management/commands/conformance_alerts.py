from datetime import datetime as dt
import json
import logging
import copy


from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)

from openlxp_P1_notification.management.utils.p1ps_requests import (
    overall_health, send_email)
from openlxp_P1_notification.models import (email, recipient)

from openlxp_P1_notification.serializer import EmailSerializer

logger = logging.getLogger('dict_config_logger')


def trigger_health_check():
    """Command to trigger email health check"""
    overall_health()


def trigger_status_update(email_type):
    """Command to trigger email notification"""

    body_data = EmailSerializer(email_type).data

    recipient_list = body_data['recipients']
    now = dt.now()
    datetimenow = now.strftime("%d/%m/%Y %H:%M:%S")

    template_data = EmailSerializer(email_type).data

    for recipient_email in recipient_list:
        body_data = copy.deepcopy(template_data)

        recipient_obj = recipient.objects.get(
            email_address=recipient_email)

        body_data['recipients'] = [recipient_email]

        if 'name' in email_type.template_type.template_inputs:
            body_data['template_inputs']['name'] = (recipient_obj.first_name +
                                                    " " +
                                                    recipient_obj.last_name)
        if 'datetime' in email_type.template_type.template_inputs:
            body_data['template_inputs']['datetime'] = datetimenow

        body_data = json.dumps(body_data)

        send_email(body_data, str(email_type.template_type))


def trigger_subscribed_list_update(email_type, recipient_list,
                                   list_name, list_url):
    """Command to trigger email for list updates"""

    now = dt.now()
    datetimenow = now.strftime("%d/%m/%Y %H:%M:%S")

    template_data = EmailSerializer(email_type).data

    for recipient_id in recipient_list:
        body_data = copy.deepcopy(template_data)

        body_data['recipients'] = [recipient_id[0]]
        first_name = recipient_id[1]

        if 'first_name' in email_type.template_type.template_inputs:
            max_len = body_data['template_inputs']['first_name']['max_length']
            body_data['template_inputs']['first_name'] = first_name[:max_len]
        if 'date_time' in email_type.template_type.template_inputs:
            max_len = body_data['template_inputs']['date_time']['max_length']
            body_data['template_inputs']['date_time'] = datetimenow[:max_len]
        if 'list_name' in email_type.template_type.template_inputs:
            max_len = body_data['template_inputs']['list_name']['max_length']
            body_data['template_inputs']['list_name'] = list_name[:max_len]
        if 'list_url' in email_type.template_type.template_inputs:
            max_len = body_data['template_inputs']['list_url']['max_length']
            body_data['template_inputs']['list_url'] = list_url[:max_len]

        body_data = json.dumps(body_data)
        send_email(body_data, str(email_type.template_type))


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument('email_references', nargs="+", type=str)
        parser.add_argument('email_references', type=str)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        # for email_reference in options['email_references']:
        try:
            email_type = email.objects.get(
                reference=options['email_references'])
        except email.DoesNotExist:
            raise CommandError('Email Reference "%s" does not exist' %
                               options['email_references'])
        # now = datetime.now()
        # dt = now.strftime("%d/%m/%Y %H:%M:%S")
        # template_inputs = {
        #     "datetime": dt,
        #     "name": "FNAME LNAME"
        # }
        # trigger_status_update(email_type)

        recipient_list = [('kjijo@deloitte.com', 'Karen', 'jijo'),
                          ('karenjijo@gmail.com', 'KJ', 'rocks')]
        trigger_subscribed_list_update(email_type, recipient_list,
                                       "Public",
                                       "https://dev-xds.deloitteopenlxp.com/lists/1")
        # get_team_templates()
