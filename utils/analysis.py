import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from collections import defaultdict
from datetime import datetime
from db import get_transactions, get_goals

def get_recent_transactions(transactions, num_transactions):
    transactions.sort(key=lambda t: t.date, reverse=True)
    return transactions[:num_transactions]
def run_analysis(user_id):
    transactions = get_transactions(user_id)

    total_earned = sum(t.amount for t in transactions if t.amount > 0)
    total_spent = abs(sum(t.amount for t in transactions if t.amount < 0))
    net_balance = total_earned - total_spent

    print(f"Total earned by user {user_id}: {total_earned}")
    print(f"Total spent by user {user_id}: {total_spent}")
    print(f"Net balance for user {user_id}: {net_balance}")

    # Monthly Summary
    summary = defaultdict(lambda: {"earned": 0, "spent": 0})
    for t in transactions:
        month = datetime.strptime(t.date, "%Y-%m-%d").strftime("%Y-%m")
        if t.amount > 0:
            summary[month]["earned"] += t.amount
        else:
            summary[month]["spent"] += abs(t.amount)

    print("\n=== Monthly Summary ===")
    print("Month".ljust(10) + "Earned".rjust(15) + "Spent".rjust(15))
    print("-" * 40)
    for month, amounts in summary.items():
        print(f"{month}".ljust(10) + 
              f"${amounts['earned']:,.2f}".rjust(15) + 
              f"${amounts['spent']:,.2f}".rjust(15))
    print("-" * 40)

    # Category Summary
    category_summary = defaultdict(float)
    for t in transactions:
        if t.amount < 0:
            category_summary[t.category] += abs(t.amount)

    # Goals
    goals = get_goals(user_id)
    print("\n=== Goal Progress Summary ===")
    goal_progress_list = []
    for goal in goals:
        current_amount = sum(abs(t.amount) for t in transactions if t.category == goal.title and t.amount < 0)
        progress = (current_amount / goal.target_amount) * 100 if goal.target_amount else 0
        progress = round(min(progress, 100), 2)
        print(f"title: {goal.title}")
        print(f"target_amount: {goal.target_amount}")
        print(f"deadline: {goal.deadline}")
        print(f"current_amount: {current_amount}")
        print(f"progress: {progress}%")
        print(f"status: {goal.status}")
        print("-" * 40)

        goal_progress_list.append({
            "title": goal.title,
            "target": goal.target_amount,
            "deadline": goal.deadline,
            "current": current_amount,
            "progress": progress,
            "status": goal.status
        })

    return {
        "total_earned": total_earned,
        "total_spent": total_spent,
        "net_balance": net_balance,
        "monthly_summary": summary,
        "category_summary": category_summary,
        "goals": goal_progress_list,
        "transactions": transactions
    }
