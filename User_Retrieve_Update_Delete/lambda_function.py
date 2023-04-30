import os
import json
from utils import update_data_process
from rds import retrieve_view, delete_view, update_view

def lambda_handler(event, context):
    # User Retrieve View
    if event.get('httpMethod') == "GET":
        user_id = event.get('pathParameters').get('id')
        table = "users"
        table_fields = ("id","username", "email", "phone", "first_name", "last_name")
        data = retrieve_view(table = table, table_fields = table_fields, id = user_id )
        return data
        
    # User Delete View
    if event.get('httpMethod') == "DELETE":
        user_id = event.get('pathParameters').get('id')
        table = "users"
        data = delete_view(table = table, id = user_id )
        return data
    
    # User Update View
    if event.get('httpMethod') == "PATCH":
        user_id = event.get('pathParameters').get('id')
        request_data = json.loads(event['body'])
        update_process_data = update_data_process(request_data,('email','phone','first_name','last_name'))
        table = "users"
        data = update_view(table = table, update_process_data = update_process_data, id = user_id )
        return data