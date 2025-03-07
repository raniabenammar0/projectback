from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus
from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.helpers.Filters import Filters
from ..modules.messages import Messages
from .service import UserService
from ..common.helpers.message_response_helper import MessageResponseHelper
from .model import UserModel
from ..common.helpers.ErrorMiddleware import exception_handler
import logging

cors_config = CORSConfig(allow_origin='*', allow_headers=['Content-Type', 'Authorization'], max_age=600,
    expose_headers=['Content-Length'], allow_credentials=True)
service = UserService()
api = Blueprint(__name__)
USER_URL = '/users'


@api.route(USER_URL + '/{_id}', methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    model = service.get_model(_id)
    if model:
        return Response(body=json_util.dumps(model))
    else:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_ONE_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(USER_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    request = api.current_request
    model = request.json_body

    try:
            new_user_data = UserModel(**model)
            user = service.add_model(new_user_data)
            if not user:
                raise ValueError(Messages.UNKNOWN_ERROR)
            message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_ADDED, user=user)
            return Response(message_response, status_code=HTTPStatus.CREATED)
    except ValueError as ve:
            message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, str(ve))
            return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    except Exception as ex:
            message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.UNKNOWN_ERROR)
            logging.exception(f"{Messages.UNKNOWN_ERROR} {ex}")
            return Response(message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)



@api.route(USER_URL + '/{_id}', methods=['PUT'], cors=cors_config)
@exception_handler
def update_by_id(_id):
    request = api.current_request
    data = request.json_body
    model = UserModel(**data)

    user_to_update = service.get_model(_id)
    if not user_to_update:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)

    if service.is_user_changed(user_to_update, data):
        message_response = MessageResponseHelper.build(ResponseTypeEnum.WARN, Messages.NO_CHANGES)
        status_code = HTTPStatus.OK
    else:
        updated_user = service.update_model(_id, model)
        if updated_user:
            message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_UPDATED)
            status_code = HTTPStatus.ACCEPTED
        else:
            message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
            status_code = HTTPStatus.NOT_FOUND

    return Response(message_response, status_code=status_code)

@api.route(USER_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    if service.delete_model(_id):
        message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_DELETED)
        status_code = HTTPStatus.NO_CONTENT
    else:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        status_code = HTTPStatus.NOT_FOUND
    return Response(message_response, status_code=status_code)
