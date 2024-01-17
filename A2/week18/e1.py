import hmac
import hashlib
import random
import os

def generate_16bit_hmac(key, message):
    hashed = hmac.new(key, message.encode(), hashlib.sha256).digest()
    truncated_hmac = hashed[:2]
    return truncated_hmac

def is_message_authentic(key, message, hmac_to_verify):
    generated_hmac = generate_16bit_hmac(key, message)
    return generated_hmac == hmac_to_verify

def hmac_to_hex(hmac_bytes):
    return hmac_bytes.hex()

# Generate a random 16-byte key for Alice
alice_key = os.urandom(16)

# Original and tampered messages
original_message = "Alice, Bob, £10"
tampered_message = "Alice, Eve, £1000"

# Print the original message
print(f"Original Message: {original_message}")

# Generate HMAC for the original message
original_hmac = generate_16bit_hmac(alice_key, original_message)

# Print the original HMAC in hexadecimal format
print(f"Original HMAC (Hexadecimal): {hmac_to_hex(original_hmac)}")

# Print the tampered message
print(f"Tampered Message: {tampered_message}")

# Check if the server rejects the tampered message with the original HMAC
is_tampered_authentic = is_message_authentic(alice_key, tampered_message, original_hmac)
print(f"Does server reject tampered message? {not is_tampered_authentic}")

# Brute-forcing the HMAC with random amounts
brute_force_attempts = 0
attempted_amounts = set()
max_attempts = 1000000  # Maximum number of brute-force attempts

while brute_force_attempts < max_attempts:
    brute_force_attempts += 1
    # Generate a random amoumnt
    random_amount = random.randint(1, 65536)
    if random_amount not in attempted_amounts:
        attempted_amounts.add(random_amount)
        new_message = f"Alice, Eve, £{random_amount}"
        if is_message_authentic(alice_key, new_message, original_hmac):
            print(f"Matching HMAC found after {brute_force_attempts} attempts")
            break
else:
    print(f"No matching HMAC found after {max_attempts} attempts")
