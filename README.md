<div align="center">

# 💎 Expenso

### *The High-Speed, Private Personal Finance Tracker*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Turborepo](https://img.shields.io/badge/Turborepo-EF4444?style=for-the-badge&logo=turborepo&logoColor=white)](https://turbo.build)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Built for lightning-fast expense logging (< 5s), zero data leakage, and deep financial clarity.</b>
</p>

[Explore Features](#-features) •
[Quick Start](#-quick-start) •
[Keyboard Shortcuts](#-keyboard-shortcuts) •
[Architecture](#-architecture) •
[API Reference](#-api-documentation)

---

</div>

## 🌟 Why Expenso?

Most finance apps force you through 5–6 screens just to record a coffee. **Expenso** is built on the core principle:

> **Minimum Clicks → Maximum Information**

- ⚡ **Zero-Latency Landing Hub**: Centered hero action trigger (`+`) with instant Expense vs Income branching.
- 🎯 **One-Click Frequent Categories**: Pre-calculated top 4 monthly categories with live spend badges (`🍔 Food`, `🛒 Shopping`, `🚕 Transport`, `💡 Bills`).
- 🔒 **Zero Data Leakage**: User-isolated databases, bcrypt-hashed credentials, stateless JWT tokens, and automated category seeding per user.
- 📊 **Real-Time Visual Intelligence**: Dynamic doughnut breakdowns, daily burn rates, and monthly budget progress monitors.
- 🔄 **Recurring Subscriptions & Budgets**: Set category caps and monitor active memberships without surprise renewals.
- ⚡ **Supercharged Keyboard Navigation**: Command bar (`Ctrl+K`), instant expense modal (`E`), instant income modal (`I`), and global search (`/`).

---

## 🎨 Feature Showcase

| 🏠 Quick Landing View | 📊 Financial Analytics | 💳 Ledger & Search |
| :---: | :---: | :---: |
| Centered Encircled Hero `+` & 4 Frequent Categories | Category Donut & Daily Trend Lines | Multi-filter Transactions & Pagination |

| 🏷️ Category Management | 🎯 Monthly Budgets | 🔄 Recurring Subscriptions |
| :---: | :---: | :---: |
| Custom Colors & Emoji/Lucide Icons | Visual Progress & Warning Thresholds | Auto-Renewal Dates & Billing Cycles |

---

## ⌨️ Power-User Keyboard Shortcuts

Expenso is designed to be operated completely keyboard-first:

| Shortcut | Action | Description |
| :---: | :--- | :--- |
| <kbd>Ctrl</kbd> + <kbd>K</kbd> | **Command Bar** | Quick access to any action, view, or modal |
| <kbd>E</kbd> | **Add Expense** | Opens expense logger with amount auto-focused |
| <kbd>I</kbd> | **Add Income** | Opens income logger immediately |
| <kbd>/</kbd> | **Search Ledger** | Jumps to transaction ledger and focuses filter |
| <kbd>Esc</kbd> | **Close / Dismiss** | Closes any open modal overlay instantly |

---

## 🏛️ Architecture & Clean Code

Expenso adheres to strict domain-driven standards and clean monorepo architecture:

```
expenso/
├── apps/
│   ├── api/                     # High-performance FastAPI backend service
│   │   ├── core/                # Database engines, config, JWT security
│   │   └── domain/              # Domain-isolated modules (Models, Schemas, Routers)
│   │       ├── auth/            # Registration, login, profile, password change
│   │       ├── transactions/    # CRUD, pagination, filtering, summaries
│   │       ├── categories/      # Custom categories & icons
│   │       ├── budgets/         # Monthly thresholds & progress calculation
│   │       ├── analytics/       # Cashflow, category breakdown, trend charts
│   │       └── recurring/       # Active subscriptions & recurring reminders
│   └── web/                     # Modular frontend client (Zero framework bloat)
│       └── public/
│           ├── css/             # Semantic CSS layers (tokens, base, components, home)
│           └── js/              # Modular JS views, charts, and state store
├── packages/config/             # Shared build configurations & ESLint rules
├── AGENTS.md                    # Operational standards (< 500 LOC per file)
└── turbo.json                   # Monorepo pipeline orchestrator
```

> [!NOTE]
> **Strict Line Limit Standard**: Every single file across the entire codebase strictly stays under **500 lines of code** for maximum maintainability.

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/fareedfk/Expenso.git
cd Expenso
```

### 2. Environment Configuration
```bash
cp .env.example .env
```
*(Default settings automatically fall back to SQLite if MySQL is not detected)*

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Optional: Seed Demo Workspace
```bash
python seed.py
```

### 5. Launch the Application
```bash
python run.py
```
App will be running at **`http://127.0.0.1:8000`**.

---

## 📡 API Documentation

Interactive Swagger documentation is auto-generated by FastAPI:

- **Swagger UI**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **ReDoc**: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

---

## 🛡️ Security & Privacy

- **Stateless Authentication**: Pure JWT bearer tokens with standard header verification.
- **Passlib & Bcrypt**: Industry-standard cryptographic salt and hashing for passwords.
- **Strict User Isolation**: All transactional data, categories, budgets, and analytics queries are explicitly bound to the authenticated `user_id`.

---

<div align="center">

Crafted with care for speed, simplicity, and financial wellness.

⭐ **Star this repository if you find it helpful!**

</div>
