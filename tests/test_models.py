import pytest
import sys
import os

sys.path.append("/home/user/Documents/Assignment/Perosnal_Finance_Tracker_Project")
from models import User, Transaction, TransactionManager, Goal, FinanceTracker
def test_user_deposit_and_withdrawal():
    user = User(1, "Alice", "alice@example.com")
    user.make_deposit(100)
    assert user.account_balance == 100
    user.make_withdrawal(50)
    assert user.account_balance == 50

def test_user_withdrawal_insufficient_balance(capsys):
    user = User(2, "Bob", "bob@example.com")
    user.make_deposit(30)
    user.make_withdrawal(50)
    captured = capsys.readouterr()
    assert "Insufficient balance" in captured.out
    assert user.account_balance == 30

def test_user_transfer_money():
    user1 = User(3, "Carol", "carol@example.com")
    user2 = User(4, "Dave", "dave@example.com")
    user1.make_deposit(200)
    user1.transfer_money(user2, 100)
    assert user1.account_balance == 100
    assert user2.account_balance == 100

def test_user_update_email():
    user = User(5, "Eve", "eve@old.com")
    user.update_email("eve@new.com")
    assert user.email == "eve@new.com"

def test_transaction_validation():
    t = Transaction(1, 50, "food")
    assert t.validate_transaction()
    t2 = Transaction(1, -10, "food")
    assert not t2.validate_transaction()
    t3 = Transaction(1, 10, "invalid_category")
    assert not t3.validate_transaction()

def test_transaction_manager_add_and_get():
    tm = TransactionManager()
    t = Transaction(1, 100, "income")
    assert tm.add_transcation(t)
    assert tm.get_transaction(1)[0] == t

def test_goal_update_progress():
    goal = Goal(1, "Save", 100)
    goal.update_progress(50)
    assert goal.status == "in progress"
    goal.update_progress(100)
    assert goal.status == "completed"

def test_finance_tracker_add_user_and_goal():
    ft = FinanceTracker()
    user = User(6, "Frank", "frank@example.com")
    ft.add_user(user)
    assert ft.users[0] == user
    goal = Goal(6, "Trip", 500)
    ft.add_goal(goal)
    assert ft.goals[0] == goal

def test_finance_tracker_get_summary():
    ft = FinanceTracker()
    ft.add_user(User(7, "Grace", "grace@example.com"))
    ft.add_goal(Goal(7, "Car", 1000))
    summary = ft.get_summary()
    assert summary["total_users"] == 1
    assert summary["total_goals"] == 1

def test_goal_to_dict():
    goal = Goal(8, "Bike", 200)
    d = goal.to_dict()
    assert d["name"] == "Bike"
    assert d["target_amount"] == 200

def test_user_invalid_deposit_and_withdrawal(capsys):
        user = User(9, "Henry", "henry@example.com")
        user.make_deposit(-10)
        captured = capsys.readouterr()
        assert "Invalid amount" in captured.out
        assert user.account_balance == 0
        user.make_withdrawal(0)
        captured = capsys.readouterr()
        assert "Invalid amount" in captured.out
        assert user.account_balance == 0

def test_user_transfer_insufficient_balance(capsys):
        user1 = User(10, "Ivy", "ivy@example.com")
        user2 = User(11, "Jack", "jack@example.com")
        user1.make_deposit(20)
        user1.transfer_money(user2, 50)
        captured = capsys.readouterr()
        assert "Insufficient balance for transfer" in captured.out
        assert user1.account_balance == 20
        assert user2.account_balance == 0

def test_transaction_to_dict():
        t = Transaction(12, 75, "travel", description="Vacation")
        d = t.to_dict()
        assert d["user_id"] == 12
        assert d["amount"] == 75
        assert d["category"] == "travel"
        assert d["description"] == "Vacation"

def test_transaction_manager_invalid_transaction(capsys):
        tm = TransactionManager()
        t = Transaction(13, -20, "food")
        result = tm.add_transcation(t)
        captured = capsys.readouterr()
        assert not result
        assert "Invalid transaction" in captured.out
        assert len(tm.transactions) == 0

def test_transaction_manager_get_transaction_empty():
        tm = TransactionManager()
        assert tm.get_transaction(99) == []

def test_goal_to_dict_fields():
        goal = Goal(14, "Emergency Fund", 1000)
        d = goal.to_dict()
        assert set(d.keys()) == {"user_id", "name", "target_amount", "deadline", "status"}
        assert d["status"] == "not started"

def test_finance_tracker_get_user_by_goals():
        ft = FinanceTracker()
        user = User(15, "Kim", "kim@example.com")
        ft.add_user(user)
        goal1 = Goal(15, "Laptop", 800)
        goal2 = Goal(16, "Phone", 500)
        ft.add_goal(goal1)
        ft.add_goal(goal2)
        user_goals = ft.get_user_by_goals(15)
        assert goal1 in user_goals
        assert goal2 not in user_goals

def test_user_display_user_balance(capsys):
        user = User(16, "Leo", "leo@example.com")
        user.make_deposit(120)
        user.display_user_balance()
        captured = capsys.readouterr()
        assert "120" in captured.out

def test_user_get_account_summary(capsys):
        user = User(17, "Mona", "mona@example.com")
        user.make_deposit(300)
        user.get_account_summary()
        captured = capsys.readouterr()
        assert "User: Mona" in captured.out
        assert "Account Balance 300" in captured.out
