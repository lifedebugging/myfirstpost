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
<img width="1339" height="593" alt="image" src="https://github.com/user-attachments/assets/e6527078-5c0f-483c-bbad-ed1f9db7a00d" />
<img width="1344" height="586" alt="image" src="https://github.com/user-attachments/assets/deed562f-264d-43d0-ba1a-19a53e3a903f" />
<img width="1336" height="596" alt="image" src="https://github.com/user-attachments/assets/b1855959-17f3-4297-af83-3f3a8d5ad527" />
<img width="1339" height="592" alt="image" src="https://github.com/user-attachments/assets/f2f80fc1-55d6-443a-8a55-af3c4d0ec011" />




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

---
## ⚙️ Installation

```bash
git clone https://github.com//finance-tracker.git
cd finance-tracker
pip install -r requirements.txt
python seed.py  # Optional: adds sample users/data
flask run
Then open: http://localhost:5000

##🧪 Sample Login
Use any of these pre-seeded emails (no password needed):
user1@example

##📌 Todo / Future Ideas
Add user registration + hashed passwords

Export transactions to CSV

Add dark mode 🌑

Connect to PostgreSQL for production

##🧑‍💻 Author
Made by Kiyo – Built with love, Flask, and some ✨ late-night energy
Wanna collab or learn more? GitHub Profile





