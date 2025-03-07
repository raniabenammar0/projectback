class Filters:
    def __init__(self, **kwargs):
        self.limit = int(kwargs.get("limit", 10))
        self.page = int(kwargs.get("page", 1))
        self.email = kwargs.get("email", None)
        self.cognito_sub = kwargs.get("cognito.sub", None)


        self.skip = (self.page - 1) * self.limit  # Calculate skip for pagination

    def apply(self):
        query_filter = {
            key: value
            for key, value in {
                "email": self.email,
                "cognito.sub": self.cognito.sub,
            }.items()
            if value is not None
        }

        query_filter["$or"] = [{"deletedAt": {"$exists": False}}, {"deletedAt": None}]

        print(f"Constructed query filter: {query_filter}")  # Debugging line

        return query_filter
