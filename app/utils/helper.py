from bson import ObjectId

def json_converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: json_converter(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [json_converter(item) for item in obj]
    return obj