import random
import hashlib

# User information
user_info = [
    "laplusbelle", "Marie", "Curie", "Woof", "020180", "010280", 
    "UKC", "Jean_Neoskour", "Jvaist_Fairecourir", "Eltrofor", "291281", "122981"
]

# Target hash and saltfc2298f491eac4cff95e7568806e088a901c904cda7dd3221f551e5b89b3c3aa
target_hash = "3281e6de7fa3c6fd6d6c8098347aeb06bd35b0f74b96f173c7b2d28135e14d45"
salt = "5UA@/Mw^%He]SBaU"

# Function to generate a random password and its hash
def generate_password():
    # Randomly select a subset of user information to create a password
    password = ''.join(random.sample(user_info, random.randint(2, 5)))

    # Hashing the password with SHA-256
    hasher = hashlib.sha256()
    hasher.update((password + salt).encode())
    hashed_password = hasher.hexdigest()

    return password, hashed_password

# Function to find a password that matches the target hash
def find_matching_password(target_hash, attempts=100000):  # Reduced attempts for quicker testing
    print("Starting password search...")
    for i in range(attempts):
        password, hashed_password = generate_password()
        if hashed_password == target_hash:
            print(f"Password found on attempt {i+1}: {password}")
            return password
        if i % 1 == 0:
            print(f"At attempt {i+1}, still searching...")

    print("No matching password found within the specified attempts.")
    return None

# Find the matching password
result = find_matching_password(target_hash)
if result:
    print(f"Matching Password: {result}")
else:
    print("No matching password found.")
