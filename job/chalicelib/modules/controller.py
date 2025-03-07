import logging
from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus

from chalicelib.common.enums.response_type_enum import ResponseTypeEnum
from chalicelib.common.helpers.message_response_helper import MessageResponseHelper
from chalicelib.modules.messages import Messages
from .model import JobModel
from ..common.helpers.error_middleware import exception_handler
from ..common.helpers.filters import Filters
from ..modules.service import JobService

cors_config = CORSConfig(allow_origin='*', allow_headers=['Content-Type', 'Authorization'], max_age=600,
    expose_headers=['Content-Length'], allow_credentials=True)

service = JobService()
api = Blueprint(__name__)
Job_URL = '/jobs'


@api.route(Job_URL, methods=['POST'], cors=cors_config)
@exception_handler
def add():
    request = api.current_request
    model_data = request.json_body
    try:
        job_data = JobModel(**model_data)
        serialized_data = job_data.dict(exclude_none=True)
        inserted_model = service.add_model(serialized_data)
        if not inserted_model:
            raise ValueError(Messages.JOB_CREATION_ERROR)
        message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_ADDED,
            id=str(inserted_model["_id"]))
        return Response(message_response, status_code=HTTPStatus.CREATED)
    except ValueError as ve:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, str(ve))
        return Response(message_response, status_code=HTTPStatus.BAD_REQUEST)
    except Exception as ex:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.UNKNOWN_ERROR)
        logging.exception(f"Unexpected error: {ex}")
        return Response(message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route(Job_URL, methods=['GET'],cors=cors_config)
@exception_handler
def get_all_with_criteria():
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)
    models = service.get_all_models(filters=criteria)
    return Response(body=json_util.dumps(models))


@api.route(Job_URL + '/{_id}', methods=['GET'],cors=cors_config)
@exception_handler
def get_by_id(_id):
    model = service.get_model(_id)
    if  model:
        return Response(body=json_util.dumps(model))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND
        )
        return Response(message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(Job_URL + '/{_id}', methods=['PUT'], cors=cors_config)
@exception_handler
def update(_id):
    request = api.current_request

    if not _id:
        return Response(
            MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.REQUIRED_ID_URL),
            status_code=HTTPStatus.BAD_REQUEST
        )

    model_data = request.json_body
    if not model_data:
        return Response(
            MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.INVALID_BODY),
            status_code=HTTPStatus.BAD_REQUEST
        )

    job_to_update = service.get_model(_id)
    if not job_to_update:
        return Response(
            MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND),
            status_code=HTTPStatus.NOT_FOUND
        )

    updated_job = service.update_model(_id, model_data)
    if updated_job:
        return Response(
            MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_UPDATED),
            status_code=HTTPStatus.OK
        )

    return Response(
        MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.JOB_CREATION_ERROR),
        status_code=HTTPStatus.BAD_REQUEST
    )



@api.route(Job_URL + '/{_id}', methods=['DELETE'], cors=cors_config)
@exception_handler
def delete_by_id(_id):
    if service.delete_model(_id):
        message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_DELETED)
        status_code = HTTPStatus.NO_CONTENT
    else:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        status_code = HTTPStatus.NOT_FOUND
    return Response(message_response, status_code=status_code)


@api.route(Job_URL + '/{_id}', methods=['PATCH'], cors=cors_config)
@exception_handler
def patch(_id):
    request = api.current_request
    model_data = request.json_body
    status = model_data.get("status")
    if status:
        updated_model = service.update_status(_id, status)
    if not updated_model:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.ERROR, Messages.ERROR_NOT_FOUND)
        status_code = HTTPStatus.NOT_FOUND
    else:
        message_response = MessageResponseHelper.build(ResponseTypeEnum.SUCCESS, Messages.SUCCESS_UPDATED)
        status_code = HTTPStatus.NO_CONTENT
    return Response(message_response, status_code=status_code)
