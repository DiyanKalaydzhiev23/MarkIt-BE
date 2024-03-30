import json
import decouple
import requests


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


def get_summary_for_extracted_text(
        data: list,
        prompt="Make analytics ask a market researcher for this data"
):
    headers = {"Authorization": f"Bearer {decouple.config('EDEN_AI_API_KEY')}"}

    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": "openai",
        "text": prompt + "".join(data),
        "chatbot_global_action": "Act as a market researcher doing research on a project. "
                                 "Give structured data about the type of people in the text, revenue, sales etc."
                                 "In the response give only data that matters and makes sense."
                                 "Remember from which file comes which data!",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 500,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    print(result['openai']['generated_text'])

    return result['openai']['generated_text']
