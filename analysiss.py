import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import dates as mdates
from db import get_user,get_transactions,get_goals
from models import User, Transaction, Goal
from datetime import datetime
from collections import defaultdict

user_id = input("Enter user ID to analyze: ")
transactions = get_transactions(user_id)

total_earned = sum(t.amount for t in transactions if t.amount > 0)
total_spent = abs(sum(t.amount for t in transactions if t.amount < 0))

#Total earned and spent
print(f"Total earned by user {user_id}: {total_earned}")
print(f"Total spent by user {user_id}: {total_spent}")

# Net balance
net_balance = total_earned + total_spent
print(f"Net balance for user {user_id}: {net_balance}")

#get_montly_summary
def get_monthly_summary(transactions):
    summary = defaultdict(lambda: {"earned": 0, "spent": 0})
    for t in transactions:
        month = datetime.strptime(t.date, "%Y-%m-%d").strftime("%Y-%m")
        if t.amount > 0:
            summary[month]["earned"] += t.amount
        else:
            summary[month]["spent"] += abs(t.amount)
    return summary

# Display monthly summary

summary = get_monthly_summary(transactions)
print("\n=== Monthly Summary ===")
print("Month".ljust(10) + "Earned".rjust(15) + "Spent".rjust(15))
print("-" * 40)
for month, amounts in summary.items():
    print(f"{month}".ljust(10) + 
          f"${amounts['earned']:,.2f}".rjust(15) + 
          f"${amounts['spent']:,.2f}".rjust(15))
print("-" * 40)

months = list(summary.keys())
earned = [amounts['earned'] for amounts in summary.values()]
spent = [amounts['spent'] for amounts in summary.values()]

# Plotting the monthly summary

x= np.arange(len(months))
width =0.4
plt.bar(x - 0.2, earned, width = width, label = "Earned", color = "green",)
plt.bar(x + 0.2, spent, width = width, label = "Spent", color = "red")
plt.xlabel("Months")
plt.ylabel("Amount ($)")
plt.title("Monthly Summary")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

#Spending by category
def get_spending_by_category(transactions):
    category_summary = defaultdict(float)
    for t in transactions:
        if t.amount < 0:
            category_summary[t.category] += abs(t.amount)
        
    return category_summary

# Display spending by category

category_summary = get_spending_by_category(transactions)
labels = category_summary.keys()
size = category_summary.values()
plt.pie(size, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.  
plt.title('Spending by Category')
plt.show()
  
def goal_progress_summary(goal):
    current_amount = 0
    for t in transactions:
        if t.category == goal.title and t.amount < 0:
            current_amount += abs(t.amount)
    progress_percent_value = (current_amount / goal.target_amount) * 100 if goal.target_amount else 0
    progress_percent_value = round(progress_percent_value, 2)
    progress_percent_value = min(progress_percent_value, 100)
    return current_amount, progress_percent_value

goals = get_goals(user_id)
print("\n=== Goal Progress Summary ===")
for goal in goals:
    current_amount, progress_percent = goal_progress_summary(goal)
    print(f"title : {goal.title}")
    print(f"target_amount: {goal.target_amount}") 
    print(f"deadline: {goal.deadline}")
    print(f"current_amount: {current_amount}")
    print(f"progress: {progress_percent}%")
    print(f"status: {goal.status}")
    print("-" * 40)
