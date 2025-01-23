import bcrypt
from db_handler import connect


#checking the username and password in the database
def authentication(cur, username, password):
    try:
        query = "SELECT * FROM library.customers WHERE username = %s"
        cur.execute(query, (username,))
        user_data = cur.fetchone()

        if user_data:
            stored_password = user_data[6]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, user_data
            else:
                return False, None
        else:
            return False, None
    except Exception as e:
        print(f"Error: {e}")
        return False, None

#login logic    
def login():
    conn, cur = connect()
    if conn and cur:
        try:
            while True:
                username = input("Username: ")
                password = input("Password: ")
                is_valid, user_data = authentication(cur, username, password)

                if is_valid:
                    print("Successful login.")
                    return True, user_data[1], user_data[7]
                else:
                    print("Invalid username or password. Try again!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Unable to connect to database.")

 


        



    

