import hashlib
from itertools import permutations

def generate_unlock_patterns():
    # Generate all permutations of the letters a-i
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    patterns = [''.join(p) for p in permutations(letters)]
    return patterns

def hash_pattern(pattern):
    # Hash the pattern directly using SHA-1
    hashed_pattern = hashlib.sha1(pattern.encode()).hexdigest()
    return hashed_pattern

def recover_unlock_pattern(target_hash):
    # Generate all possible unlock patterns
    all_patterns = generate_unlock_patterns()

    # Iterate through patterns and check for a match
    for pattern in all_patterns:
        hashed_pattern = hash_pattern(pattern)
        if hashed_pattern == target_hash:
            return True, pattern

    return False, None

# Example usage:
if __name__ == "__main__":
    # Recorded hash value from the rooted mobile phone
    target_hash = '91077079768edba10ac0c93b7108bc639d778d67'

    # Attempt to recover the unlock pattern
    success, recovered_pattern = recover_unlock_pattern(target_hash)

    if success:
        print(f"Unlock pattern recovered: {recovered_pattern}")
    else:
        print("Unlock pattern not found.")
