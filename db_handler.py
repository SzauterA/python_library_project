import psycopg2
from dotenv import load_dotenv
import os


#configuration data from the enviroment file
load_dotenv()
config = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

#connection to the database and cursor creation
def connect():
    try:
        conn = psycopg2.connect(**config) 
        cur = conn.cursor()
        return conn, cur
    except (psycopg2.DatabaseError, Exception) as err:
        print(err)
        return None, None

#creating the schema and tables
def create_schema(conn, cur):
    try:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS library;
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS library.customers (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                birth DATE NOT NULL,
                password TEXT NOT NULL,
                permission INTEGER NOT NULL
            );
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS library.books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(50) NOT NULL,
                author VARCHAR(50) NOT NULL,
                isbn VARCHAR(20) UNIQUE NOT NULL,
                available INTEGER NOT NULL
            );
        """)

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    
#inserting some books data as an example
def insert_data(conn, cur):
    books_data = [
        ('The Shadow Over Innsmouth', 'H.P. Lovecraft', '9781495393082', 5),
        ('At the Mountains of Madness', 'H.P. Lovecraft', '9780241341315', 3),
        ('The Shadow Out of Time', 'H.P. Lovecraft', '9780967321530', 2),
        ('The Shining', 'Stephen King', '9780307743657', 5),
        ('The Outsider', 'Stephen King', '9781501180989', 3),
        ('Dracula', 'Bram Stoker', '9781503261389', 6)
    ]

    try:
        cur.executemany("""
            INSERT INTO library.books (title, author, isbn, available)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (isbn) DO NOTHING
        """, books_data)  

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

#main logic to connect, create schema and insert data
def connection_main():
    conn, cur = connect()
    if conn is not None and cur is not None:
        create_schema(conn, cur)
        insert_data(conn, cur)
        cur.close()
        conn.close()
    else:
        print("Unable to connect to database.")

connection_main()