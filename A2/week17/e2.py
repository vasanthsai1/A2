import os
import hashlib
import getpass

def register_user():
    username = input("Enter your username: ")
    password_file_path = input("Enter the path to your password file: ")

    if not os.path.exists(password_file_path):
        print("File does not exist. Please provide a valid file path.")
        return None, None

    # Read the contents of the password file
    with open(password_file_path, 'rb') as file:
        password = file.read()

    # Hash the password
    hashed_password = hashlib.sha256(password).hexdigest()

    # Store the username and hashed password in a database or file (for simplicity, just print here)
    print(f"User registered: {username}, Password: {password.decode('utf-8')}, Hashed Password: {hashed_password}")
    return username, hashed_password

def login_user(registered_username, registered_password):
    username = input("Enter your username: ")

    # Check if the entered username matches the registered username
    if username == registered_username:
        password_file_path = input("Enter the path to your password file: ")

        if not os.path.exists(password_file_path):
            print("File does not exist. Please provide a valid file path.")
            return

        # Read the contents of the password file
        with open(password_file_path, 'rb') as file:
            entered_password = file.read()

        # Hash the entered password for comparison
        entered_password_hash = hashlib.sha256(entered_password).hexdigest()

        # Compare the entered password hash with the stored password hash
        if entered_password_hash == registered_password:
            print("Login successful.")
        else:
            print("Login failed. Incorrect password.")
    else:
        print("Login failed. Username not found.")

if __name__ == "__main__":
    print("User Registration:")
    registered_username, registered_password = register_user()

    # Check if registration was successful before proceeding to login
    if registered_username is not None and registered_password is not None:
        print("\nUser Login:")
        login_user(registered_username, registered_password)
