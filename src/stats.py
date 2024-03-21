from adapters.api import explore_api_dataset_dto


def handle_no_dataset_case():
    return {"api_call_count": None, "download_count": None, "popularity_score": None, "records_size": None}


def get_dataset_stats_report(data: dict, pprint: bool):
    if data["total_count"] == 0:
        report = handle_no_dataset_case()
    else:
        report = explore_api_dataset_dto(data["results"][0])
    if pprint:
        print(report)
    return report
