import os
import json
from rds import list_view, create_view

def lambda_handler(event, context):
    # User List View
    if event.get('httpMethod') == "GET":
        queryParams = event.get('queryStringParameters')
        page_size = queryParams.get('page_size') if queryParams else 0
        page = queryParams.get('page') if queryParams else 0
        search = queryParams.get('search') if queryParams else None
        search_fields = ['username', 'email'] if search else []
        table = "users"
        table_fields = ("id","username", "email", "phone", "first_name", "last_name")
        data = list_view(table = table, table_fields = table_fields, page_size = page_size, page = page, search = search, search_fields=search_fields )
        return data
        
    # User Craete       
    if event.get('httpMethod') == "POST":
        request_data = json.loads(event['body'])
        table = 'users'
        table_fields = ("username", "phone", "email", "password")
        data = create_view(table=table, table_fields=table_fields, request_data=request_data)
        return data