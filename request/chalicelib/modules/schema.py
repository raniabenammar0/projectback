import datetime
from pymongoose.mongo_types import Types, Schema
from ..config.mongodb import mongo_client
from pymongoose import methods

methods.database = mongo_client



projectSchema = {
    "projectId" : {
        "type" : Types.String,
        "required": True
    },
    "projectName" : {
        "type" : Types.String,
        "required": True
    },
    "projectPlateformId" : {
        "type" : Types.String,
        "required": True
    },
}

authorSchema = {
    "userName" : {
        "type" : Types.String,
        "required": True
    },
    "avatar_url" : {
        "type" : Types.Number,
        "required": True
    },
}



class MergeRequestSchema(Schema):
    schema_name = "MergeRequest"

    def __init__(self, **kwargs):
        self.schema = {
            "mergeTitle": {
                "type": Types.String,
                "required": True,
            },
            "plateformId": {
                "type": Types.String,
                "required": True,
            },
            "state": {
                "type": Types.String,
                "required": True,
            },
            "author": {
                "type": authorSchema,
                "required": True,
            },
            "assignedTo": {
                "type": Types.String,
                "required": True,
            },
            "changes_number": {
                "type": Types.Number,
                "required": True,
            },
             "link": {
                 "type": Types.String,
                 "required": True,
             },
              "sourceBranch": {
                  "type": Types.String,
                  "required": True,
              },
               "project": {
                   "type": projectSchema,
                   "required": True,
               },
            "createdAt": {
                "type": Types.Date,
                "default": datetime.datetime.now,
                "required": True
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
        return MergeRequestSchema(**self.schema)

    def __getitem__(self, item):
        return self.schema[item]

methods.schemas["MergeRequest"] = MergeRequestSchema()
