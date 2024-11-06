from termcolor import colored

class MembershipClub:
    
    def __init__(self):
        self.members = {
            "user1": {"password": "password1", "role": "member", "payment_status": "unpaid"},
            "user2": {"password": "password2", "role": "coach", "payment_status": "paid"},
            "user3": {"password": "password3", "role": "treasurer", "payment_status": "unpaid"}
        }
        self.messages = []
        self.practice_schedule = []
    
    def register(self, username, password, confirm_password, name=None, phone_number=None, address=None, role="member", payment_status="unpaid", coach_fees=None):
        if username in self.members:
            print(colored("Username already exists. Please choose a different one.", "red", attrs=["bold"]))
        elif password != confirm_password:
            print(colored("Password confirmation does not match. Please try again.", "red", attrs=["bold"]))
        else:
            if role == "member":
                if not (name and phone_number and address):
                    print(colored("Please provide all required information (name, phone number, address) for member registration.", "red", attrs=["bold"]))
                    return
            self.members[username] = {
                "password": password,
                "name": name,
                "phone_number": phone_number,
                "address": address,
                "role": role,
                "payment_status": payment_status,
                "payments": [],
                "coach_fees": coach_fees
            }
            print(colored("Registration successful!", "green", attrs=["bold"]))

    def login(self, username, password):
        if username in self.members and self.members[username]["password"] == password:
            print(colored("Login successful!", "green", attrs=["bold"]))
            return True
        else:
            print(colored("Invalid username or password.", "red", attrs=["bold"]))
            return False
    

    def send_message(self, sender, receiver, message):
        self.messages.append({"sender": sender, "receiver": receiver, "message": message})
        print("Message sent successfully!")

    def add_coach(self, coach_username):
        if coach_username in self.members:
            if self.members[coach_username]["role"] != "coach":
                self.members[coach_username]["role"] = "coach"
                print(f"{coach_username} added as coach.")
                self.send_message("treasurer", coach_username, "You have been added as a coach.")
            else:
                print(f"{coach_username} is already a coach.")
        else:
            self.members[coach_username] = {"password": "default_password", "role": "coach", "payment_status": "paid"}
            print(f"{coach_username} added as coach.")
            self.send_message("treasurer", coach_username, "You have been added as a coach.")

    def remove_coach(self, coach_username):
        if coach_username in self.members and self.members[coach_username]["role"] == "coach":
            self.members[coach_username]["role"] = "member"
            print(f"{coach_username} removed as coach.")
        else:
            print(f"{coach_username} is not a coach.")

    def add_member(self, member_username):
        if member_username in self.members:
            if self.members[member_username]["role"] != "coach":
                 self.members[member_username]["role"] = "member"
                 print(f"{member_username} added as member.")
                 self.send_message("coach", member_username, "You have been added as a member.")
            else:
                print(f"{member_username} is already a member.")
        else:
            self.members[member_username] = {"password": "default_password", "role": "member", "payment_status": "paid"}
            print(f"{member_username} added as member.")
            self.send_message("coach", member_username, "You have been added as a member.")

    def remove_member(self, member_username):
        if member_username in self.members and self.members[member_username]["role"] == "member":
            del self.members[member_username]
            print(f"{member_username} removed as member.")
        else:
            print(f"{member_username} is not a member.")

    def schedule_practice(self, coach_username, practice_details):
        if coach_username in self.members and self.members[coach_username]["role"] == "coach":
            self.practice_schedule.append({"coach": coach_username, "details": practice_details})
            print("Practice scheduled successfully!")
            self.notify_treasurer_and_coach(coach_username, practice_details)
        else:
            print(f"{coach_username} is not a coach.")

    def make_payment(self, username, amount):
        if username in self.members and self.members[username]["role"] == "member":
            discount_or_charge = self.calculate_discount_or_charge(username)
            if discount_or_charge != 0:
                print(f"Applying discount or charge of ${discount_or_charge}.")
                amount += discount_or_charge
            self.members[username]["payment_status"] = "paid"
            self.members[username]["payments"].append(amount)  
            print(f"Payment of ${amount} received from {username}.")
            self.notify_treasurer_and_coach(username, f"Payment of ${amount} received.")
            self.check_discount_eligibility(username)
        else:
            print(f"{username} is not a member.")

    def notify_treasurer_and_coach(self, username, message):
        for member in self.members:
            if self.members[member]["role"] in ["treasurer", "coach"]:
                self.send_message(username, member, message)
    def check_discount_eligibility(self, username):
        if len(self.members[username]["payments"]) >= 3:
            # Check if the member has not skipped payment for 3 months
            if all(payment > 0 for payment in self.members[username]["payments"][-3:]):
                print(f"{username} is eligible for a 10% discount on the next class.")
                self.send_message("club", username, "Congratulations! You are eligible for a 10% discount on the next class.")

    def calculate_discount_or_charge(self, username):
        payments = self.members[username]["payments"]
        unpaid_count = sum(1 for payment in payments if payment <= 0)
        if unpaid_count == 0:
            return 0  # No discount or charge if all payments are made
        elif unpaid_count == 1:
            return -self.PENALTY_FEE  # Apply penalty fee for one missed payment
        else:
            return self.PENALTY_FEE * (unpaid_count - 1)  # Apply additional penalty fee for repeated non-payments

    def send_payment_reminder(self, treasurer_username, member_username):
        if treasurer_username in self.members and self.members[treasurer_username]["role"] == "treasurer":
            if self.members[member_username]["payment_status"] == "unpaid":
                message = "Reminder: You have an unpaid membership fee. Please submit your payment."
                self.messages.append({"sender": treasurer_username, "receiver": member_username, "message": message})
                return f"Payment reminder sent to {member_username}."
            else:
                return f"{member_username} has already paid."
        else:
            return "Only treasurers can send payment reminders."

    def send_payment_reminders(self, treasurer_username):
        if treasurer_username in self.members and self.members[treasurer_username]["role"] == "treasurer":
            unpaid_members = [username for username, info in self.members.items() if info["role"] == "member" and info["payment_status"] == "unpaid"]
            if unpaid_members:
                print("Sending payment reminders to unpaid members:")
                for member_username in unpaid_members:
                    print(self.send_payment_reminder(treasurer_username, member_username))
            else:
                print("All members have paid their fees.")
        else:
            print("Only treasurers can send payment reminders.")
    
    def pay_coach_fees(self, treasurer_username, coach_username, amount):
        if treasurer_username in self.members and self.members[treasurer_username]["role"] == "treasurer":
            if coach_username in self.members and self.members[coach_username]["role"] == "coach":
                if self.members[coach_username]["payment_status"] == "unpaid":
                    self.members[coach_username]["payment_status"] = "paid"
                    self.members[coach_username]["payments"].append(amount)
                    print(f"Coach fees of ${amount} paid successfully for {coach_username}.")
                    self.send_message(treasurer_username, coach_username, f"Coach fees of ${amount} paid.")
                    return
                else:
                    print(f"{coach_username} has already paid coach fees.")
            else:
                print(f"{coach_username} is not a coach.")
        else:
            print("Only treasurers can pay coach fees.")
    
    def pay_hall_rent(self, treasurer_username, amount):
        if treasurer_username in self.members and self.members[treasurer_username]["role"] == "treasurer":
            # Here you would add the logic to pay the hall rent.
            # This might involve recording the payment, updating payment status, etc.
            print(f"Hall rent of ${amount} paid successfully.")
            self.send_message("club", "treasurer", f"Hall rent of ${amount} paid successfully.")
        else:
            print("Only treasurers can pay hall rent.")
    
    
    def count_unpaid_coaches_expense(club):
        unpaid_coaches = []
        for username, info in club.members.items():
            if info["role"] == "coach" and info["payment_status"] == "unpaid":
                unpaid_coaches.append((username, info["coach_fees"]))
        return unpaid_coaches

    
    def calculate_income_statement(self, x, y):
        profit_loss = x - y
        if profit_loss >= 0:
            status = "Profit"
        else:
            status = "Loss"
        return {
            "Total Revenue": x,
            "Total Expenses": y,
            "Profit/Loss": profit_loss,
            "Status": status
        }

    
    def get_messages(self, username):
        user_messages = []
        for message in self.messages:
            if message["receiver"] == username:
                sender = message["sender"]
                content = message["message"]
                user_messages.append((sender, content))
        return user_messages

    def view_messages(self, username):
        user_messages = self.get_messages(username)
        if user_messages:
            print(f"Messages for {username}:")
            for sender, content in user_messages:
                print(f"From: {sender}\nMessage: {content}")
        else:
            print(f"No messages for {username}.")



    
