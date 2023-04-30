import json

def response(**kwargs):
    data = kwargs.get('data')
    message = kwargs.get('message')
    status = kwargs.get('status')
    meta_data = kwargs.get('meta_data')
    body = {
        'success': True if status < 400 else False,
        'message': message
        }
        
    if meta_data:
        body['meta_data'] = meta_data
        
    if data:
        body['body'] = data
        

    return {
            "statusCode": status,
            "body": json.dumps(body)
        }
        

# def entries_to_remove(data: dict, removable_keys: tuple) -> dict:
#     for i in data:
#         for k in removable_keys:
#             i.pop(k, None)
#     return data

def update_data_process(request_data, fields):
    change_data = ""
    for key, value in request_data.items():
        if key in fields:
            change_data = change_data + key + " = " + f"'{value}'" + ", " if isinstance(value, str) else change_data + key + " = " + f"{value}" + ", "
    
    return change_data[0:-2]
    

def create_data_process(request_data, fields):
    keys = ", ".join(fields)
    values_type = ""
    values = ()
    
    for key in fields:
        values += (request_data.get(key),)
        if isinstance(request_data.get(key), str):
            values_type = values_type + '%s,'
        elif isinstance(request_data.get(key), int):
            values_type = values_type + '%f,'
            
    return {'keys': keys, 'values': values, 'values_type': values_type[:-1]}