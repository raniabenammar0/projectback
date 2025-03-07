from pymongoose.mongo_types import Types, Schema
from ..config.mongodb import mongo_client
from pymongoose import methods
import datetime

methods.database = mongo_client
CognitoSchema = {
    "sub": {
        "type": Types.String,
        "required": False
    },
    "email": {
        "type": Types.String,
        "required": True
    }
}

class UserSchema(Schema):
    schema_name = "UserModel"



    def __init__(self, **kwargs):
        self.schema = {
            "userName": {
                "type": Types.String,
                "required": True,
            },
            "cognito": {
                "type": CognitoSchema,
                "required": True,
            },
            "firstLogin": {
                "type": Types.Boolean,
                "required": True,
                "default": True
            },
            "email": {
                "types": Types.String,
                "required": True,
            },
            "credit": {
                "types": Types.Number,
                "required": False,
                "default": 10
            },
            "lastName": {
                "types": Types.String,
                "required": False,
            },
            "phone": {
                "types": Types.Number,
                "required": False
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
            "deletedAt": {
                "type": Types.Date,
                "required": False
            },
        }
        super().__init__(self.schema_name, self.schema, kwargs)

    def to_dict(self):
        return  {
            key: getattr(self, key, None)
            for key in self.schema.keys()
        }

    def copy(self):
        return UserSchema(**self.schema)

    def __getitem__(self, item):
        if item == "_id":
            return self.id  # Return the _id field if requested
        return self.schema.get(item)

methods.schemas["UserModel"] = UserSchema
