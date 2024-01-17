import hashlib
import secrets

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt, iterations=2):
    password_salt = password + salt
    hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()

    for _ in range(iterations - 1):
        hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

    return hashed_password

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    profile_info = input("Enter your profile information: ")

    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    user_data = {
        'username': username,
        'salt': salt,
        'hashed_password': hashed_password,
        'profile_info': profile_info
    }

    print(f"User {username} registered successfully!")

    return user_data

def login_user(user_data):
    entered_username = input("Enter your username: ")
    entered_password = input("Enter your password: ")

    stored_username = user_data['username']
    stored_salt = user_data['salt']
    stored_hashed_password = user_data['hashed_password']

    hashed_password_attempt = hash_password(entered_password, stored_salt)

    if entered_username == stored_username and hashed_password_attempt == stored_hashed_password:
        print(f"Login successful! Welcome, {entered_username}.")
    elif entered_username != stored_username:
        print("Login failed. Incorrect username.")
    else:
        print("Login failed. Incorrect password.")

# Register user
user_data = register_user()

# Attempt to log in with the correct username and password
login_user(user_data)

# Attempt to log in with an incorrect username and password
login_user(user_data)
hasattr