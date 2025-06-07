def number_to_binary():
    try:
        num = int(input("Enter a number: "))
        print(f"Binary representation: {bin(num)[2:]}")
    except ValueError:
        print("Please enter a valid integer.")

def binary_to_number():
    binary = input("Enter binary code: ")
    try:
        num = int(binary, 2)
        print(f"Decimal number: {num}")
    except ValueError:
        print("Please enter valid binary code (only 0s and 1s).")

def main():
    while True:
        print("\nMenu:")
        print("1. Number to binary")
        print("2. Binary to number")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            number_to_binary()
        elif choice == '2':
            binary_to_number()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
