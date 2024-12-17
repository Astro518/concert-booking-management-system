import os
import uuid
import datetime

# Class to represent a User
class User:
    def __init__(self, role, username):
        self.role = role
        self.username = username

# Function to read users from file and authenticate
def authenticate(role, username, password):
    with open("users.txt", "r") as file:
        for line in file:
            user_info = line.strip().split(",")
            if user_info[0] == role and user_info[1] == username and user_info[2] == password:
                return User(role, username)
    return None

# Function to create a new user
def create_new_user():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    with open("users.txt", "a") as file:
        file.write(f"\nuser,{username},{password}")

    print("New user created successfully!")

# Function to display available tickets with pricing
def display_available_tickets():
    with open("tickets.txt", "r") as file:
        for line in file:
            ticket_type, quantity, price = line.strip().split(":")
            print(f"{ticket_type.capitalize()}: {quantity} available - Price: ${price} each")

# Function to book tickets
def book_tickets(user):
    ticket_type = input("Enter ticket type (e.g., VIP, Regular): ").strip().capitalize()
    num_tickets = int(input("Enter the number of tickets to book: "))

    with open("tickets.txt", "r+") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if ticket_type in line:
                available_tickets, price = map(int, line.split(":")[1:])
                if num_tickets <= available_tickets:
                    total_cost = num_tickets * price
                    lines[i] = f"{ticket_type.capitalize()}: {available_tickets - num_tickets}:{price}\n"
                    print(f"{num_tickets} {ticket_type.capitalize()} tickets booked successfully!")
                    print(f"Total Cost: ${total_cost}")
                    booking_id = str(uuid.uuid4())[:8]
                    log_booking(user, ticket_type, num_tickets, total_cost, booking_id)
                    break
                else:
                    print("Not enough tickets available.")
                    return
        else:
            print("Invalid ticket type.")
            return

    with open("tickets.txt", "w") as file:
        file.writelines(lines)

# Function to log booking details
def log_booking(user, ticket_type, num_tickets, total_cost, booking_id):
    with open("booking_log.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - Role: {user.role}, User: {user.username}, Booking ID: {booking_id}, "
                   f"Ticket Type: {ticket_type}, Quantity: {num_tickets}, Total Cost: ${total_cost}\n")

# Function to cancel booking
def cancel_booking():
    booking_id = input("Enter booking ID to cancel: ").strip()
    # Add cancellation logic here
    print("Booking cancelled successfully!")

# Function to reset user details by admin
def reset_user_details():
    print("Resetting user details...")
    with open("users.txt", "w") as file:
        file.write("admin,admin,admin\nuser,user,user")
    print("User details reset successfully!")

# Function to reset ticket details by admin
def reset_tickets():
    print("Resetting ticket details...")
    with open("tickets.txt", "w") as file:
        file.write("VIP:100:100\nRegular:200:50")
    print("Ticket details reset successfully!")

# Function to check tickets by each user
def check_tickets_by_user():
    users_tickets = {}
    with open("booking_log.txt", "r") as file:
        for line in file:
            parts = line.strip().split(", ")
            role = parts[0].split(": ")[1]
            username = parts[1].split(": ")[1]
            ticket_type = parts[3].split(": ")[1]
            quantity = int(parts[4].split(": ")[1])
            if username in users_tickets:
                if ticket_type in users_tickets[username]:
                    users_tickets[username][ticket_type] += quantity
                else:
                    users_tickets[username][ticket_type] = quantity
            else:
                users_tickets[username] = {ticket_type: quantity}

    print("Tickets booked by each user:")
    for username, tickets in users_tickets.items():
        print(f"{username}:")
        for ticket_type, quantity in tickets.items():
            print(f"- {quantity} {ticket_type.capitalize()} tickets")

# Main function
def main():
    if not os.path.exists("tickets.txt"):
        with open("tickets.txt", "w") as file:
            file.write("VIP:100:100\nRegular:200:50")

    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as file:
            file.write("admin,admin,admin\nuser,user,user")

    print("Welcome to the Ticket Booking System!")
    while True:
        print("1. Existing user")
        print("2. New user")
        choice = input("Choose option: ").strip()

        if choice == "1":
            role = input("Enter your role (admin/user): ").strip().lower()
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            user = authenticate(role, username, password)
            if user:
                print("Authentication successful!\n")
                break
            else:
                print("Invalid role, username, password combination. Please try again.\n")

        elif choice == "2":
            create_new_user()
        else:
            print("Invalid choice. Please try again.\n")

    while True:
        print("\n1. Display available tickets")
        print("2. Book tickets")
        print("3. Cancel booking")
        if user.role == "admin":
            print("4. Reset user details")
            print("5. Reset ticket details")
            print("6. Check tickets by user")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_available_tickets()
        elif choice == "2":
            book_tickets(user)
        elif choice == "3":
            cancel_booking()
        elif choice == "4" and user.role == "admin":
            reset_user_details()
        elif choice == "5" and user.role == "admin":
            reset_tickets()
        elif choice == "6" and user.role == "admin":
            check_tickets_by_user()
        elif choice == "7":
            print("Exiting program. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
