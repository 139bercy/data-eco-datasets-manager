# url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
# dataset = "liste-des-complements-alimentaires-declares"
# params = {"where": f"dataset_id='{dataset}'", "include_app_metas": True}

# data = query_ods(url=url, params=params)


def get_dataset_quality_ratio(data: dict, dcat: bool = True, pprint: bool = False):
    if data["total_count"] == 0:
        report = handle_no_dataset_case()
    else:
        report = get_report(data, dcat)
    if pprint:
        print(report)
    return report


def get_report(data: dict, dcat: bool):
    description = get_fields_description_quality_ratio(dataset=data, pprint=False)
    default = get_metadata_quality_ratio(dataset=data, name="default", pprint=False)
    if dcat:
        dcat = get_metadata_quality_ratio(dataset=data, name="dcat", pprint=False)
    else:
        dcat = {"ratio": "N/A"}
    total = get_global_quality_ratio([description["ratio"], default["ratio"], dcat["ratio"]])
    report = {
        "description_metadata_percent": description["ratio"],
        "default_metadata_percent": default["ratio"],
        "dcat_metadata_percent": dcat["ratio"],
        "quality_ratio": total,
    }
    return report


def get_global_quality_ratio(metrics):
    data = [item for item in metrics if type(item) == float or type(item) == int]
    result = round(sum(data) / len(data))
    return result


def handle_no_dataset_case():
    report = {
        "description_metadata_percent": "N/A",
        "default_metadata_percent": "N/A",
        "dcat_metadata_percent": "N/A",
        "quality_ratio": "N/A",
    }
    return report


def get_metadata_quality_ratio(dataset: dict, name: str, pprint: bool = False):
    metadata = dataset.get("results", [])[0].get("metas", {}).get(name, {})
    total_fields = count_metadata_field(metadata=metadata)
    incomplete = calculate_incomplete_metadata(metadata=metadata)
    ratio = calculate_quality_ratio(total_fields, incomplete)
    result = {
        "metadata": name,
        "total_fields": total_fields,
        "incomplete": incomplete,
        "ratio": ratio,
    }
    if pprint:
        print(result)
    return result


def get_fields_description_quality_ratio(dataset: dict, pprint: bool = False):
    fields = dataset.get("results", [])[0].get("fields", [])

    fields_count = len(fields)
    description_count = sum(1 for field in fields if field.get("description") is None)

    count = fields_count - description_count
    ratio = calculate_quality_ratio(total=fields_count, count=count)
    result = {"fields": fields_count, "description": count, "ratio": ratio}
    if pprint:
        print(result)
    return result


def calculate_incomplete_metadata(metadata: dict):
    values = [key for key, value in metadata.items() if value is not None]
    count = len(values)
    return count


def calculate_quality_ratio(total: int, count: int) -> float or str:
    try:
        result = int(round((count / total) * 100))
        return result
    except ZeroDivisionError:
        return "N/A"


def count_metadata_field(metadata):
    return len(metadata)


# export(data, "dataset-sample.json")
# with open("../dataset-sample.json") as file:
#     data = json.load(file)
#     get_dataset_quality_ratio(data=data, pprint=True)
