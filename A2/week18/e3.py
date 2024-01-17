import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Random.random import randint

# Utility functions for encryption and decryption
def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message, AES.block_size))
    return cipher.iv + ct_bytes

def decrypt(ciphertext, key):
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

# Generate keys as in e2
K_BS = get_random_bytes(16)  # Pre-shared key between Bob and Server

# For the attack simulation, we assume Eve has already obtained the following from a previous session:
K_AB = get_random_bytes(16)  # Pre-recorded session key between Alice and Bob
message_for_Bob = f"{K_AB.hex()},Alice".encode()  # Message 3 that Alice would send to Bob
message_3_encrypted = encrypt(message_for_Bob, K_BS)  # Message 3 encrypted with K_BS

print("Unknown to Eve:")
print("Pre-shared key between Alice and Server: [does not matter / Unused in the attack]")
print(f"Pre-shared key between Bob and Server: {K_BS.hex()}")

print("Known to Eve (Collected from a previous session between Alice and Bob):")
print(f"Pre-recorded K_AB: {K_AB.hex()}")
print(f"Pre-recorded Message 3 (Alice => Bob): {message_3_encrypted.hex()}")

#Eve replays Message 3 to Bob, impersonating Alice

print("\n3 (Eve => Bob): E_{K_BS} (K_AB, A) = " + message_3_encrypted.hex())

#Bob receives the message, decrypts it with his key with the Server
#Since this is a replay, we are simulating Bob's expected behavior

try:
    decrypted_message_for_Bob = decrypt(message_3_encrypted, K_BS)
    K_AB_for_Bob_hex, Alice_identifier = decrypted_message_for_Bob.decode().split(',')

    if Alice_identifier != "Alice":
        raise ValueError("Authentication failed. Alice identifier not found.")

    print(f"3 (Bob): (K_AB, A) = ({K_AB_for_Bob_hex}, Alice)")
    print("Eve successfully passed message 3 authentication!")

# Bob generates and encrypts his nonce, thinking he is communicating with Alice
    N_B = randint(0, 99999999)  # Bob's nonce
    encrypted_nonce_for_Alice = encrypt(str(N_B).encode(), K_AB)
    print(f"4 (Bob): N_B = {N_B}")
    print(f"4 (Bob => Eve): E_{K_AB.hex()} (N_B) = {encrypted_nonce_for_Alice.hex()}")

# Eve decrypts Bob's nonce
    decrypted_nonce_for_Alice = decrypt(encrypted_nonce_for_Alice, K_AB)
    N_B_received = int(decrypted_nonce_for_Alice.decode())
    print(f"4 (Eve): N_B = {N_B_received}")
    print("Eve successfully decrypted Message 4 to get N_B!")

# Eve responds to Bob's nonce challenge by decrementing it
    N_B_response = (N_B_received - 1)
    encrypted_response_for_Bob = encrypt(str(N_B_response).encode(), K_AB)
    print(f"5 (Eve => Bob): E_{K_AB.hex()} (N_B-1) = {encrypted_response_for_Bob.hex()}")

# Bob receives the decremented nonce from Eve, thinking it is from Alice
    decrypted_response_for_Bob = decrypt(encrypted_response_for_Bob, K_AB)
    N_B_decremented_received = int(decrypted_response_for_Bob.decode())

    if N_B_decremented_received != N_B - 1:
        raise ValueError("Nonce response does not match. Possible replay attack.")

    print(f"5 (Bob): N_B-1 = {N_B_decremented_received}")
    print("Eve successfully passed Message 5 authentication!\n")


    print("Eve successfully launched a replay attack to reuse a previously recorded session key agreed between Alice and Bob.")

except Exception as e:
    print(f"An error occurred: {e}")



