import json

def extract_json(input:str) -> dict:
    try:
        start_index = input.find("{")
        end_index = input.rfind("}") + 1
        return json.loads(input[start_index:end_index])
    except json.JSONDecodeError:
        print("⚠️\tCannot extract Json from input prompt!")
        return {}