import json


def serialize_dump_json(data):
    result = []

    for record in data:
        result.append(json.dumps(record))

    return result


def serialize_load_json(data):
    result = []

    for record in data:
        result.append(json.loads(record))

    return result