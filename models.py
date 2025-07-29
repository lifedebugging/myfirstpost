from datetime import datetime
class User:
    def __init__(self, user_id: int, name: str, email: str, account_balance: float = 0.0):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.account_balance = account_balance
        self.transaction_history = []

    def make_deposit(self, amount: float):
        if not self.validate_amount(amount):
            return
        self.account_balance += amount
        print(self.account_balance)

    def make_withdrawal(self, amount: float):
        if not self.validate_amount(amount):
            return
        if amount > self.account_balance:
            print("Insufficient balance")
            return
        self.account_balance -= amount
        print(self.account_balance)

    def display_user_balance(self):
        print(self.account_balance)

    def transfer_money(self, other_user: "User", amount: float):
        if not self.validate_amount(amount):
            return
        if self.account_balance >= amount:
            self.account_balance -= amount
            other_user.account_balance += amount
            print("Transfer successful")
        else:
            print("Insufficient balance for transfer")

    @staticmethod
    def validate_amount(amount: float):
        if amount <= 0:
            print("Invalid amount")
            return False
        return True

    def update_email(self, new_email: str):
        self.email = new_email

    def get_account_summary(self):
        print(f"User: {self.name} Email {self.email} Account Balance {self.account_balance}")


    
class Transaction:
    VALID_CATEGORIES = ["food", "rent", "income", "travel", "entertainment", "healthcare", "education"]
    def __init__(self, user_id, amount, category, date = None, description = None):
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date or datetime.today()
        self.description = description

    def validate_transaction(self):
        return self.amount > 0 and self.category in self.VALID_CATEGORIES

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description
        }        

class TransactionManager:
    def __init__(self):
        self.transactions = []

    def add_transcation(self,transaction):
        if transaction.validate_transaction():
            self.transactions.append(transaction)
            print("Transaction added successfully")
            return True
        else:
            print("Invalid transaction")
            return False
        
    def get_transaction(self,user_id):
        if user_id is not None:
            return [t for t in self.transactions if t.user_id == user_id]
        return self.transactions
    
    def get_balance(self,user_id):
        balance = 0
        for t in self.get_transaction(user_id):
            if t.category == "income" or t.trans_type == "deposit":
                balance += t.amount

            elif t.category != "income" or t.trans_type == "withdrawal":
                balance -= t.amount

        return balance

class Goal:

    VALID_STATUSES = ["not started", "in progress", "completed"]
    def __init__(self, user_id, title, target_amount, deadline, status):
        self.user_id = user_id
        self.title= title
        self.target_amount = target_amount
        self.deadline = deadline or datetime.today()
        self.status = status if status in self.VALID_STATUSES else "not started"

    def update_progress(self,amount):
        if amount >= self.target_amount:
            self.status = 'completed'
            print("Goal completed")
        else:
            self.status = 'in progress'
            print("Goal progress updated")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "title": self.title,
            "target_amount": self.target_amount,
            "deadline": self.deadline,
            "status": self.status
        }


    
class FinanceTracker:
    def __init__(self):
        self.users = []
        self.transactions = []
        self.goals = []
        self.current_user = None

    def add_user(self,user):
        self.users.append(user)
        print("User added successfully")

    def add_transactonion(self,transaction):
        return self.transaction_manager.add_transaction(transaction)
    
    def add_goal(self, goal):
        self.goals.append(goal)
        print("Goal added successfully")
    
    def get_user_by_goals(self, user_id):
        return [g for g in self.goals if g.user_id == user_id]
    
    def get_summary(self):
        return {
            "total_users": len(self.users),
            "total_transactions": len(self.transactions),
            "total_goals": len(self.goals)
        }

#goal_category_mapping 
goal_category_mapping = {
    "Vacation": "travel",
    "Buy a Bike": "transportation",
    "Emergency Fund": "savings",
    "Home Renovation": "home improvement",
    "Gadget Upgrade": "electronics",
    "Wedding": "event",
    "New Laptop": "electronics",
    "Education": "education",
    "Business Investment": "investment",
    "Medical Fund": "healthcare"
}
def get_goal_category(goal_titles):
    return goal_category_mapping.get(goal_titles, "other")

def get_goal_status(goal):
    if goal.status in Goal.VALID_STATUSES:
        return goal.status
    else:
        return "not started"

def get_goal_progress(goal):
    if goal.status == "completed":
        return goal.target_amount
    elif goal.status == "in progress":
        return goal.target_amount * 0.5  # Example: 50% progress for in-progress goals
    else:
        return 0  # Not started or invalid status
