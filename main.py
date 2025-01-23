from signup import signup
from login import login
from operations import operations


#main logic of the program
def main():
    while True:
        print("Welcome to the library!")
        is_logged_in = False
        while not is_logged_in:
            choice_1 = input("Do you have a user account? yes/no: ").strip().lower()
            if choice_1 == 'no':
                print("Let's start registration!")
                signup()
            elif choice_1 == 'yes':
                print("Let's log in to your account!")
                is_logged_in, user_name, user_permission = login()
                print(f"Hello {user_name}! You have level {user_permission} permission.")
            else:
                print("Invalid input. Please only choose from 'yes/no'!")
                continue

        while is_logged_in:
            choice_2 = input("Press 'Q' to quit or 'C' to continue: ").strip().lower()
            if choice_2 == 'q':
                is_logged_in = False
                print("Logging out. Goodbye!")
                break
            elif choice_2 == 'c':
                match user_permission:
                    case 1:
                        permissions_list = [1, 5]
                    case 2:
                        permissions_list = [1, 2, 5]
                    case 3:
                        permissions_list = [1, 2, 3, 5]
                    case 4:
                        permissions_list = [1, 2, 3, 4, 5]
                operations(permissions_list)
            else:
                print("Invalid input. Please only choose from 'Q' or 'C'!")


main()



