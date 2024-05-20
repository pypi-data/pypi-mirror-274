from enum import StrEnum


class NotifyType(StrEnum):
    FEISHU_USER_TEXT = "feishu_user_text"
    FEISHU_USER_RICH_TEXT = "feishu_user_rich_text"
    FEISHU_GROUP_TEXT = "feishu_group_text"
    FEISHU_GROUP_MESSAGE_CARD = "feishu_group_message_card"
