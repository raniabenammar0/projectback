import datetime
from pymongoose.mongo_types import Types, Schema
from ..config.mongodb import mongo_client
from pymongoose import methods

methods.database = mongo_client
ProjetSchema = {
    "projectDataBaseId" : {
        "type" : Types.String,
        "required": True
    },
    "projectPlatformId" : {
        "type" : Types.String,
        "required": True
    },
    "projectName" : {
        "type" : Types.String,
        "required": True
    },
};


ReviewSchema ={
    "commentPlatformId" : {
        "type" : Types.Number,
        "required": True
    }
};

UserSchema ={
    "userId" : {
        "type" : Types.String,
        "required": True
    }
};

LicenseSchema={
    "LicenseId" :{
        "type" :Types.String,
        "required" :False
    }
}
MergeRequestSchema = {
    "mrDataBaseId" : {
        "type" : Types.String,
        "required": True
    },"mrPlatformId" : {
        "type" : Types.Number,
        "required": False
    },"title" : {
        "type" : Types.String,
        "required": False
    },"author" : {
        "type" : Types.String,
        "required": True
    },"web_url" : {
        "type" : Types.String,
        "required": True
    },
};
class JobSchema(Schema):
    schema_name = "Job"

    def __init__(self, **kwargs):
        self.schema = {
            "user": {
                "type": UserSchema ,
                "required": True
            },
            "mergeRequest": {
                "type": MergeRequestSchema ,
                "required": True
            },
            "review": {
                "type": ReviewSchema,
                "required": True
            },
            "project": {
                "type": ProjetSchema,
                "required": True,
            },
             "status": {
                "type": Types.String,
                "required": False,
            },
            "jobType": {
                "type": Types.String,
                "enum": ["REVIEW", "VERIFY"],
                "required": True
            },
            "license": {
                "type": LicenseSchema,
                "required": False
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
        return JobSchema(**self.schema)

    def __getitem__(self, item):
        return self.schema[item]

methods.schemas["Job"] = JobSchema()
