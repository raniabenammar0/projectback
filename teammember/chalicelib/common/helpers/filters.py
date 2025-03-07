class Filters:
    def __init__(self, **kwargs):
        self.limit = kwargs.get("limit")
        self.page = kwargs.get("page")
        self.email = kwargs.get("email")
        self.status = kwargs.get("status")
        self.projectDataBaseId = kwargs.get('projectDataBaseId')

        if self.limit is not None and self.page is not None:
            self.limit = int(self.limit)
            self.page = int(self.page)
            self.skip = (self.page - 1)*self.limit
        else:
            self.limit = None
            self.skip = 0
    def apply(self):
        query_filter = {
            key: value
            for key, value in {"user.email": self.email,"status": self.status}.items()
            if value is not None
        }
        if self.projectDataBaseId:
            query_filter['project.projectDataBaseId'] = self.projectDataBaseId

        if self.email:
            query_filter['user.email'] = self.email

        query_filter["$or"] = [{ "deletedAt": { "$exists": False } }, { "deletedAt": None }]


        return query_filter

