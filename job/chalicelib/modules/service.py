from ..modules.schema import JobSchema
from ..modules.model import JobModel
from pymongoose import methods
import datetime
from bson import ObjectId

class JobService:

    def _cast_fields(self, model):
        for field in ["_id", "createdAt", "updatedAt" , "deletionDate"]:
            if field in model:
                model[field] = str(model[field])
        return model

    def get_all_models(self, filters):
        query = filters.apply()
        models = JobSchema.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={"createdAt": -1}
        )
        serialized_models = [self._cast_fields(model) for model in models]
        return serialized_models

    def get_model(self, _id):
        model = JobSchema.find_by_id(_id, parse=False)
        return self._cast_fields(model) if model else None

    def add_model(self, model: dict):
        job = JobModel(**model)
        serialized_data = job.dict(exclude_none=True)
        inserted_model = methods.insert_one("Job", serialized_data)
        return self.get_model(inserted_model)


    def update_model(self, _id, model: dict):
        obj_id = ObjectId(_id)
        job = JobModel(**model)
        job.updatedAt = datetime.datetime.now()
        update_data = job.model_dump(exclude_none=True)
        unset_data = {key: "" for key, value in job.model_dump().items() if value is None}

        update_query = {"$set": update_data}
        if unset_data:
            update_query["$unset"] = unset_data
        count = JobSchema.update({"_id": obj_id}, update_query)
        return self.get_model(obj_id) if count != 0 else None


    def delete_model(self, _id):
        count = JobSchema.update({"_id": _id}, {"$set": {"deletionDate": datetime.datetime.now()}})
        return count
    
    def update_status(self, job_id, status):
        if not status:
            return None
        obj_id = ObjectId(job_id)
        count = JobSchema.update({"_id": obj_id}, {"$set": {"status": status, "updatedAt": datetime.datetime.now()}})
        return self.get_model(obj_id) if count != 0 else None

