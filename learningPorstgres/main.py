import psycopg2
from config import *

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

with connection.cursor() as cursor:
    cursor.execute(insert_query, (user_id, user_name, user_email))
    print(cursor.fetchone())

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT version()"
    )
    print(cursor.fetchone())