total_revenue=[]
total_expenses=[]

def treasurer_ui(club, treasurer_username):
    print(colored(f"Welcome, {treasurer_username}, to the Treasurer Interface!", "green", attrs=["bold"]))
    while True:
        print(colored("\nTreasurer Options:", "green", attrs=["bold"]))
        print(colored("1. Add Coach", "white", attrs=["bold"]))
        print(colored("2. Remove Coach", "white", attrs=["bold"]))
        print(colored("3. Send Payment Reminders", "white", attrs=["bold"]))
        print(colored("4. Pay Coach Fees", "white", attrs=["bold"]))
        print(colored("5. Pay Hall Rent", "white", attrs=["bold"]))
        print(colored("6. View Income Statement", "white", attrs=["bold"]))
        print(colored("7. View unpaid coaches expense", "white", attrs=["bold"]))
        print(colored("8. View Messages", "white", attrs=["bold"]))
        print(colored("9. Logout", "white", attrs=["bold"]))
        choice = input(colored("Enter your choice: ", "yellow", attrs=["bold"]))
        if choice == "1":
            coach_username = input(colored("Enter the username of the coach to add: ", "yellow", attrs=["bold"]))
            coach_charge = input(colored("Enter the fees charged by the coach:", "yellow", attrs=["bold"]))
            club.add_coach(coach_username)
        elif choice == "2":
            print(colored("\nList of Coaches:", "green", attrs=["bold"]))
            for member, info in club.members.items():
                if info["role"] == "coach":
                    print(colored(member, "white", attrs=["bold"]))
            coach_username = input(colored("Enter the username of the coach to remove: ", "yellow", attrs=["bold"]))
            club.remove_coach(coach_username)
        elif choice == "3":
            club.send_payment_reminders(treasurer_username)
        elif choice == "4":
            coach_username = input(colored("Enter the username of the coach to pay fees: ", "yellow", attrs=["bold"]))
            amount = float(input(colored("Enter the amount to pay: $", "yellow", attrs=["bold"])))
            club.pay_coach_fees(treasurer_username, coach_username, amount)
        elif choice == "5":
            amount = float(input(colored("Enter the amount of hall rent to pay: $", "yellow", attrs=["bold"])))
            club.pay_hall_rent(treasurer_username, amount)
        elif choice == "6":
            income_statement = club.calculate_income_statement(sum(total_revenue), sum(total_expenses))
            print(colored("\nIncome Statement:", "green", attrs=["bold"]))
            for item, value in income_statement.items():
                print(colored(f"{item}: ${value}", "white", attrs=["bold"]))
        elif choice == "7":
            unpaid_coaches = club.count_unpaid_coaches_expense()
            print(colored("\nUnpaid Coaches and Their Fees:", "green", attrs=["bold"]))
            for coach, fees in unpaid_coaches:
                print(colored(f"Coach: {coach}, Fees: ${fees}", "white", attrs=["bold"]))
        elif choice == "8":
            club.view_messages(treasurer_username)
        elif choice == "9":
            print(colored("Logging out from Treasurer Interface...", "green", attrs=["bold"]))
            break
        else:
            print(colored("Invalid choice. Please try again.", "red", attrs=["bold"]))

