import datetime
import time
import psycopg2
import random
import string


db_name = 'database'
db_user = 'username'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'


def generate_random_string():
    length = random.randint(1, 100)
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def create_table():
    cursor.execute("""SELECT EXISTS (SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'test_table');
    """)
    if not cursor.fetchall()[0][0]:
        cursor.execute("""CREATE TABLE test_table (
        id integer PRIMARY KEY,
        data varchar(100) NOT NULL,
        date timestamp NOT NULL DEFAULT CURRENT_DATE
        )""")
        conn.commit()
    else:
        cursor.execute("""DELETE FROM test_table""")


def use():
    while True:
        for i in range(1, 31):
            data = generate_random_string()
            date = str(datetime.datetime.now())

            query = """
            INSERT INTO test_table (id, data, date)
            VALUES
            (%s, %s, %s)
            """
            insert_line = (i, data, date)
            cursor.execute(query, insert_line)
            conn.commit()

            # для дебага
            cursor.execute("""SELECT * FROM test_table""")
            print(cursor.fetchall())
            # --------------------------------------------

            time.sleep(60)
        cursor.execute("""DELETE FROM test_table""")


if __name__ == '__main__':
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        cursor = conn.cursor()
        create_table()
        use()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
    finally:
        print('db end')
