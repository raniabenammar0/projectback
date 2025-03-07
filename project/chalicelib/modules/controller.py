from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus
import os

from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.helpers.filters import Filters
from ..common.helpers.message_response_helper import MessageResponseHelper
from ..common.helpers.error_middelware import exception_handler
from ..modules.messages import Messages
from .service import ProjectService

cors_config = CORSConfig(
    allow_origin="*",
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
    expose_headers=["Content-Length"],
    allow_credentials=True,
)

service = ProjectService()
api = Blueprint(__name__)
Project_URL = "/projects"

@api.route(Project_URL, methods=["POST"], cors=cors_config)
@exception_handler
def add_project():
    request = api.current_request
    model_data = request.json_body
    model_data["gptKey"] = os.getenv("SECRET_TOKEN")

    try:
        inserted_model = service.add_model(model_data)
        return Response(
            body=json_util.dumps(inserted_model),
            status_code=HTTPStatus.CREATED,
        )
    except ValueError as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            str(e),
        )
        return Response(body=message_response, status_code=HTTPStatus.BAD_REQUEST)
    except Exception as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNKNOWN_ERROR,
        )
        return Response(body=message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)



@api.route(Project_URL, methods=["GET"], cors=cors_config)
@exception_handler
def get_all_projects():
    query_params = api.current_request.query_params or {}
    criteria = Filters(**query_params)

    models = service.get_all_models(filters=criteria)
    return Response(body=json_util.dumps(models) , status_code=HTTPStatus.OK)


@api.route(Project_URL + "/{_id}", methods=["GET"], cors=cors_config)
@exception_handler
def get_project_by_id(_id):
    model = service.get_model(_id)

    if model:
        return Response(body=json_util.dumps(model))
    else:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.ERROR_NOT_FOUND,
        )
        return Response(body=message_response, status_code=HTTPStatus.NOT_FOUND)


@api.route(Project_URL + "/{_id}", methods=["PATCH"], cors=cors_config)
@exception_handler
def update_project(_id):
    request = api.current_request
    model_data = request.json_body
    git_token = model_data.get("gitToken")

    try:
        updated_model = service.update_git_token(_id, git_token)

        if updated_model:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.SUCCESS,
                Messages.SUCCESS_UPDATED,
            )
            return Response(body=message_response, status_code=HTTPStatus.OK)
        else:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                Messages.ERROR_NOT_FOUND,
            )
            return Response(body=message_response, status_code=HTTPStatus.NOT_FOUND)

    except ValueError as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            f"{Messages.ERROR_VALIDATION_FAILED}: {str(e)}",
        )
        return Response(body=message_response, status_code=HTTPStatus.BAD_REQUEST)

    except Exception as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNKNOWN_ERROR,
        )
        return Response(body=message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route(Project_URL + "/{_id}", methods=["DELETE"], cors=cors_config)
@exception_handler
def deactivate_project(_id):
    query_params = api.current_request.query_params or {}
    definitive = query_params.get("definitive", "false").lower() == "true"

    try:
        project = service.deactivate_project(_id, definitive)

        if project:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.SUCCESS,
                Messages.SUCCESS_DELETED if definitive else "Project successfully deactivated.",
            )
            return Response(body=message_response, status_code=HTTPStatus.OK)
        else:
            message_response = MessageResponseHelper.build(
                ResponseTypeEnum.ERROR,
                Messages.ERROR_NOT_FOUND,
            )
            return Response(body=message_response, status_code=HTTPStatus.NOT_FOUND)

    except ValueError as ve:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            str(ve),
        )
        return Response(body=message_response, status_code=HTTPStatus.BAD_REQUEST)

    except Exception as e:
        message_response = MessageResponseHelper.build(
            ResponseTypeEnum.ERROR,
            Messages.UNKNOWN_ERROR,
        )
        return Response(body=message_response, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@api.route(Project_URL + "/encrypt", methods=["POST"], cors=cors_config)
@exception_handler
def encrypt_token():
    request = api.current_request
    token = request.json_body.get("token")

    if not token:
        return Response(
            body={"error": "Token is required"},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    try:
        encrypted_token = service.encrypt_token(token)
        return Response(
            body={"encryptedToken": encrypted_token},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.OK,
        )

    except Exception as e:
        return Response(
            body={"error": str(e)},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@api.route(Project_URL + "/decrypt", methods=["POST"], cors=cors_config)
@exception_handler
def decrypt_token():
    request = api.current_request
    encrypted_token = request.json_body.get("gitToken")

    if not encrypted_token:
        return Response(
            body={"error": "Encrypted token is required"},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.BAD_REQUEST,
        )

    try:
        decrypted_token = service.decrypt_token(encrypted_token)
        return Response(
            body={"decryptedToken": decrypted_token},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.OK,
        )

    except Exception as e:
        return Response(
            body={"error": str(e)},
            headers={"Access-Control-Allow-Origin": "*"},
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
