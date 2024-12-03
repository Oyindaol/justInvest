#!/usr/bin/env python3

from datetime import datetime
import os
import binascii
import hashlib

# Define Available roles
roles = ["Client", "Premium Client", "Financial Planner", "Financial Advisor", "Teller"]


# Define roles and their permissions
ROLES_PERMISSIONS = {
    "Client": ["View account balance", "View investment portfolio", "View Financial Advisor contact info"],
    "Premium Client": ["View account balance", "View investment portfolio", "View Financial Advisor contact info",
                      "Modify investment portfolio", "View Financial Planner contact info"],
    "Financial Advisor": ["View account balance", "View investment portfolio", "Modify investment portfolio",
                         "View private consumer instruments"],
    "Financial Planner": ["View account balance", "View investment portfolio", "Modify investment portfolio",
                         "View private consumer instruments", "View money market instruments"],
    "Teller": ["View account balance"]  # Permissions checked dynamically based on time 
}


# Sample user-role assignments provided for Testing purposes
USER_ROLES = {
    "Sasha Kim": "Client",
    "Emery Blake": "Client",
    "Noor Abbasi": "Premium Client",
    "Zuri Adebayo": "Premium Client",
    "Mikael Chen": "Financial Advisor",
    "Jordan Riley": "Financial Advisor",
    "Ellis Nakamura": "Financial Planner",
    "Harper Diaz": "Financial Planner",
    "Alex Hayes": "Teller",
    "Adair Patel": "Teller"
}


