# College Presentation Slide Data — Expenso Project
# Submitted by: Fareed Khilji | 23EA0CA030
# Submitted to: Dr. Sanjay Tiwari (HOD)

STUDENT = {
    "name": "Fareed Khilji",
    "roll": "23EA0CA030",
    "submitted_to": "Dr. Sanjay Tiwari",
    "designation": "(HOD, CSE Dept.)",
    "course": "B.Tech — Computer Science & Engineering",
    "college": "Arya Institute of Engineering Technology & Management (AIETM), Jaipur",
    "year": "4th Year  |  Academic Year 2025-26",
    "project": "Expenso — Personal Finance & Expense Tracker",
    "type": "Major Project / Capstone Project",
}

COLLEGE_SLIDES = [
    {   # Slide 2: Introduction
        "tag": "INTRODUCTION",
        "title": "Introduction to Expenso",
        "points": [
            "Expenso is a full-stack personal finance and expense tracking web application.",
            "It enables users to log daily income and expenses quickly with minimal effort.",
            "The system provides visual analytics through charts and summary dashboards.",
            "Built using FastAPI (Python) on the backend and Vanilla JavaScript on the frontend.",
            "Data is stored locally in an SQLite database via SQLAlchemy ORM.",
            "The goal is to make financial tracking fast, private, and hassle-free.",
        ],
        "footer": "Introduction"
    },
    {   # Slide 3: Objectives
        "tag": "OBJECTIVES",
        "title": "Objectives of the Project",
        "points": [
            "To design a lightweight, fast, and responsive personal finance tracker.",
            "To implement secure user authentication using JWT tokens and bcrypt hashing.",
            "To allow users to log expenses in under 5 seconds with minimal clicks.",
            "To auto-detect expense categories based on typed description keywords.",
            "To provide real-time income vs expense analytics via interactive charts.",
            "To follow Clean Architecture and Domain-Driven Design principles throughout.",
        ],
        "footer": "Objectives"
    },
    {   # Slide 4: Problem Statement
        "tag": "PROBLEM STATEMENT",
        "title": "Problem Statement",
        "points": [
            "Most existing finance apps require 5–6 screens and multiple dropdowns to log one entry.",
            "Commercial apps often track user behavior and sell data to third-party advertisers.",
            "Heavy frontend frameworks (React, Angular) make apps slow on low-end devices.",
            "No simple, self-hosted, privacy-first solution exists for everyday expense tracking.",
            "Users abandon habit tracking within 14 days due to friction and complexity.",
            "Expenso solves all these issues with a clean, single-page, zero-bloat architecture.",
        ],
        "footer": "Problem Statement"
    },
    {   # Slide 5: System Architecture
        "tag": "SYSTEM DESIGN",
        "title": "System Architecture",
        "points": [
            "Monorepo structure using Turborepo with apps/api and apps/web workspaces.",
            "Backend: FastAPI ASGI app with domain-driven modules (auth, expenses, income).",
            "Frontend: Modular Vanilla JS with Services → Views → Components layers.",
            "Database: SQLite with SQLAlchemy ORM, Users and Transactions tables.",
            "Authentication: Stateless JWT (HS256 algorithm) stored in localStorage.",
            "CSS is split into tokens, base, components, modals, and responsive layers.",
        ],
        "footer": "System Architecture"
    },
    {   # Slide 6: Technology Stack
        "tag": "TECHNOLOGY STACK",
        "title": "Technology Stack Used",
        "points": [
            "Backend Language: Python 3.10+ with FastAPI framework (async ASGI server).",
            "ORM & Database: SQLAlchemy 2.0 with SQLite (relational, RDBMS with FK cascades).",
            "Security: Passlib bcrypt for password hashing; python-jose for JWT tokens.",
            "Frontend: Modular Vanilla JavaScript (ES6 IIFE pattern), HTML5, CSS3.",
            "Data Validation: Pydantic v2 schemas for all API request/response models.",
            "Charts & Analytics: Chart.js library for real-time bar and doughnut charts.",
        ],
        "footer": "Technology Stack"
    },
    {   # Slide 7: Database Design
        "tag": "DATABASE DESIGN",
        "title": "Database Schema & Design",
        "points": [
            "Users Table: id (PK), username, email, full_name, hashed_password, created_at.",
            "Transactions Table: id (PK), user_id (FK), type, amount, category, description.",
            "Transactions also store: payment_mode, date, and created_at timestamp.",
            "Foreign key cascade: deleting a user removes all associated transactions.",
            "ORM models defined in domain/expenses/models.py and domain/auth/models.py.",
            "Database migrations handled via SQLAlchemy Base.metadata.create_all().",
        ],
        "footer": "Database Design"
    },
    {   # Slide 8: Key Features
        "tag": "KEY FEATURES",
        "title": "Key Features of Expenso",
        "points": [
            "Smart Category Auto-Detection: Types keywords like 'pizza' → Food auto-selected.",
            "Quick Expense Logging: Add any expense in under 5 seconds from the home screen.",
            "Income & Expense Isolation: Adding income never affects the expense form state.",
            "Visual Dashboard: Real-time charts showing income vs expense with category breakdown.",
            "User Authentication: Secure login/signup with JWT sessions and bcrypt passwords.",
            "Profile Management: Users can update name, email, and password from the UI.",
        ],
        "footer": "Key Features"
    },
    {   # Slide 9: Implementation
        "tag": "IMPLEMENTATION",
        "title": "Implementation Details",
        "points": [
            "Frontend services handle API calls (authService.js, expenseService.js, etc.).",
            "Views render components like expenseList, categoryGrid, and dashboard charts.",
            "app.js is a thin orchestrator that initializes views and routes user actions.",
            "Backend routers are isolated per domain: /api/auth, /api/expenses, /api/income.",
            "Category prediction runs locally in the browser using a keyword dictionary map.",
            "Responsive CSS with token-based design system works across all screen sizes.",
        ],
        "footer": "Implementation"
    },
    {   # Slide 10: Testing & Results
        "tag": "TESTING & RESULTS",
        "title": "Testing & Results",
        "points": [
            "All REST API endpoints tested via browser and manual HTTP request validation.",
            "JWT authentication tested: invalid tokens return 401 Unauthorized correctly.",
            "Category auto-detection tested with 20+ keywords across 8 expense categories.",
            "Dashboard analytics verified to update in real-time after each transaction entry.",
            "Income isolation tested: expense state fully resets before each income entry.",
            "Application runs locally on http://localhost:8000 with zero setup required.",
        ],
        "footer": "Testing & Results"
    },
    {   # Slide 11: Conclusion
        "tag": "CONCLUSION",
        "title": "Conclusion",
        "points": [
            "Expenso successfully demonstrates a production-grade full-stack web application.",
            "The project applies Clean Architecture, JWT security, and ORM-based database design.",
            "Category auto-detection reduces user effort and improves the logging experience.",
            "The modular codebase strictly follows the < 500 LOC per file engineering discipline.",
            "The project is fully functional, self-hosted, and runs without any cloud dependencies.",
            "Future scope: Mobile app, UPI statement import, AI-powered spending insights.",
        ],
        "footer": "Conclusion"
    },
    {   # Slide 12: References
        "tag": "REFERENCES",
        "title": "References",
        "points": [
            "FastAPI Documentation — https://fastapi.tiangolo.com",
            "SQLAlchemy ORM Docs — https://docs.sqlalchemy.org",
            "Pydantic v2 Guide — https://docs.pydantic.dev",
            "JWT Standard (RFC 7519) — https://tools.ietf.org/html/rfc7519",
            "Chart.js Documentation — https://www.chartjs.org/docs",
            "OWASP Security Guidelines — https://owasp.org/www-project-top-ten",
        ],
        "footer": "References"
    },
]
