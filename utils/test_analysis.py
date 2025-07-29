from analysiss import run_analysis

if __name__ == "__main__":
    user_id = input("Enter user ID to test: ")
    data = run_analysis(user_id)

    print("\n=== Data Returned ===")
    print(f"Total Earned: {data['total_earned']}")
    print(f"Total Spent: {data['total_spent']}")
    print(f"Net Balance: {data['net_balance']}")

    print("\n--- Monthly Summary ---")
    for month, val in data['monthly_summary'].items():
        print(f"{month}: Earned ${val['earned']}, Spent ${val['spent']}")

    print("\n--- Spending by Category ---")
    for cat, amt in data['category_summary'].items():
        print(f"{cat}: ${amt}")

    print("\n--- Goal Progress ---")
    for g in data['goals']:
        print(f"{g['title']} - {g['progress']}% | Status: {g['status']}")
