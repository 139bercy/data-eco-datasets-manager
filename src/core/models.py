import hashlib


class Dataset:
    def __init__(
        self,
        buid: str,
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
        size: str = None,
        records_count: int = None,
        link: str = None,
        description_score: float = None,
        default_score: float = None,
        dcat_score: float = None,
        quality_score: float = None,
    ):
        self.buid = buid
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
        self.size = size
        self.records_count = records_count
        self.link = link
        self.description_score = description_score
        self.default_score = default_score
        self.dcat_score = dcat_score
        self.quality_score = quality_score

    @classmethod
    def create(cls, *args, **kwargs):
        kwargs["buid"] = get_key(f"{kwargs['created']}{kwargs['dataset_id']}")
        return cls(**kwargs)

    def update(
        self,
        download_count: int,
        api_call_count: int,
        popularity_score: float,
        records_size: int,
        size: str,
        records_count: int,
    ):
        self.download_count = download_count
        self.api_call_count = api_call_count
        self.popularity_score = round(popularity_score, 1)
        self.records_size = records_size
        self.size = size
        self.records_count = records_count

    def __str__(self):
        return f"<Dataset: {self.dataset_id}>"

    def __repr__(self):
        return f"<Dataset: {self.__dict__}>"


def sha256_hash_string(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode("utf-8"))
    return sha256_hash.hexdigest()


def get_key(chain):
    """
    Utiliser les 8 premiers caractères d'un hash est à ce stade suffisamment discriminant pour éviter les collisions.
    """
    return sha256_hash_string(chain)[0:8]
