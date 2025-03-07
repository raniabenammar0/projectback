class Filters:
    def __init__(self, **kwargs):
        self.limit = kwargs.get("limit")
        self.page = kwargs.get("page")
        self.userId = kwargs.get("userId")

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
            for key, value in {"user.userId": self.userId}.items()
            if value is not None

        }
        query_filter["$or"] = [{ "deletionDate": { "$exists": False } }, { "deletionDate": None }]


        return query_filter

