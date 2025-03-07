from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus

from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.helpers.filters import Filters
from ..common.helpers.message_response_helper import MessageResponseHelper
from ..common.helpers.error_middelware import exception_handler
from ..modules.messages import Messages
from .service import MergeRequestService

cors_config = CORSConfig(
    allow_origin="*",
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
    expose_headers=["Content-Length"],
    allow_credentials=True,
)

service = MergeRequestService()
api = Blueprint(__name__)
MergeRequest_URL = '/request'

@api.route(MergeRequest_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    request = api.current_request
    model_data = request.json_body

    try:
        inserted_id = service.add_model(model_data)
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_ADDED,
            id=str(inserted_id),
        )
        return Response(message_response, status_code=HTTPStatus.CREATED)
    except ValueError as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            str(e),
        )
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNEXPECTED_ERROR,
        )
        return Response(message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

@api.route(MergeRequest_URL, methods=['GET'], cors=cors_config)
@exception_handler
def get_all_with_criteria():
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=json_util.dumps(models))

@api.route(MergeRequest_URL + "/{_id}", methods=['GET'], cors=cors_config)
@exception_handler
def get_by_id(_id):
    model = service.get_model(_id)

    if model:
        return Response(body=json_util.dumps(model))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND,
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


    
@api.route(MergeRequest_URL + '/{_id}', methods=['PUT'], cors=cors_config)
@exception_handler
def patch(_id):
    request = api.current_request
    model_data = request.json_body

    try:
      
        model_data["_id"] = _id

      
        updated_model = service.update_model(model_data)

        if not updated_model:
          
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                Messages.ERROR_NOT_FOUND,
            )
            return Response(
                body=message_response,
                headers={'Access-Control-Allow-Origin': '*'},
                status_code=HTTPStatus.NOT_FOUND,
            )

       
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_UPDATED,
        )
        return Response(
            body=message_response,
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=HTTPStatus.OK,
        )

    except ValueError as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            f"{Messages.ERROR_VALIDATION_FAILED}: {str(e)}",
        )
        return Response(
            body=message_response,
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    except Exception as e:
       
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNKNOWN_ERROR,
        )
        return Response(
            body=message_response,
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )





@api.route(MergeRequest_URL + "/{_id}", methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    if service.delete_model(_id):
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.SUCCESS,
            Messages.SUCCESS_DELETED,
        )
        return Response(message_response, status_code=HTTPStatus.OK)
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND,
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)
