import sqlite3
from models import User
from models import Transaction
from models import Goal


def initialize_database() -> None:
    """Create the database tables if they don't exist."""
    conn = sqlite3.connect('finance_tracker.db')  # Creates file if not exist
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        account_balance REAL DEFAULT 0.0)
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL,
        category TEXT,
        date TEXT,
        description TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        target_amount REAL NOT NULL,
        deadline TEXT,
        status TEXT DEFAULT 'not started',
        FOREIGN KEY(user_id) REFERENCES users(id)
        )
        ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()


def get_db_connection() -> sqlite3.Connection:
    """Get a connection to the database."""
    return sqlite3.connect('finance_tracker.db')


def add_user(user: User) -> None:
    """Add a user to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        print(f"User {user.email} already exists. Skipping.")
        conn.close()
        return

    cursor.execute('''
        INSERT INTO users (name, email, account_balance)
        VALUES (?, ?, ?)
    ''', (user.name, user.email, user.account_balance))
    conn.commit()
    user.id = cursor.lastrowid
    conn.close()
    print(f"User added: {user.name}")


def get_user(user_id: int) -> User | None:
    """Get a user from the database by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE id = ?
    ''', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    else:
        print("User not found")
        return None


def get_user_by_email(email: str) -> User | None:
    """Get a user from the database by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ?
    ''', (email,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    else:
        print("User not found")
        return None


def add_transaction(transaction: Transaction) -> bool:
    """Add a transaction to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if not transaction_exists(transaction.user_id, transaction.amount, transaction.category, transaction.date, transaction.description):
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.user_id, transaction.amount, transaction.category, transaction.date, transaction.description))
        conn.commit()
        conn.close()
        print("Transaction added successfully")
        return True
    else:
        print("Transaction already exists")
        conn.close()
        return False


def transaction_exists(user_id: int, amount: float, category: str, date: str, description: str) -> bool:
    """Check if a transaction already exists in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE user_id = ? AND amount = ? AND category = ? AND date = ? AND description = ?
    ''', (user_id, amount, category, date, description))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_transactions(user_id: int | None = None) -> list[Transaction]:
    """Get all transactions from the database for a given user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute('''
            SELECT * FROM transactions WHERE user_id = ?
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT * FROM transactions
        ''')
    transactions = cursor.fetchall()
    conn.close()
    return [Transaction(user_id=t[1], amount=t[2], category=t[3], date=t[4], description=t[5]) for t in transactions]


def add_goal(goal: Goal) -> None:
    """Add a goal to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO goals (user_id, title, target_amount, deadline, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (goal.user_id, goal.title, goal.target_amount, goal.deadline, goal.status))
    conn.commit()
    conn.close()
    print("Goal added successfully")


def get_goals(user_id: int | None = None) -> list[Goal]:
    """Get all goals from the database for a given user ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute('''
            SELECT * FROM goals WHERE user_id = ?
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT * FROM goals
        ''')
    goals = cursor.fetchall()
    conn.close()
    return [Goal(user_id=g[1], title=g[2], target_amount=g[3], deadline=g[4], status=g[5]) for g in goals]

