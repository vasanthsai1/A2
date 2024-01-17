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

# Initialization of keys and nonces
K_AS = get_random_bytes(16) # Pre-shared key between Alice and Server
K_BS = get_random_bytes(16) # Pre-shared key between Bob and Server
K_AB = get_random_bytes(16) # Session key to be used between Alice and Bob

print(f"Pre-shared key between Alice and Server: {K_AS.hex()}")
print(f"Pre-shared key between Bob and Server: {K_BS.hex()}")

# Begin protocol simulation
print("\n=== Needham-Schroeder Protocol Simulation ===\n")

# Alice initiates the protocol
N_A = randint(0, 99999999) # Alice's nonce
print(f"1 (Alice): N_A {N_A}")
print(f"1 (Alice > Server): (A, B, N_A) (Alice, Bob, {N_A})")

# Server generates the session key and prepares the message for Alice
message_for_Alice = f"{N_A},{K_AB.hex()}".encode()
encrypted_message_for_Alice = encrypt(message_for_Alice, K_AS)
print(f"2 (Server): K_AB {K_AB.hex()}")
print(f"2 (Server): E(K_AS) (N_A, K_AB) E({K_AS.hex()}) ({N_A}, {K_AB.hex()}) = {encrypted_message_for_Alice.hex()}")

# Alice decrypts Server's message, gets the session key, and forwards the message to Bob
try:
    decrypted_message_for_Alice = decrypt(encrypted_message_for_Alice, K_AS)
    N_A_received, K_AB_received_hex = decrypted_message_for_Alice.decode().split(',')
    
    if int(N_A_received) != N_A:
        raise ValueError("Nonce does not match. Possible replay attack.")

    print(f"2 (Alice): (N_A, B, K_AB, E(K_BS) (K_AB, A)) = ({N_A_received}, Bob, {K_AB_received_hex}, [encrypted part])")
    print("=> Message 2 authentication was successful!")

# Prepare and encrypt Alice's message to Bob
    message_for_Bob = f"{K_AB_received_hex},Alice".encode()
    encrypted_message_for_Bob = encrypt(message_for_Bob, K_BS)
    print(f"3 (Alice -> Bob): E(K_BS) (K_AB, A) = {encrypted_message_for_Bob.hex()}")
except Exception as e:
    print(f"Authentication failed at Alice's side: {e}")
    exit()

# Bob receives the message, decrypts it with his key with the Server
try:
    decrypted_message_for_Bob = decrypt(encrypted_message_for_Bob, K_BS)
    K_AB_for_Bob_hex, Alice_identifier = decrypted_message_for_Bob.decode().split(',')
    
    if Alice_identifier != "Alice":
        raise ValueError("Authentication failed. Alice identifier not found.")

    print(f"3 (Bob): (K_AB, A) = ({K_AB_for_Bob_hex}, Alice)")
    print("=> Message 3 authentication was successful")

# Bob generates and encrypts his nonce
    N_B = randint(0, 99999999) # Bob's nonce
    encrypted_nonce_for_Alice = encrypt(str(N_B).encode(), bytes.fromhex(K_AB_for_Bob_hex))
    print(f"4 (Bob -> Alice): E(K_AB) (N_B) = {encrypted_nonce_for_Alice.hex()}")

except Exception as e:
    print(f"Authentication failed at Bob's side: {e}")
    exit()
    
# Alice responds to Bob's nonce challenge
try:
    decrypted_nonce_for_Alice = decrypt(encrypted_nonce_for_Alice, bytes.fromhex(K_AB_for_Bob_hex))
    N_B_received = int(decrypted_nonce_for_Alice.decode())
    
    if N_B_received != N_B:
        raise ValueError("Nonce does not match. Possible replay attack.")

    N_B_response = (N_B_received - 1)
    encrypted_response_for_Bob = encrypt(str(N_B_response).encode(), bytes.fromhex(K_AB_for_Bob_hex))
    print(f"5 (Alice -> Bob): E(K_AB) (N_B-1) = {encrypted_response_for_Bob.hex()}")
    
except Exception as e:
    print(f"Authentication failed at Alice's side responding to Bob: {e}")
    exit()
    
#Bob verifies Alice's response
try:
    decrypted_response_for_Bob = decrypt(encrypted_response_for_Bob, bytes.fromhex(K_AB_for_Bob_hex))
    N_B_decremented_received = int(decrypted_response_for_Bob.decode())
    
    if N_B_decremented_received != N_B - 1:
        raise ValueError("Nonce response does not match. Possible replay attack.")

    print(f"5 (Bob): N_B-1 = {N_B_decremented_received}")
    print("=> Message 5 authentication was successful!")
    print(f"The key agreed between Alice and Bob: {K_AB.hex()}")
    
except Exception as e:
    print(f"Authentication failed at Bob's side verifying Alice's response: {e}")
    exit()