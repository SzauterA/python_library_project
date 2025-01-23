from db_handler import connect
from psycopg2 import sql
import textwrap
import datetime
import os
import re
import patterns

#listing all books
def listing(cur):
    print("You chose to list the books of the library.")
    query = "SELECT * FROM library.books"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return rows

#searching in the list
def searching(cur):
    while True:
        choice = input("Do you want to search in the list? yes/no: ").strip().lower()
        if choice == 'yes':
            search = input('Expression you want to search for: ').strip()
            search_pattern = f"%{search}%"
            
            query = """
            SELECT * FROM library.books 
            WHERE title LIKE %s 
            OR author LIKE %s 
            OR isbn LIKE %s 
            OR CAST(available AS TEXT) LIKE %s
            """
            cur.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            filtered_rows = cur.fetchall()
            
            if filtered_rows:
                print('Search result:')
                for row in filtered_rows:
                    print(row)
                log_searches(cur, search, filtered_rows)
            else:
                print("No books found matching the search parameters.")
        elif choice == 'no':
            return
        else:
            print("Invalid input. Please only choose from 'yes/no'!")
            continue
    
#logging search results
def log_searches(cur, search, filtered_rows):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"Search Keyword: {search}\n"
    log_entry += f"Search Time: {timestamp}\n"
    log_entry += "Search Results:\n"
    for result in filtered_rows:
        log_entry += f"{result}\n"
    log_entry += "\n"

    with open("search_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
    print("Search saved.")
    
#modify a book's detail
def modification(cur):
    print("You chose to update a book's detail.")
    while True:
        schema_name = 'library'
        table_name = 'books'
        row_name = 'title'
        row_value = input("The book's title: ")
        cur.execute("SELECT title FROM library.books WHERE title = %s", (row_value,))
        if cur.fetchone() is None:
            print("Book not found in the library. Please enter a valid title.")
            continue
        else:
            while True:
                column_name = input("Detail to change (title/author/isbn/available): ")
                if column_name not in ['title', 'author', 'isbn', 'available']:
                    print("Please choose only from the given details!")
                    continue
                else:
                    new_value = input("New value: ")
                    if column_name == 'title' and not re.match(patterns.title_pattern, new_value):
                        print("Invalid title format. Please try again.")
                        continue
                    elif column_name == 'author' and not re.match(patterns.author_pattern, new_value):
                        print("Invalid author format. Please try again.")
                        continue
                    elif column_name == 'isbn' and not re.match(patterns.ISBN_pattern, new_value):
                        print("Invalid ISBN format. Please try again.")
                        continue
                    elif column_name == 'available' and not re.match(patterns.available_pattern, new_value):
                        print("Invalid number format. Please try again.")
                        continue

                query = sql.SQL("UPDATE {schema}.{table} SET {column} = %s WHERE {row} = %s").format(
                    schema=sql.Identifier(schema_name),
                    table=sql.Identifier(table_name),
                    column=sql.Identifier(column_name),
                    row=sql.Identifier(row_name)
                )
                cur.execute(query, (new_value, row_value))
                print("Detail changed successfully.")
                return

#remove a book from the list
def deletion(cur):
    print("You chose to delete a book from the list.")
    while True:
        title = input("Title: ")
        cur.execute("SELECT title FROM library.books WHERE title = %s", (title,))
        if cur.fetchone() is None:
            print("Book not found in the library. Please enter a valid title.")
        else:
            break

    query = "DELETE FROM library.books WHERE title = %s"
    cur.execute(query, (title,))
    print("Book successfully deleted from the library.")

#add a new book to the list
def addition(cur):
    print("You chose to add a new book to the list.")
    while True:
        title = input("Title: ")
        if not re.match(patterns.title_pattern, title):
            print("Invalid title format. Please try again.")
            continue
        break
    
    while True:
        author = input("Author: ")
        if not re.match(patterns.author_pattern, author):
            print("Invalid author format. Please try again.")
            continue
        break
    
    while True:
        isbn = input("ISBN number: ")
        if not re.match(patterns.ISBN_pattern, isbn):
            print("Invalid ISBN format. Please try again.")
            continue
        break
    
    while True:
        available = input("Number of available books: ")
        if not re.match(patterns.available_pattern, available):
            print("Invalid number format. Please try again.")
            continue
        available = int(available)
        break

    query = "INSERT INTO library.books (title, author, isbn, available) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (title, author, isbn, available))
    print("Successfully added new book to the library.")



#checking access, selecting operations
def operations(permissions_list):
    while True:
        try:
            print(textwrap.dedent("""\
                Choose operation from your permission level:
                Level 1: listing
                Level 2: listing, modification
                Level 3: listing, modification, deletion
                Level 4: listing, modification, deletion, addition

                1=listing, 2=modification, 3=deletion, 4=addition, 5=quit
            """))
            op_num = int(input("Number of operation: "))
        except ValueError:
            print("Please provide a valid number!")
            continue

        if op_num not in permissions_list:
            print("You dont have permission to perform this operation. Please choose another one!")
            continue
        
        conn, cur = connect()
        if conn and cur:
            try:
                if op_num == 1:
                    listing(cur)
                    searching(cur)   
                elif op_num == 2:
                    modification(cur)
                elif op_num == 3:
                    deletion(cur)
                elif op_num == 4:
                    addition(cur) 
                elif op_num == 5:
                    break  
                else:
                    print("Please choose only from the given numbers!")
                    continue
                conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
            finally:
                cur.close()
                conn.close()
        else:
            print("Unable to connect to database.")