def member_ui(club, username):
    print(colored(f"Welcome {username} to the Member Interface!", "green", attrs=["bold"]))
    while True:
        print(colored("\nMember Options:", "green", attrs=["bold"]))
        print(colored("1. Schedule Practice", "white", attrs=["bold"]))
        print(colored("2. Make Payment", "white", attrs=["bold"]))
        print(colored("3. View Messages", "white", attrs=["bold"]))
        print(colored("4. Logout", "white", attrs=["bold"]))
        choice = input(colored("Enter your choice: ", "yellow", attrs=["bold"]))
        if choice == "1":
            print(colored("\nList of Coaches:", "green", attrs=["bold"]))
            for member, info in club.members.items():
                if info["role"] == "coach":
                    print(colored(member, "white", attrs=["bold"]))
            coach_name = input(colored("Enter the username of the coach you want to book the services for: ", "yellow", attrs=["bold"]))
            practice_details = input(colored("Enter practice details: ", "yellow", attrs=["bold"]))
            club.schedule_practice(coach_name, practice_details)
        elif choice == "2":
            amount = float(input(colored("Enter the membership payment amount per month: $", "yellow", attrs=["bold"])))
            club.make_payment(username, amount)
        elif choice == "3":
            club.view_messages(username)
        elif choice == "4":
            print(colored("Logging out from Member Interface...", "green", attrs=["bold"]))
            break
        else:
            print(colored("Invalid choice. Please try again.", "red", attrs=["bold"]))

