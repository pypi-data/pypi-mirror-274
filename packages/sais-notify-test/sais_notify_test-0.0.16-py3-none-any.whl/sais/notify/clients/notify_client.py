import json
import logging
from http import HTTPStatus

import requests

from sais.notify.auth.auth_info import EnvVarCredentialsProvider
from sais.notify.config.const import LOGGER_NAME
from sais.notify.model.message_model import MessageModel


class NotifyClient(object):
    def __init__(self, endpoint, auth_provider: EnvVarCredentialsProvider):
        self.endpoint = endpoint
        self.auth_provider = auth_provider
        self.logger = logging.getLogger(LOGGER_NAME)

    def send_notification_feishu(self, message_info: MessageModel) -> bool:
        headers = {
            'Authorization': self.auth_provider.token,
            'Content-Type': 'application/json'
        }
        payload = message_info.model_dump_json()
        response = requests.post(f'{self.endpoint}/api/v1/notify/send', headers=headers,
                                 json=payload)

        if response.status_code == HTTPStatus.OK:
            self.logger.info(f'Notification sent successfully')
            return response.json()
        else:
            raise Exception(f'Error sending notification: {response.status_code} - {response.text}')
