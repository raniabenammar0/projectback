from bson import ObjectId
from pymongoose import methods
import datetime
from .model import UserModel
from .schema import UserSchema


class UserService:

    def _cast_fields(self, model):
        for field in ["_id", "createdAt", "updatedAt", "deletedAt"]:
            if field in model:
                model[field] = str(model[field])
        return model

    def get_model(self, _id):
        model = UserSchema.find_by_id(_id, parse=False)
        return self._cast_fields(model) if model else None
    def is_user_changed(self, model: dict, data: dict) -> bool:
        if not data.get('userName') or not data.get('email'):
            return True
        return all(
            data.get(field) == model.get(field)
            for field in ['userName', 'lastName', 'email', 'phone','credit']
        )
    def add_model(self, model: UserModel):
        serialized_data = model.model_dump(exclude_none=True)
        cognito_sub = model.cognito.sub if model.cognito else None
        cognito_email = model.cognito.email if model.cognito else None
        email = model.email if model.email else None
        existing_user = None
        if cognito_sub :
            existing_user = UserSchema.find_one({"cognito.sub": cognito_sub})
        elif  cognito_email and cognito_email == email :
            existing_user= UserSchema.find_one({"cognito.email": cognito_email})
        if existing_user:
            user_id = existing_user["_id"]
            first_login = serialized_data.get("firstLogin", True)
            if first_login:
                UserSchema.update({"_id": user_id}, {"$set": {"firstLogin": False}})
            return  self.get_model(user_id)
        else :
            inserted_model = methods.insert_one("UserModel", serialized_data)
            return self.get_model(inserted_model)

    def update_model(self, _id, model: UserModel):
        if not _id:
            return None
        obj_id = ObjectId(_id)
        update_data = model.model_dump(exclude_none=True)
        unset_data = {key: "" for key, value in model.model_dump().items() if value is None}
        if "createdAt" in update_data: del update_data["createdAt"]
        update_query = { "$set": {  "updatedAt": datetime.datetime.now,**update_data }}
        if unset_data:  update_query["$unset"] = unset_data
        count = UserSchema.update({"_id": obj_id}, update_query)
        return self.get_model(obj_id) if count != 0 else None
    def delete_model(self, _id):
        count = UserSchema.update({"_id": _id}, {"$set": {"deletedAt": datetime.datetime.now()}})
        return count
