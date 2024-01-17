# Ensure your terminal or environment supports UTF-8 encoding

def main():
    try:
        # Prompt for password input
        password = input("Enter your password (emojis are allowed): ")

        # Print the entered password
        print(f"Your entered password is: {password}")

    except UnicodeDecodeError:
        print("Error: Unicode encoding not supported in your terminal.")

if __name__ == "__main__":
    main()
