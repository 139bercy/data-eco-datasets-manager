def get_dataset_quality_score(data: dict, dcat: bool = True, pprint: bool = False):
    if data["total_count"] == 0:
        report = handle_no_dataset_case()
    else:
        report = get_report(data, dcat)
    if pprint:
        print(report)
    return report


def get_report(data: dict, dcat: bool):
    description = get_fields_description_quality_score(dataset=data, pprint=False)
    default = get_metadata_quality_score(dataset=data, name="default", pprint=False)
    if dcat:
        dcat = get_metadata_quality_score(dataset=data, name="dcat", pprint=False)
    else:
        dcat = {"score": None}
    total = get_global_quality_score([description["score"], default["score"], dcat["score"]])
    report = {
        "description_score": description["score"],
        "default_score": default["score"],
        "dcat_score": dcat["score"],
        "quality_score": total,
    }
    return report


def get_global_quality_score(metrics):
    data = [item for item in metrics if type(item) == float or type(item) == int]
    result = round(sum(data) / len(data))
    return result


def handle_no_dataset_case():
    report = {
        "description_score": None,
        "default_score": None,
        "dcat_score": None,
        "quality_score": None,
    }
    return report


def get_metadata_quality_score(dataset: dict, name: str, pprint: bool = False):
    metadata = dataset.get("results", [])[0].get("metas", {}).get(name, {})
    total_fields = count_metadata_field(metadata=metadata)
    incomplete = calculate_incomplete_metadata(metadata=metadata)
    score = calculate_quality_score(total_fields, incomplete)
    result = {
        "metadata": name,
        "total_fields": total_fields,
        "incomplete": incomplete,
        "score": score,
    }
    if pprint:
        print(result)
    return result


def get_fields_description_quality_score(dataset: dict, pprint: bool = False):
    fields = dataset.get("results", [])[0].get("fields", [])

    fields_count = len(fields)
    description_count = sum(1 for field in fields if field.get("description") is None)

    count = fields_count - description_count
    score = calculate_quality_score(total=fields_count, count=count)
    result = {"fields": fields_count, "description": count, "score": score}
    if pprint:
        print(result)
    return result


def calculate_incomplete_metadata(metadata: dict):
    values = [key for key, value in metadata.items() if value is not None]
    count = len(values)
    return count


def calculate_quality_score(total: int, count: int) -> float or str:
    try:
        result = int(round((count / total) * 100))
        return result
    except ZeroDivisionError:
        return None


def count_metadata_field(metadata):
    return len(metadata)
