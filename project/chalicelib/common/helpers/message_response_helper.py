from  chalicelib.common.enums.response_type_enum import ResponseTypeEnum


class MessageResponseHelper:
    @staticmethod
    def build(message_type: ResponseTypeEnum, message, **kwargs):
        response = {message_type.value: message}
        response.update(kwargs)
        return response


