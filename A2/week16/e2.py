import hashlib
import requests

# Target hash and rounds
target_hash = "3ddcd95d2bff8e97d3ad817f718ae207b98c7f2c84c5519f89cd15d7f8ee1c3b"
max_rounds = 10  # You can adjust this based on your experimentation

# Download phpbb leaked password database
url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/phpbb.txt"
response = requests.get(url)
passwords = response.text.splitlines()

# Dictionary attack function
def dictionary_attack(password, target_hash, max_rounds):
    for round_count in range(1, max_rounds + 1):
        # Hash the password with the chosen hash function and rounds
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for _ in range(round_count - 1):
            hashed_password = hashlib.sha256(hashed_password.encode()).hexdigest()

        # Check for a match
        if hashed_password == target_hash:
            return True, password, round_count

    return False, None, None

# Perform the dictionary attack
for password in passwords:
    success, cracked_password, rounds_used = dictionary_attack(password, target_hash, max_rounds)
    if success:
        print(f"Password cracked: {cracked_password} (Rounds: {rounds_used})")
        break
else:
    print("Password not found in the phpbb dictionary.")
