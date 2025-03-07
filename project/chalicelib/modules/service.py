import datetime
import os
from bson import ObjectId
from cryptography.fernet import Fernet
from pymongoose import methods
from ..modules.messages import Messages
from ..modules.model import Project
from ..modules.schema import ProjectSchema

class ProjectService:
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')

    def _cast_fields(self, model):
        for field in ["_id", "createdAt", "updatedAt", "start_date"]:
            if field in model:
                model[field] = str(model[field])
        return model

    def get_all_models(self, filters):
        query = filters.apply()
        models = ProjectSchema.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={"createdAt": -1}
        )
        total_count = ProjectSchema.count(query)
        serialized_models = [self._cast_fields(model) for model in models]
        return {
            "total": total_count,
            "results": serialized_models
        }

    def get_model(self, _id):
        model = ProjectSchema.find_by_id(_id, parse=False)
        return self._cast_fields(model) if model else None

    def add_model(self, model: dict):
        git_token = model.get("gitToken")
        if git_token:
            model["gitToken"] = self.encrypt_token(git_token)
        project = Project(**model)
        serialized_data = project.dict(exclude_none=True)
        inserted_model = methods.insert_one("Project", serialized_data)
        return self.get_model(inserted_model)

    def update_git_token(self, project_id, git_token):
        if not git_token:
            return None
        obj_id = ObjectId(project_id)
        encrypted_token = self.encrypt_token(git_token)
        count = ProjectSchema.update({"_id": obj_id}, {"$set": {"gitToken": encrypted_token, "updatedAt": datetime.datetime.now()}})
        return self.get_model(obj_id) if count != 0 else None

    # def delete_model(self, _id):
    #     count = ProjectSchema.update({"_id": _id}, {"$set": {"deletionDate": datetime.datetime.now()}})
    #     return count

    def deactivate_project(self, _id, definitive):
        obj_id = ObjectId(_id)
        if definitive is False:
            result = ProjectSchema.update(
                {"_id": obj_id},
                {"$set": {"deactivated": True, "updatedAt": datetime.datetime.now()}}
            )
        elif definitive is True:
            result = ProjectSchema.update(
                {"_id": obj_id},
                {"$set": {"deletionDate": datetime.datetime.now()}}
            )
        else:
            raise ValueError(Messages.ERROR_VALIDATION_TYPE)

        # Check if the update operation modified any document
        return self.get_model(obj_id) if result > 0 else None


    def encrypt_token(self, token):
        cipher = self._get_cipher()
        return cipher.encrypt(token.encode()).decode()

    def decrypt_token(self, encrypted_token):
        cipher = self._get_cipher()
        return cipher.decrypt(encrypted_token.encode()).decode()

    def _get_cipher(self):
        return Fernet(self.ENCRYPTION_KEY)
