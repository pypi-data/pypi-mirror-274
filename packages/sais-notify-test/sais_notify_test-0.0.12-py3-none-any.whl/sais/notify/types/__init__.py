from enum import Enum


class MyStrEnum(Enum):
    def __new__(cls, value, member_name=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.member_name = member_name or value
        return obj

    def __str__(self):
        return self.value


class NotifyType(MyStrEnum):
    FEISHU_USER_TEXT = "feishu_user_text"
    FEISHU_USER_RICH_TEXT = "feishu_user_rich_text"
    FEISHU_GROUP_TEXT = "feishu_group_text"
    FEISHU_GROUP_MESSAGE_CARD = "feishu_group_message_card"