# Function to generate salt   
def generate_salt(length=32):
    salt_bytes = os.urandom(length // 2)
    salt_hex = binascii.hexlify(salt_bytes).decode('utf-8')
    return salt_hex


# Hash the password using the SHA-256 algorithm
def calculate_sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


# Append a new user record to the password file "passwd.txt".
def append_to_file(username, salt, hashedPassword, role):
    with open('passwd.txt', 'a') as file:
        file.write(username + "::")
        file.write(salt + "::")
        file.write(hashedPassword + "::")
        file.write(role + "\n")

    
# Search for a user in the password file ("passwd.txt") by username.
def search_user(username):
    try:
        with open('passwd.txt', 'r') as file:
            for line in file:
                if line.startswith(f"{username}::"):
                    return line.strip()
    except FileNotFoundError:
        return None
    return None


# Checks if inputted password is valid.
def is_valid_password(password):
    # Check password length (8-12 characters required)
    if len(password) < 8 or len(password) > 12:
        return False
    
    # Check for at least one upper-case letter
    if not any(char.isupper() for char in password):
        return False
    
    # Check for at least one lower-case letter
    if not any(char.islower() for char in password):
        return False
    
    # Check for at least one numerical digit
    if not any(char.isdigit() for char in password):
        return False
    
    # Check for at least one special character
    special_characters = {'!', '@', '#', '$', '%', '*', '&'}
    if not any(char in special_characters for char in password):
        return False
    
    # Check for common weak passwords
    common_weak_passwords = ['Password1', 'Qwerty123', 'Qaz123wsx']
    if password in common_weak_passwords:
        return False
    
    return True


# Verify the password for a given username.
def verify_password(username, password):
    username = search_user(username).split("::")
    salt = username[1]
    calculatedHashedPassword = username[2]
    new_password = calculate_sha256(password + salt)
    if new_password != calculatedHashedPassword:
        return "ACCESS DENIED (Incorrect Password)"
    else:
        return "ACCESS GRANTED"


#  Check if the given user has permission to perform a specific action.
def check_permission(user, action):
    role = USER_ROLES.get(user)
    if not role:
        return f"User {user} does not exist."

    # Handle Teller role with time-based restrictions
    if role == "Teller":
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:
            return "ACCESS GRANTED" if action in ROLES_PERMISSIONS[role] else "ACCESS DENIED"
        return "ACCESS DENIED (Outside Business Hours)"

    # Check if action is in role permissions
    if action in ROLES_PERMISSIONS.get(role, []):
        return "ACCESS GRANTED"
    return "ACCESS DENIED"
    

# Register a new user by creating a record in the password file and automatically log them in.
def register():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    while not is_valid_password(password):
        print("Review the following password guides: "
              , "\nPasswords must be least 8-12 characters in length"
              , "\nPassword must include at least: one upper-case letter, one lower-case letter, one numerical digit,"
              , "and one special character from the set: {!, @, #, $, %, ?, ∗}"
              , "\nPasswords found on a list of common weak passwords (e.g., Password1, Qwerty123, or Qaz123wsx) must be prohibited"
              , "\nPasswords matching the format of calendar dates, license plate numbers, telephone numbers, or other common numbers "
              , "must be prohibited")
        password = input("Enter your password: ")

    print("\nAvailable roles (case sensitive!): ", ", ".join(roles))  # Print available roles
    role = input("Enter your role: ")

    while role not in roles:
        print("Role not recognized, possible roles: ", roles)
        role = input("Enter your role again: ")

    # Generate salt and hash the password
    salt = generate_salt()
    hashedPassword = calculate_sha256(password + salt)

    # Append the record to the password file
    append_to_file(username, salt, hashedPassword, role)
    print(f"User {username} registered successfully!")

    # Automatically log the user in
    print(f"User {username} logged in!")
    # Simulate login by passing the username and password directly
    verify_and_login(username, password)


# Helper method to log in a user immediately after successful registration.
def verify_and_login(username, password):
    verification_result = verify_password(username, password)
    if verification_result == "ACCESS GRANTED":
        # Fetch user details from the password file
        user_record = search_user(username)
        if user_record:
            user_details = user_record.split("::")
            role = user_details[3]
            
            # print("\nACCESS GRANTED!")
            print("\n-------------- justInvest System ---------------")
            print("Operations available on the system:")
            print("1. View account balance")
            print("2. View investment portfolio")
            print("3. Modify investment portfolio")
            print("4. View Financial Advisor contact info")
            print("5. View Financial Planner contact info")
            print("6. View money market instruments")
            print("7. View private consumer instruments")
            print("\n")
            print(f"Username: {username}")
            print(f"Role: {role}")

            # Fetch authorized operations
            authorized_operations = []
            permissions = ROLES_PERMISSIONS.get(role, [])

            if role == "Teller":
                # Handle Teller's time-based restrictions
                current_hour = datetime.now().hour
                if 9 <= current_hour <= 17:
                    permissions = ROLES_PERMISSIONS["Teller"]
                else:
                    permissions = []
                    print("Tellers can only access the system between 9:00 AM and 5:00 PM.")

            operation_mapping = {
                "View account balance": 1,
                "View investment portfolio": 2,
                "Modify investment portfolio": 3,
                "View Financial Advisor contact info": 4,
                "View Financial Planner contact info": 5,
                "View money market instruments": 6,
                "View private consumer instruments": 7
            }

            for permission in permissions:
                if permission in operation_mapping:
                    authorized_operations.append(operation_mapping[permission])
            
            print(f"Your authorized operations are: {','.join(map(str, authorized_operations))}")

            # Loop for performing operations
            while True:
                print("\nWhich operation would you like to perform?")
                print("Enter 0 to log out.")
                selected_operation = input("Select an operation: ")

                # Ensure valid input
                if not selected_operation.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                selected_operation = int(selected_operation)

                if selected_operation == 0:
                    print(f"User {username} logged out! Returning to the main menu.")
                    break  # This will exit the loop and return control to the main menu.
                elif selected_operation in authorized_operations:
                    print(f"ACCESS GRANTED! Performing operation {selected_operation}")
                else:
                    print("ACCESS DENIED! Unauthorized operation. Try again!")
        else:
            print("Error: User not found.")
    else:
        print("ACCESS DENIED: Invalid username or password.")


# Log in a user, verify their credentials, and display access privileges.
def login():
    print("\n-------------- justInvest System ---------------")
    print("Operations available on the system:")
    print("1. View account balance")
    print("2. View investment portfolio")
    print("3. Modify investment portfolio")
    print("4. View Financial Advisor contact info")
    print("5. View Financial Planner contact info")
    print("6. View money market instruments")
    print("7. View private consumer instruments")
    print("\n")

    print("\n-------------- User Login ---------------")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    # Verify the user's credentials
    verification_result = verify_password(username, password)
    if verification_result == "ACCESS GRANTED":
        # Fetch user details from the password file
        user_record = search_user(username)
        if user_record:
            user_details = user_record.split("::")
            role = user_details[3]
            
            print("\nACCESS GRANTED!")
            print(f"Username: {username}")
            print(f"Role: {role}")

            # Fetch authorized operations
            authorized_operations = []
            permissions = ROLES_PERMISSIONS.get(role, [])

            if role == "Teller":
                # Handle Teller's time-based restrictions
                current_hour = datetime.now().hour
                if 9 <= current_hour <= 17:
                    permissions = ROLES_PERMISSIONS["Teller"]
                else:
                    permissions = []
                    print("Tellers can only access the system between 9:00 AM and 5:00 PM.")

            operation_mapping = {
                "View account balance": 1,
                "View investment portfolio": 2,
                "Modify investment portfolio": 3,
                "View Financial Advisor contact info": 4,
                "View Financial Planner contact info": 5,
                "View money market instruments": 6,
                "View private consumer instruments": 7
            }

            for permission in permissions:
                if permission in operation_mapping:
                    authorized_operations.append(operation_mapping[permission])
            
            print(f"Your authorized operations are: {','.join(map(str, authorized_operations))}")

            # Loop for performing operations
            while True:
                print("\nWhich operation would you like to perform?")
                print("Enter 0 to log out.")
                selected_operation = input("Select an operation: ")

                # Ensure valid input
                if not selected_operation.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                selected_operation = int(selected_operation)

                if selected_operation == 0:
                    print(f"User {username} logged out! Returning to the main menu.")
                    break  # This will exit the loop and return control to the main menu.
                elif selected_operation in authorized_operations:
                    print(f"ACCESS GRANTED! Performing operation {selected_operation}")
                else:
                    print("ACCESS DENIED! Unauthorized operation. Try again!")
        else:
            print("Error: User not found.")
    else:
        print("ACCESS DENIED: Invalid username or password.")
    



if __name__ == "__main__":
    while True:
        print("\n-------------- justInvest System ---------------")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting the justInvest System!")
            break
        else:
            print("Invalid choice. Please try again!")

    