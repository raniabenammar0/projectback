from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus
from ..modules.model import TeamMember
from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.helpers.filters import Filters
from ..modules.messages import Messages
from .service import TeamMemberService
from ..common.helpers.message_response_helper import MessageResponseHelper
from ..common.helpers.error_middleware import exception_handler


cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'Authorization'],
    max_age=600,
    expose_headers=['Content-Length'],
    allow_credentials=True
)

service = TeamMemberService()
api = Blueprint(__name__)
TeamMember_URL = '/team-member'




@api.route(TeamMember_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    request = api.current_request
    model = request.json_body

    try:
        user_data = TeamMember(**model)
        teammember = service.add_model(user_data)
        message_response = MessageResponseHelper.build(
        ResponseTypeEnum.SUCCESS,
        Messages.SUCCESS_ADDED)
        return Response(message_response, status_code=HTTPStatus.CREATED)

    except ValueError as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            str(e)
        )
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)

    except Exception as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNKNOWN_ERROR,
        )
        return Response(message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route(TeamMember_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=json_util.dumps(models))


@api.route(TeamMember_URL + '/{_id}', methods=['GET'],cors=cors_config)
@exception_handler
def get_by_id(_id):
    model = service.get_model(_id)
    if model:
        return Response(body=json_util.dumps(model))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)



@api.route(TeamMember_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler

def patch(_id):
    request = api.current_request

    if not _id:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.REQUIRED_ID
        )
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)

    allowed_keys = {"status", "role","user"}
    received_keys = set(request.json_body.keys())

    if not received_keys.issubset(allowed_keys):
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNAUTHORIZED_FIELDS
        )
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)

    status = request.json_body.get("status")
    role = request.json_body.get("role")
    user = request.json_body.get("user")

    if status is None and role is None and  user is None :
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.INVALID_PAYLOAD
        )
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)

    if status is not None:
        service.update_status(_id, status)

    if role is not None:
        service.update_role(_id, role)

    if user is not None:
          service.update_user(_id,user)

    message_response = MessageResponseHelper.build(
        ResponseTypeEnum.SUCCESS,
        Messages.SUCCESS_UPDATED
    )
    return Response(message_response, status_code=HTTPStatus.OK)


@api.route(TeamMember_URL + '/{_id}', methods=['PUT'], cors=cors_config )
@exception_handler
def update_by_id(_id):
    request = api.current_request
    data = request.json_body
    model = TeamMember (**data)

    team_member_to_update = service.get_model(_id)
    if not team_member_to_update:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)

    if (service.check_changes(team_member_to_update, data)):
        message_response = MessageResponseHelper.build(ResponseTypeEnum.WARN, Messages.NO_CHANGES)
        status_code = HTTPStatus.OK

    elif service.update_team_member(_id, model):

        message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_UPDATED)
        status_code = HTTPStatus.NO_CONTENT
    else:

        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        status_code = HTTPStatus.NOT_FOUND

    return Response(message_response, status_code=status_code)



@api.route(TeamMember_URL + '/{_id}', methods=['DELETE'] ,cors=cors_config)
@exception_handler
def delete_by_id(_id):
    if service.delete_model(_id):
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_DELETED
        )
        status_code = HTTPStatus.OK
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        status_code = HTTPStatus.NOT_FOUND
    return Response(message_response, status_code=status_code)
