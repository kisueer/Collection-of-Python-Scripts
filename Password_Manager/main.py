import random
import string
import json
import os

# Function to generate a random password with letters and numbers only
def generate_password(length=12):
    if length <= 0:
        raise ValueError("Password length must be a positive integer.")
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to save passwords to a JSON file
def save_passwords(passwords, file_name):
    with open(file_name, 'w') as file:
        json.dump(passwords, file, indent=4)

# Function to load passwords from a JSON file
def load_passwords(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
        return {}

# Function to add a new password entry
def add_password(passwords, app_name, username, password):
    if not app_name or not username:
        print("Error: Application name and username cannot be empty.")
        return
    passwords[app_name] = {'username': username, 'password': password}

# Function to retrieve a password for a given app
def get_password(passwords, app_name):
    if app_name in passwords:
        return passwords[app_name]['username'], passwords[app_name]['password']
    else:
        return None, None

# Function to clear the console screen based on the operating system
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function to manage password manager operations
def main():
    passwords = load_passwords('passwords.json')

    while True:
        clear_screen()  # Clear screen before displaying menu
        print("Password Manager Menu:")
        print("1. Generate a new password")
        print("2. Add a new password entry")
        print("3. Retrieve a password")
        print("4. Save passwords to passwords.json")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            try:
                length = int(input("Enter the length of the password to generate: "))
                new_password = generate_password(length)
                print(f"Generated Password: {new_password}")

                add_to_list = input("Do you want to add this password to the password list? (yes/no): ").strip().lower()
                if add_to_list == 'yes':
                    app_name = input("Enter the application name: ")
                    username = input("Enter the username/email: ")
                    add_password(passwords, app_name, username, new_password)
                    save_passwords(passwords, 'passwords.json')
                    print(f"Password saved for {app_name}")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == '2':
            app_name = input("Enter the application name: ")
            username = input("Enter the username/email: ")
            new_password = input("Enter the password (or leave blank to generate one): ")

            if not new_password:
                new_password = generate_password()
                print(f"Generated Password: {new_password}")

            add_password(passwords, app_name, username, new_password)
            save_passwords(passwords, 'passwords.json')
            print(f"Password saved for {app_name}")

        elif choice == '3':
            app_name = input("Enter the application name to retrieve password: ")
            username, password = get_password(passwords, app_name)
            if password:
                print(f"Application: {app_name}")
                print(f"Username/Email: {username}")
                print(f"Password: {password}")
            else:
                print(f"No password found for {app_name}")

        elif choice == '4':
            save_passwords(passwords, 'passwords.json')
            print("Passwords saved to passwords.json")

        elif choice == '5':
            print("Exiting Password Manager.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

        input("Press Enter to continue...")  # Wait for user to press Enter before clearing screen

if __name__ == '__main__':
    main()
