import os
import hashlib
import datetime

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Generate a random salt
    salt = os.urandom(16)

    # Hash the password along with the salt
    hashed_password = hashlib.sha256(password.encode('utf-8') + salt).hexdigest()

    # Store the hashed password and salt in a database or file (for simplicity, just print here)
    print(f"User registered: {username}, Hashed Password: {hashed_password}, Salt: {salt.hex()}")
    return hashed_password, salt

def login_user(hashed_password, salt):
    # Simulate getting the current date and time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Encode the salt as a hexadecimal string
    salt_hex = salt.hex()

    # Update the hashed password with the current date and time
    updated_hsp = hashlib.sha256((hashed_password + salt_hex + current_time).encode('utf-8')).hexdigest()

    # Generate an OTP as the last 6 bytes of the updated hashed password
    otp = updated_hsp[-12:-6]

    print(f"OTP generated: {otp}")

    # Simulate the user receiving the OTP via SMS
    user_input = input("Enter the received OTP to log in: ")

    # Check if the user input matches the generated OTP
    if user_input == otp:
        print("Login successful.")
    else:
        print("Login failed. Incorrect OTP.")

if __name__ == "__main__":
    print("User Registration:")
    hashed_password, salt = register_user()

    print("\nUser Login:")
    login_user(hashed_password, salt)
