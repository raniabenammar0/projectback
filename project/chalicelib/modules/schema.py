import datetime
from pymongoose.mongo_types import Types, Schema
from ..config.mongodb import mongo_client
from pymongoose import methods

methods.database = mongo_client

class ProjectSchema(Schema):
    schema_name = "Project"

    def __init__(self, **kwargs):
        self.schema = {
            "userId": {
                "type": Types.String,
                "required": True
            },
            "projectName": {
                "type": Types.String,
                "required": True
            },
            "projectPlateformId": {
                "type": Types.String,
                "required": True,
            },
            "gitUrl": {
                "type": Types.String,
                "required": True,
            },
            "gitToken": {
                "type": Types.String,
                "required": True,
            },
            "deactivated": {
                "type": Types.Boolean,
                "required": True,
            },
            "platform": {
                "type": Types.String,
                "enum": ["GITLAB", "GITHUB", "BITBUCKET"],
                "required": True
            },
            "gptKey": {
                "type": Types.String,
                "required": True,
            },
            "createdAt": {
                "type": Types.Date,
                "default": datetime.datetime.now,
                "required": False
            },
            "updatedAt": {
                "type": Types.Date,
                "default": datetime.datetime.now,
                "required": False
            },
            "deletionDate": {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def to_dict(self):
        return self.dict(exclude_none=True)

    def copy(self):
        return ProjectSchema(**self.schema)

    def __getitem__(self, item):
        return self.schema[item]

methods.schemas["Project"] = ProjectSchema()
