# 🧾 FinTrack – Personal Finance Tracker

A lightweight Flask web app to help users **track their income, expenses, and financial goals** — all in one place. Includes dynamic charts, real-time goal progress, and a dashboard UI.

---

## 🚀 Features

- 📊 **Dashboard Overview**: Track income, expenses, and net balance
- 📅 **Monthly Summary**: Bar chart for earned vs spent across months
- 🥧 **Category Breakdown**: Pie chart showing spending by category
- 🧾 **Add Transactions**: Record income or expenses with descriptions
- 🎯 **Set Financial Goals**: Track goal progress with target and deadlines
- 🧠 **Data Analysis**: Backed by Python logic & matplotlib visualizations
- 🔐 **Login System**: Simple login using email (for now)

---

## 🛠️ Tech Stack

| Layer        | Tool               |
|--------------|--------------------|
| Backend      | Python (Flask)     |
| Frontend     | HTML5, CSS3        |
| Database     | SQLite3            |
| Charts       | Matplotlib (image encoded) |
| Data Utils   | Pandas, io, base64 |

---

## 📷 Screenshots

*(Add screenshots if you want — dashboard, charts, etc.)*

---

## 📁 Folder Structure
│
├── app.py # Main Flask app
├── db.py # DB setup and queries
├── models.py # Data classes: User, Transaction, Goal
├── utils/
│ └── analysis.py # All business logic and chart generators
├── templates/ # HTML views
│ ├── dashboard.html
│ ├── add_transaction.html
│ └── login.html
├── static/
│ └── style.css # App styling
├── seed.py # Script to add sample users and data
├── requirements.txt # All dependencies
├── README.md # This file
└── .gitignore
