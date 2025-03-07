from bson import json_util
from chalice import Blueprint, Response
from chalice import CORSConfig
from http import HTTPStatus

from ..common.enums.response_type_enum import ResponseTypeEnum
from ..common.helpers.Filters import Filters
from ..common.helpers.message_response_helper import MessageResponseHelper
from ..common.helpers.error_middelware import exception_handler
from .service import EmailService


cors_config = CORSConfig(
    allow_origin="*",
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
    expose_headers=["Content-Length"],
    allow_credentials=True,
)

service = EmailService()
api = Blueprint(__name__)
Email_URL = '/email'





@api.route( Email_URL + "/delivery", methods=['POST'], cors=cors_config)
@exception_handler
def sendEmail():
    request = api.current_request
    model_data = request.json_body
    response = service.send_email(model_data)
    return response
