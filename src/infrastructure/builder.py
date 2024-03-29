import tinydb


class TinyDBQueryBuilder:
    def __init__(self, db):
        self.db = db
        self.query = tinydb.Query()
        self.filters = []

    def add_filter(self, field, operator, value):
        if operator == "==":
            self.filters.append(self.query[field] == value)
        elif operator == "!=":
            self.filters.append(self.query[field] != value)
        elif operator == ">":
            self.filters.append(self.query[field] > value)
        elif operator == ">=":
            self.filters.append(self.query[field] >= value)
        elif operator == "<":
            self.filters.append(self.query[field] < value)
        elif operator == "<=":
            self.filters.append(self.query[field] <= value)
        elif operator == "contains":
            self.filters.append(self.query[field].search(value))
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def build_query(self):
        if not self.filters:
            return None
        else:
            combined_filter = self.filters[0]
            for filter_ in self.filters[1:]:
                combined_filter &= filter_
            return combined_filter
