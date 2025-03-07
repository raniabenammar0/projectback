import datetime
from bson import ObjectId
from pymongoose import methods
from ..modules.model import TeamMember
from ..modules.schema import TeamMemberSchema

class TeamMemberService:

    def _cast_fields(self, model):
        for field in ["_id", "createdAt", "updatedAt", "startDate"]:
            if field in model:
                model[field] = str(model[field])
        return model

    def get_all_models(self, filters):
        query = filters.apply()

        if filters.projectDataBaseId:
            query['project.projectDataBaseId'] = filters.projectDataBaseId
        if filters.email:
            query['user.email'] = filters.email

        models = TeamMemberSchema.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={"createdAt": -1}
        )
        total_count = TeamMemberSchema.count(query)
        serialized_models = [self._cast_fields(model) for model in models]
        return {
            "total": total_count,
            "results": serialized_models
        }



    def get_model(self, _id):
        model = TeamMemberSchema.find_by_id(_id, parse=False)
        return self._cast_fields(model) if model else None

    def update_status(self, team_member_id, status):
        if not status:
            return None
        obj_id = ObjectId(team_member_id)
        count = TeamMemberSchema.update({"_id": obj_id}, {"$set": {"status": status, "updatedAt": datetime.datetime.now() }})
        return self.get_model(obj_id) if count != 0 else None

    def update_role(self, team_member_id, role):
            if not role:
                return None
            obj_id = ObjectId(team_member_id)
            count = TeamMemberSchema.update({"_id": obj_id}, {"$set": {"role": role, "updatedAt": datetime.datetime.now() }})
            return self.get_model(obj_id) if count != 0 else None

    def update_user(self, _id, user):
        if not user:
            return None
        obj_id = ObjectId(_id)
        count = TeamMemberSchema.update({"_id": obj_id},
                                        {"$set": {"user": user, "updatedAt": datetime.datetime.now()}})
        return self.get_model(obj_id) if count != 0 else None

    def update_team_member(self, _id, team_member: TeamMember):
        if not _id:
            return None
        obj_id = ObjectId(_id)
        team_member.updatedAt = datetime.datetime.now()
        update_data = team_member.model_dump(exclude_none=True)
        unset_data = {key: "" for key, value in team_member.model_dump().items() if value is None}
        if "createdAt" in update_data: del update_data["createdAt"]
        update_query = {"$set": {**update_data}}
        if unset_data:
            update_query["$unset"] = unset_data
        count = TeamMemberSchema.update({"_id": obj_id}, update_query)
        return self.get_model(obj_id) if count != 0 else None


    def add_model(self, model: TeamMember):
        user = TeamMemberSchema.find_one({
            "user.email": model.user.email,
            "project.projectDataBaseId": model.project.projectDataBaseId
        })
        if not user :
            now = datetime.datetime.now()
            serialized_data = model.model_dump(exclude_none=True)
            serialized_data["createdAt"] = now
            serialized_data["updatedAt"] = now
            inserted_model = methods.insert_one("TeamMember", serialized_data)
            return self.get_model(inserted_model)
        if user :
            raise ValueError(f"Email '{model.user.email}' already registered")



    def delete_model(self, _id):
        count = TeamMemberSchema.update({"_id": _id}, {"$set": {"deletedAt": datetime.datetime.now() }})
        return count

    def check_changes(self, model: dict, data: dict) -> bool:

        return(
                data.get('user', {}).get('email') == model.get('user', {}).get('email') and
                data.get('user', {}).get('userId') == model.get('user', {}).get('userId') and
                data.get('user', {}).get('userName') == model.get('user', {}).get('userName')
        )