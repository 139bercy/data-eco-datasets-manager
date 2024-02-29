import json


def response_to_json(response):
    result = json.loads(response.text)
    return result


def pprint(response):
    result = json.dumps(response, indent=2, ensure_ascii=False)
    print(result)
    return result


def export(response, filename):
    with open(filename, "w") as file:
        json.dump(response, file, indent=2, ensure_ascii=False)
    print(f"File {filename} has been created!")
