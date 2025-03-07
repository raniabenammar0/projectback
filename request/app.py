from chalice import Chalice
from chalicelib.modules.controller import api as request_api
import time
import os  # Import os to read environment variables

start_time = time.time()

def exception_handler(event, get_response):
    try:
        print(event , get_response)
        return get_response(event)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': str(e)}
        }

app = Chalice(app_name='job-service')
app.experimental_feature_flags.update(['BLUEPRINTS'])
app.log
app.register_blueprint(request_api)
app.middleware('all')(exception_handler)
print("--- %s seconds ---" % (time.time() - start_time))

def handler (event , context):
    return app(event,context)

@app.route('/')
def index():
    return {'hello': 'world'}

