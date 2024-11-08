import psycopg2
from psycopg2._json import Json

from config import *
from db import quiz

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

# with connection.cursor() as cursor:
#     cursor.execute(
#         f"INSERT INTO public.tests (test_name, user_id, questions) VALUES ('first_test', 423, {Json(quiz)})")
#     connection.commit()

user_id = 1713420283

with connection.cursor() as cursor:
    cursor.execute(
        f"SELECT * FROM tests WHERE user_id = {user_id}")
    connection.commit()

    results = cursor.fetchone()

    print(results[0])
