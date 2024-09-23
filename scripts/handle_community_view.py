import json

from community import add_community_custom_view

ds = []

with open("data/xxxx-xx-xx-datasets.json", "r") as file:
    data = json.load(file)["results"]
    for dataset in data:
        name = dataset.get("metadata").get("default").get("title", {}).get("value", None)
        ds_id = dataset["uid"]
        print()
        print(dataset["dataset_id"])
        if not dataset["is_published"]:
            print(f"Dataset: '{name}' is not published. Skipping...")
            continue
        if dataset["is_restricted"]:
            print(f"Dataset: '{name}' is restricted. Skipping...")
            continue
        elif (
            "custom_view_title" in dataset["metadata"]["visualization"]
            and dataset["metadata"]["visualization"]["custom_view_title"]["value"] == "Contributions"
        ):
            print(f"Dataset: '{name}' already have community view. Skipping...")
        else:
            add_community_custom_view(dataset_uid=ds_id)
