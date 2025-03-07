import datetime
from pymongoose import methods
from ..modules.model import MergeRequest
from ..modules.schema import MergeRequestSchema
from bson import ObjectId 
from bson.errors import InvalidId


class MergeRequestService:

    def _cast_fields(self, model):
        for field in ["_id", "createdAt", "updatedAt", "start_date"]:
            if field in model:
                model[field] = str(model[field])
        return model

    def get_all_models(self, filters):
        query = filters.apply()
        models = MergeRequestSchema.find(
            query,
            limit=filters.limit,
            skip=filters.skip,
            sort={"createdAt": -1}
        )
        total_count = MergeRequestSchema.count(query)
        serialized_models = [self._cast_fields(model) for model in models]
        return {
            "total": total_count,
            "results": serialized_models
        }

    def get_model(self, _id):
        model = MergeRequestSchema.find_by_id(_id, parse=False)
        return self._cast_fields(model) if model else None

    def update_model(self, model: dict):
    
     obj_id = ObjectId(model["_id"])
     mergeRequest = MergeRequest(**model)
     mergeRequest.updatedAt = datetime.datetime.now()
     serialized_data = mergeRequest.dict(exclude_none=True)
     count = MergeRequestSchema.update({"_id": obj_id}, {"$set": serialized_data})
     return self.get_model(obj_id) if count != 0 else None

        
 
     


    def add_model(self, model: dict):
        mergeRequest = MergeRequest(**model)
        serialized_data = mergeRequest.dict(exclude_none=True)
        inserted_id = methods.insert_one("MergeRequest", serialized_data)
        return inserted_id

    def delete_model(self, _id):
        count = MergeRequestSchema.update({"_id": _id}, {"$set": {"deletionDate": datetime.datetime.now()}})
        return count
