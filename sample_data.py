"""from db import add_user, add_transaction, add_goal
from models import User, Transaction, Goal
from datetime import datetime, timedelta
import random
import numpy as np

users = []
for i in range(1, 21):
    user = User(i, f"User{i}", f"user{i}@example.com")
    user.account_balance = round(np.random.uniform(100, 5000), 2)
    add_user(user)
    users.append(user)

for user in users:
    if user is None:
        raise ValueError("User is None")
    for j in range(50, 150):
        category = random.choice(["food", "rent", "income", "travel", "entertainment", "healthcare", "education"])
        if category == "income":
            amount = round(random.uniform(500, 3000), 2)
        elif category == "rent":
            amount = round(random.uniform(-3000, -1000), 2)
        elif category == "food":
            amount = round(random.uniform(-500, -50), 2)
        elif category == "travel":
            amount = round(random.uniform(-1000, -100), 2)
        elif category == "entertainment":
            amount = round(random.uniform(-800, -50), 2)
        elif category == "healthcare":
            amount = round(random.uniform(-1500, -100), 2)
        elif category == "education":
            amount = round(random.uniform(-2000, -200), 2)
        else:
            amount = round(random.uniform(-500, 500), 2)  # fallback
        date = (datetime.today() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        description = f"Transaction {j+1} for {user.name}"
        transaction = Transaction(user.user_id, amount, category, date, description)
        try:
            add_transaction(transaction)
        except Exception as e:
            print(f"Error adding transaction for {user.name}: {e}")
        print(f"Added transaction for {user.name}: {transaction.to_dict()}")
         

goal_titles = [
    "Vacation", "Buy a Bike", "Emergency Fund", "Home Renovation", "Gadget Upgrade", 
    "Wedding", "New Laptop", "Education", "Business Investment", "Medical Fund"
]
for user in users:
    if user is None:
        raise ValueError("User is None")
    num_goals = random.randint(1, 5)
    for i in range(num_goals):
        user_id = user.user_id
        title = f"{random.choice(goal_titles)} #{i+1}"
        target_amount = round(random.uniform(1000, 20000), 2)
        deadline = (datetime.today() + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        status = random.choice(["not started", "in progress", "completed"])
        goal = Goal(user_id, title, target_amount, deadline, status)

        # Add some progress randomly
        progress = round(random.uniform(0, target_amount * 0.7), 2)
        goal.update_progress(progress)

        try:
            add_goal(goal)
        except Exception as e:
            print(f"Error adding goal {i+1}: {e}")
        print(f"Added goal {i+1}: {goal.to_dict()}")

"""
# This code is used to generate sample data for the Personal Finance Tracker project.
# It creates 20 users, each with 50-150 transactions and 1-5 financial goals.
# The transactions are randomly generated with different categories and amounts.
# The goals are also randomly generated with titles, target amounts, deadlines, and statuses.
# The data is added to the database using the add_user, add_transaction, and add_goal functions.
