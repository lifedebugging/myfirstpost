from flask import Flask, render_template, request, redirect, session
from db import get_user_by_email, add_user
from utils.analysis import run_analysis, get_recent_transactions
 

import io
import base64
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def plot_monthly_chart(monthly_summary):
    months = list(monthly_summary.keys())
    earned = [monthly_summary[m]['earned'] for m in months]
    spent = [monthly_summary[m]['spent'] for m in months]
    fig, ax = plt.subplots()
    ax.bar(months, earned, label='Earned', color='green', alpha=0.6)
    ax.bar(months, spent, label='Spent', color='red', alpha=0.6, bottom=earned)
    ax.set_ylabel('Amount ($)')
    ax.set_title('Monthly Income vs Expenses')
    ax.legend()
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def plot_category_chart(category_summary):
    categories = list(category_summary.keys())
    amounts = list(category_summary.values())
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%')
    ax.set_title('Expenses by Category')
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        user = get_user_by_email(email)
        if user:
            session["user_id"] = user.user_id
            session["user_name"] = user.name
            print(f"Returning user: {user.name}")
        else:
            from models import User
            new_user = User(None, name, email, 0.0)
            add_user(new_user)
            user = get_user_by_email(email)
            if user:
                session["user_id"] = user.user_id
                session["user_name"] = user.name
                print(f"New user registered: {user.name}")
            else:
                # Handle error if user could not be added/fetched
                return "Registration failed. Please try again.", 500

        return redirect("/dashboard")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"], strict_slashes = False)
def login() -> str:
    if request.method == "POST":
        email = request.form['email']
        user = get_user_by_email(email)
        if user:
            session['user_email'] = user.email
            session['user_id'] = user.user_id
            return redirect("/add_transaction")
        else:
            return render_template("login.html", error="User not found. Please register first.")    
    return render_template("login.html") 

@app.route("/add_transaction", methods=["GET", "POST"], strict_slashes=False)
def add_transaction() -> str:
    if request.method == "GET":
        return render_template("add_transaction.html")
    
    try:
        txn_type = request.form["type"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        description = request.form.get("description")
        goal = request.form.get("goal_title")
        target = request.form.get("target")
        deadline = request.form.get("deadline")


        user_id = session.get("user_id")
        if not user_id:
            return "User not logged in.", 401

        from models import Transaction  
        transaction = Transaction(user_id, amount, category, date, description)
        if transaction.validate_transaction():
            from db import add_transaction
            add_transaction(transaction)
            
            return render_template("add_transaction.html", message="Transaction added successfully.")
        else:
            return "Invalid transaction.", 400
    except KeyError as e:
        return f"Missing form field: {e}", 400
    except ValueError as e:
        return f"Invalid form field value: {e}", 400
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route("/dashboard", methods=["GET"], strict_slashes=False)
def dashboard() -> str:
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    analysis = run_analysis(user_id)
    recent_transactions = get_recent_transactions(analysis["transactions"], 5)

    monthly_chart = plot_monthly_chart(analysis["monthly_summary"])
    category_chart = plot_category_chart(analysis["category_summary"])

    return render_template(
        "dashboard.html",
        analysis=analysis,
        monthly_chart=monthly_chart,
        recent_transactions=recent_transactions,
        category_chart=category_chart,
        user_name=session.get("user_name", "Guest")
    )
@app.route("/")
def index():
    return redirect("/register")

def summarize_monthly(transactions):
    from collections import defaultdict
    import datetime
    summary = defaultdict(lambda: {'earned': 0, 'spent': 0})
    for t in transactions:
        # If t.date is a string like "2025-07-29"
        month = datetime.datetime.strptime(t.date, "%Y-%m-%d").strftime("%b %Y")
        if t.amount > 0:
            summary[month]['earned'] += t.amount
        else:
            summary[month]['spent'] += abs(t.amount)
    return dict(sorted(summary.items()))

def summarize_categories(transactions):
    summary = {}
    for t in transactions:
        if t.category not in summary:
            summary[t.category] = 0
        summary[t.category] += abs(t.amount)
    return summary


if __name__ == "__main__":
    from db import initialize_database
    initialize_database()
    app.run(debug=True)
