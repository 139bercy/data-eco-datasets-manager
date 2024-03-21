import itertools


class Dataset:
    def __init__(
        self,
        created: str,
        updated: str,
        dataset_id: str,
        title: str,
        publisher: str,
        published: bool,
        restricted: bool,
        download_count: int = None,
        api_call_count: int = None,
        popularity_score: float = None,
        records_size: int = None,
    ):
        self.created = created
        self.updated = updated
        self.dataset_id = dataset_id
        self.title = title
        self.publisher = publisher
        self.published = published
        self.restricted = restricted
        self.download_count = download_count
        self.api_call_count = api_call_count
        self.popularity_score = popularity_score
        self.records_size = records_size

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def update(self, download_count: int, api_call_count: int, popularity_score: float, records_size: int):
        self.download_count = download_count
        self.api_call_count = api_call_count
        self.popularity_score = round(popularity_score, 1)
        self.records_size = records_size

    def __str__(self):
        return f"<Dataset: {self.dataset_id}>"

    def __repr__(self):
        return f"<Dataset: {self.__dict__}>"