def coach_ui(club, username):
    print(colored(f"Welcome {username} to the Coach Interface!", "green", attrs=["bold"]))
    while True:
        print(colored("\nCoach Options:", "green", attrs=["bold"]))
        print(colored("1. Add Member", "white", attrs=["bold"]))
        print(colored("2. Remove Member", "white", attrs=["bold"]))
        print(colored("3. Send practice message to all members", "white", attrs=["bold"]))
        print(colored("4. Send reminder to unpaid members", "white", attrs=["bold"]))
        print(colored("5. View Messages", "white", attrs=["bold"]))
        print(colored("6. Logout", "white", attrs=["bold"]))
        choice = input(colored("Enter your choice: ", "yellow", attrs=["bold"]))
        if choice == "1":
            member_username = input(colored("Enter the username of the member to add: ", "yellow", attrs=["bold"]))
            club.add_member(member_username)
        elif choice == "2":
            print(colored("\nList of Members:", "green", attrs=["bold"]))
            for member, info in club.members.items():
                if info["role"] == "member":
                    print(colored(member, "white", attrs=["bold"]))
            member_username = input(colored("Enter the username of the member to remove: ", "yellow", attrs=["bold"]))
            club.remove_member(member_username)
        elif choice == "3":
            message = input(colored("Enter the practice details: ", "yellow", attrs=["bold"]))
            for member in club.members:
                if club.members[member]["role"] == "member":
                    club.send_message(username, member, message)
            print(colored("Practice message sent to all members.", "green", attrs=["bold"]))
        elif choice == "4":
            for member in club.members:
                if club.members[member]["role"] == "member" and club.members[member]["payment_status"] == "unpaid":
                    message = "Reminder: You have an unpaid membership fee. Please submit your fee"
                    club.send_message(username, member, message)
            print(colored("Reminder sent to unpaid members.", "green", attrs=["bold"]))
        elif choice == "5":
            club.view_messages(username)
        elif choice == "6":
            print(colored("Logging out from Coach Interface...", "green", attrs=["bold"]))
            break
        else:
            print(colored("Invalid choice. Please try again.", "red", attrs=["bold"]))

def main():
    club = MembershipClub()
    while True:
        print(colored("\nWelcome to the Membership Club!", "green", attrs=["bold"]))
        print(colored("1. Register as Member", "white", attrs=["bold"]))
        print(colored("2. Register as Coach", "white", attrs=["bold"]))
        print(colored("3. Register as Treasurer", "white", attrs=["bold"]))
        print(colored("4. Login", "white", attrs=["bold"]))
        print(colored("5. Exit", "white", attrs=["bold"]))
        choice = input(colored("Enter your choice: ", "yellow", attrs=["bold"]))
        if choice == "1":
            print(colored("\nMember Registration:", "green", attrs=["bold"]))
            username = input(colored("Enter a username: ", "yellow", attrs=["bold"]))
            password = input(colored("Enter a password: ", "yellow", attrs=["bold"]))
            confirm_password = input(colored("Confirm your password: ", "yellow", attrs=["bold"]))
            name = input(colored("Enter your name: ", "yellow", attrs=["bold"]))
            phone_number = input(colored("Enter your phone number: ", "yellow", attrs=["bold"]))
            address = input(colored("Enter your address: ", "yellow", attrs=["bold"]))
            club.register(username, password, confirm_password, name, phone_number, address)
        elif choice == "2":
            print(colored("\nCoach Registration:", "green", attrs=["bold"]))
            username = input(colored("Enter a username: ", "yellow", attrs=["bold"]))
            password = input(colored("Enter a password: ", "yellow", attrs=["bold"]))
            confirm_password = input(colored("Confirm your password: ", "yellow", attrs=["bold"]))
            coach_fees = float(input(colored("Enter the coach's fees per class: $", "yellow", attrs=["bold"])))
            club.register(username, password, confirm_password, role="coach", coach_fees=coach_fees)
        elif choice == "3":
            print(colored("\nTreasurer Registration:", "green", attrs=["bold"]))
            username = input(colored("Enter a username: ", "yellow", attrs=["bold"]))
            password = input(colored("Enter a password: ", "yellow", attrs=["bold"]))
            confirm_password = input(colored("Confirm your password: ", "yellow", attrs=["bold"]))
            club.register(username, password, confirm_password, role="treasurer")
        elif choice == "4":
            print(colored("\nLogin:", "green", attrs=["bold"]))
            username = input(colored("Enter your username: ", "yellow", attrs=["bold"]))
            password = input(colored("Enter your password: ", "yellow", attrs=["bold"]))
            if club.login(username, password):
                if club.members[username]["role"] == "member":
                    member_ui(club, username)
                elif club.members[username]["role"] == "coach":
                    coach_ui(club, username)
                elif club.members[username]["role"] == "treasurer":
                    treasurer_ui(club, username)
        elif choice == "5":
            print(colored("Thank you for using the Membership Club!", "green", attrs=["bold"]))
            break
        else:
            print(colored("Invalid choice. Please try again.", "red", attrs=["bold"]))


if __name__ == "__main__":
    main()

