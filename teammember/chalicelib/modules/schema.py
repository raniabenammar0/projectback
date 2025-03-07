import datetime
from pymongoose.mongo_types import Types, Schema
from ..config.mongodb import mongo_client
from pymongoose import methods
from pydantic import Field

methods.database = mongo_client



userSchema ={
    "userId" : {
        "type" : Types.String,
        "required": True
    },
    "userName" : {
        "type" : Types.String,
        "required": True
    },
    "email" : {
        "type" : Types.String,
        "required": True
    },
}

projetSchema = {
    "projectDataBaseId" : {
        "type" : Types.String,
        "required": True
    },
    "projectId" : {
        "type" : Types.Number,
        "required": True
    },
    "projectName" : {
        "type" : Types.String,
        "required": True
    },
    "gitUrl" : {
            "type" : Types.String,
            "required": True
        },
}


class TeamMemberSchema(Schema):
    schema_name = "TeamMember"

    def __init__(self, **kwargs):
        self.schema = {
            "user": {
                "type": userSchema,
                "required": False
            },
            "project": {
                "type": projetSchema,
                "required": False,
            },
            "userToken": {
                "type": Types.String,
                "required": True,
            },
            "role": {
                "type": Types.String,
                "enum": ["OWNER", "MAINTAINER", "DEV"],
                "required": True
            },
            "status": {
                "type": Types.String,
                "enum": ["PENDING", "ACCEPTED", "REJECTED"],
                "required": True
            },
            "createdAt": {
                "type": Types.Date,
                "default": datetime.datetime.now(),
                "required": False
            },
            "updatedAt": {
                "type": Types.Date,
                "default": datetime.datetime.now(),
                "required": False
            },
            "deletedAt": {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def to_dict(self):
        return self.dict(exclude_none=True)

    def copy(self):
        return TeamMemberSchema(**self.schema)

    def __getitem__(self, item):
        return self.schema[item]

methods.schemas["TeamMember"] = TeamMemberSchema()
