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
    ):
        self.created = created
        self.updated = updated
        self.dataset_id = dataset_id
        self.title = title
        self.publisher = publisher
        self.published = published
        self.restricted = restricted
        self.download_count = None

    @classmethod
    def create(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def update(self, download_count: int):
        self.download_count = download_count



    def __str__(self):
        return f"<Dataset: {self.dataset_id}>"
