import os
import psycopg2
import psycopg2.extras
from utils import response, create_data_process
from pagination import pagination

def db_connect():
    conn = psycopg2.connect(database= os.environ['DATABASE'], user= os.environ['USER'], password= os.environ['PASSWORD'], host=os.environ['HOST'], port= os.environ['PORT'])
    return conn
    

def list_view(table, table_fields, page_size=None, page=None, search=None, search_fields=None):
    query = f"select {','.join(table_fields)} from {table}"
    try:
        conn = db_connect()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        count_sql = f"SELECT COUNT(*) FROM {table} "
        
        
        # Filter 
        # if filter_fields:
        #   filter_field_text = ' AND '.join([f"{table}.{key} = {values}" for key,values in filter_fields.items()])
        #   q = f" WHERE {filter_field_text} AND " if search else f" WHERE {filter_field_text} "
        #   sql = sql + q
        #   count_sql = count_sql + q
        
        # search
        if search:
            search = search.upper()
            search_field_text = ' OR '.join([f"UPPER({x}) LIKE '%{search}%'" for x in search_fields])
            q = f" WHERE {search_field_text} "
            query = query+q
            count_sql = count_sql + q

        # Pagination
        cursor.execute(count_sql)
        count = cursor.fetchone().get('count')
        pagination_data = pagination(page_size, page, count)
        if pagination_data.get('status') !=200:
            conn.close()
            return response(message=pagination_data['message'], status = pagination_data['status'])
            
        meta_data = {
            "total": count,
            "page_size": pagination_data.get('page_size'),
            "page": pagination_data.get('page'),
            "next_page": pagination_data.get('next_page'),
            "previous_page" : pagination_data.get('previous_page')
            }
            
        # Main Query
        query = query + pagination_data.get('query')
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()
        return response(data=data, meta_data = meta_data, message= 'Success', status= 200)
    
    except Exception as e:
        conn.close()
        return response(message= str(e), status= 400)



def retrieve_view(table, table_fields, id):
    query = f"select {','.join(table_fields)} from {table}  WHERE id = {id}"
    try:
        conn = db_connect()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        data = cursor.fetchone()
        conn.close()
        if data:
            return response(data=data, message= 'Success', status= 200)
        else:
            return response(message= f'{table.capitalize()} Not Found', status= 400)
    
    except Exception as e:
        conn.close()
        return response(message= str(e), status= 400)
        
        
def create_view(table, table_fields, request_data):
    process_data = create_data_process(request_data, table_fields)
    query = f"INSERT INTO {table}({process_data['keys']}) VALUES ({process_data['values_type']}) RETURNING id, {process_data['keys']}"

    try:
        conn = db_connect()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(query, process_data['values'])
        data = cursor.fetchone()
        conn.commit()
        conn.close()
        return response(data=data, message= 'Success', status= 200)

    except Exception as e:
        conn.close()
        return response(message= str(e), status= 400)
    
        

def delete_view(table, id):
    query = f"DELETE FROM {table} WHERE id = {id}"
    try:
        conn = db_connect()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        rows_count = cursor.rowcount
        if rows_count == 1:
            conn.commit()
            conn.close()
            return response(message= 'Deleted', status= 200)
        else:
            conn.close()
            return response(message= f'{table.capitalize()} Not Found', status= 400)
    
    except Exception as e:
        conn.close()
        return response(message= str(e), status= 400)
        

def update_view(table, update_process_data, id):
    try:
        conn = db_connect()
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute("""SELECT id FROM users WHERE id = {};""".format(id))
        if cursor.rowcount == 1:
            sql_text = f"UPDATE users SET {update_process_data} WHERE users.id = {id} RETURNING id, username, phone, email, first_name, last_name;"
            cursor.execute("""{}""".format(sql_text))
            data = cursor.fetchone()
            conn.commit()
            conn.close()
            return response(data=data, message= 'Updated', status= 200)
        
        else:
            conn.close()
            return response(message= 'User Is not found', status= 400)
    
    except Exception as e:
        conn.close()
        return response(message= str(e), status= 400)