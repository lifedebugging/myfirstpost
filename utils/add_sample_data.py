from db import initialize_database, add_user, add_transaction, add_goal
from models import User, Transaction, Goal
from datetime import datetime, timedelta
import random

def add_sample_data():
    # Initialize database
    initialize_database()

    # Sample user data
    user_infos = [
        ("John Doe", "john@example.com"),
        ("Jane Smith", "jane@example.com"),
        ("Alice Johnson", "alice@example.com"),
        ("Bob Brown", "bob@example.com"),
        ("Charlie Lee", "charlie@example.com"),
        ("Diana King", "diana@example.com"),
        ("Ethan Clark", "ethan@example.com"),
        ("Fiona Scott", "fiona@example.com"),
        ("George Young", "george@example.com"),
        ("Hannah Adams", "hannah@example.com"),
    ]

    # Add users
    user_ids = []
    for name, email in user_infos:
        user = User(None, name, email, 0.0)
        add_user(user)
        from db import get_user_by_email
        user_db = get_user_by_email(email)
        user_ids.append(user_db.user_id)

    # Categories for transactions
    categories = ["income", "rent", "food", "entertainment", "travel", "healthcare", "education", "utilities"]

    # Add transactions for each user
    for user_id in user_ids:
        # Each user gets 8 transactions
        for i in range(8):
            date = (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")
            if i % 4 == 0:
                # Income transaction
                amount = random.randint(2000, 4000)
                category = "income"
                description = "Salary"
            else:
                # Expense transaction
                amount = -random.randint(50, 800)
                category = random.choice(categories[1:])
                description = f"{category.capitalize()} expense"
            txn = Transaction(user_id, amount, category, date, description)
            add_transaction(txn)

    # Add sample goals for each user
    for user_id in user_ids:
        goals = [
            Goal(user_id, "Emergency Fund", random.randint(3000, 7000), "2025-12-31", "in progress"),
            Goal(user_id, "Vacation", random.randint(1000, 4000), "2025-06-30", "not started"),
        ]
        for goal in goals:
            add_goal(goal)

    print("Sample data for 10 users added successfully!")
    print("You can now test the dashboard with this sample data.")

if __name__ == "__main__":
    add_sample_data() 
