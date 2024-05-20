from sais.notify.auth.auth_info import EnvVarCredentialsProvider
from sais.notify.clients.notify_client import NotifyClient
from sais.notify.config import const
from sais.notify.config.const import ENDPOINT, NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU, \
    NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU_GROUP, LOGGER_NAME
from sais.notify.model.message_model import NotificationRequest, MessageModel
from sais.notify.types import NotifyType
import logging


class MessageHandler(object):
    def __init__(self, auth_provider: EnvVarCredentialsProvider):
        self.auth_provider = auth_provider
        self.logger = logging.getLogger(LOGGER_NAME)

    def send_notification(self, notify_type: NotifyType, to: str, message: str) -> bool:
        request = NotificationRequest(notify_type=notify_type, to=to, message=message)
        request.model_dump()
        if notify_type in (NotifyType.FEISHU_USER_TEXT, NotifyType.FEISHU_USER_RICH_TEXT,
                           NotifyType.FEISHU_GROUP_TEXT, NotifyType.FEISHU_GROUP_MESSAGE_CARD):
            return self.__send_notification_feishu(notify_type, to, message)
        else:
            self.logger.error(f'not support notify type: {notify_type}')
        return False

    def __send_notification_feishu(self, notify_type: NotifyType, to: str, message: str) -> bool:
        client = NotifyClient(ENDPOINT, self.auth_provider)
        message_model = MessageModel(message=message, to=to)
        if notify_type == NotifyType.FEISHU_USER_TEXT:
            message_model.set_type(NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU)
            return client.send_notification_feishu(message_model)
        elif notify_type == NotifyType.FEISHU_USER_RICH_TEXT:
            message_model.set_type(NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU)
            message_model.set_robot_name(const.SAIS_ROBOT_NAME)
            return client.send_notification_feishu(message_model)
        elif notify_type == NotifyType.FEISHU_GROUP_TEXT:
            message_model.set_type(NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU_GROUP)
            return client.send_notification_feishu(message_model)
        elif notify_type == NotifyType.FEISHU_GROUP_MESSAGE_CARD:
            message_model.set_type(NOTIFY_SERVICE_NOTIFY_TYPE_FEISHU_GROUP)
            return client.send_notification_feishu(message_model)
