import json
from http import HTTPStatus

import requests
from fastapi.logger import logger

from sais.notify.auth.auth_info import EnvVarCredentialsProvider
from sais.notify.model import MessageModel


class NotifyClient(object):
    def __init__(self, endpoint, auth_provider: EnvVarCredentialsProvider):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def send_notification_feishu(self, message: MessageModel) -> bool:
        headers = {
            'Authorization': self.auth_provider.token,
            'Content-Type': 'application/json'
        }

        payload = message.model_dump_json()
        response = requests.post(f'{self.endpoint}/api/v1/notify/send', headers=headers, data=json.dumps(payload))

        if response.status_code == HTTPStatus.OK:
            logger.info(f'Notification sent successfully')
            return response.json()
        else:
            raise Exception(f'Error sending notification: {response.status_code} - {response.text}')
