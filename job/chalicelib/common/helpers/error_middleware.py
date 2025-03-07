from .error_handler import ErrorHandler
from pydantic import ValidationError
from chalice import Response
from datetime import datetime

def exception_handler(get_response):
    def wrapper(*args, **kwargs):
        try:
            return get_response(*args, **kwargs)
        except ValidationError as exc:
            errors = exc.errors()
            error_details = {
                "errors": [],
                "timestamp": datetime.utcnow().isoformat(),
                "status_code": 400,
            }
            for error in errors:
                error_detail = ErrorHandler(
                    error_type=error['type'],
                    errors=error['msg'] + str(error['loc']),
                    uri=error.get('url', '')
                )
                error_details["errors"].append(error_detail.__dict__)
            return Response(
                body=error_details,
                headers={'Access-Control-Allow-Origin': '*'},
                status_code=400
            )
        except Exception as e:
            error_response = {
                "errors": {
                    "type": "UnhandledException",
                    "errors": str(e),
                    "uri": "",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status_code": 500,
                }
            }
            return Response(
                body=error_response,
                headers={'Content-Type': 'application/json'},
                status_code=500
            )
    return wrapper
