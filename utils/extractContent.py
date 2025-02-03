import json
import ast

def extract_json(input:str) -> dict:
    try:
        start_index = input.find("{")
        end_index = input.rfind("}") + 1
        return json.loads(input[start_index:end_index])
    except json.JSONDecodeError:
        print("⚠️\tCannot extract Json from input prompt!")
        return {}

def extract_list(response: str) -> list:
    try:
        start_index = response.find("[")
        end_index = response.rfind("]") + 1
        
        list_part = response[start_index:end_index].strip()
        
        extracted_list = ast.literal_eval(list_part)
        
        if isinstance(extracted_list, list):
            return extracted_list
        else:
            return []
    except Exception as e:
        print(f"Error extracting list: {e}")
        return []