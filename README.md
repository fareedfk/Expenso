# Expenso — Personal Expense Tracker

A modern, high-performance personal finance and expense management application designed for speed, privacy, and actionable insights.

![Expenso Dashboard](https://raw.githubusercontent.com/fareedfk/Expenso/main/apps/web/public/img/logo.svg)

## ✨ Highlights

- **Quick Record Entry (<5s)**: Streamlined landing page with an encircled action hub and top frequently used category chips.
- **Complete Privacy & Isolation**: Each user gets a completely isolated workspace with seeded default categories.
- **Interactive Analytics**: Monthly breakdown, category donut charts, daily spending trends, and budget progress bars.
- **Smart Budgets & Recurring Bills**: Track category limits with visual indicators and manage active subscriptions.
- **Fast Search & Filter**: Filter transactions by type, category, date range, amount, and text query.
- **Monorepo Turborepo Architecture**: Clean separation between FastAPI backend (`apps/api`), modular frontend (`apps/web`), and shared packages.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, PyMySQL / SQLite fallback, Pydantic, JWT Authentication (bcrypt).
- **Frontend**: Vanilla HTML5, Semantic CSS3, Vanilla JavaScript ES6+, Chart.js.
- **Monorepo**: Turborepo, NPM workspaces.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- MySQL (via XAMPP, Docker, or native service) or automatic SQLite fallback.
- Node.js & npm (optional, for Turbo pipeline)

### 2. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your MySQL credentials (if MySQL is running, otherwise SQLite is used automatically)

# Optional: Seed sample demo data
python seed.py

# Start application server
python run.py
```

The application will be live at `http://127.0.0.1:8000`.

---

## 🏛️ Architecture & Clean Code Rules

- **Strict File Limit**: Every file is strictly under 500 lines of code (<500 LOC).
- **Domain-Driven Isolation**: Feature routers, models, and schemas are isolated under `apps/api/domain/<feature>`.
- **Frontend Modularity**: Separated CSS layers (`tokens.css`, `base.css`, `components.css`, `home.css`) and modular JS views (`services/`, `components/`, `views/`).

---

## 📄 License
MIT License
