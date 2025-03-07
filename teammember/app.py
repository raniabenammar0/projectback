from chalice import Chalice
from chalicelib.modules.controller import api

app = Chalice(app_name='TeamMember')
app.experimental_feature_flags.update(['BLUEPRINTS'])
app.register_blueprint(api)

def handler(event, context):
    return app(event, context)
