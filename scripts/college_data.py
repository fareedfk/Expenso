# Slide Data for Expenso College Presentation
# Student: Fareed Khilji (23EA0CA030)
# Guide: Dr. Sanjay Tiwari (HOD, CSE)
# College: Arya Institute of Engineering Technology & Management (AIETM), Jaipur

STUDENT = {
    "name": "Fareed Khilji",
    "roll": "23EA0CA030",
    "submitted_to": "Dr. Sanjay Tiwari",
    "designation": "(HOD, CSE Dept.)",
    "course": "B.Tech — Computer Science & Engineering",
    "college": "Arya Institute of Engineering Technology & Management (AIETM), Jaipur",
    "year": "4th Year  |  Academic Year 2025–26",
    "project": "Expenso — Personal Finance & Expense Tracker",
    "presentation_type": "Industrial Training Presentation",
}

SLIDES_CONTENT = [
    # Slide 2: Overview & Concept
    {
        "tag": "EXECUTIVE OVERVIEW",
        "title": "Project Overview & Core Concept",
        "type": "overview",
        "cards": [
            {
                "title": "💡 What is Expenso?",
                "bg": "F8FAFC",
                "border": "CBD5E1",
                "accent": "1E3A8A",
                "items": [
                    "A full-stack, privacy-first personal finance application.",
                    "Engineered for sub-5-second daily expense and income logging.",
                    "Interactive real-time analytics with Chart.js visualization.",
                    "Self-hosted SQLite database with zero cloud data sharing."
                ]
            },
            {
                "title": "🎯 Motivation & Need",
                "bg": "F8FAFC",
                "border": "CBD5E1",
                "accent": "2563EB",
                "items": [
                    "Existing apps require 5-6 clicks and rigid complex forms.",
                    "Commercial apps read user SMS and monetize private habits.",
                    "Heavy frontends cause sluggish performance on mobile devices.",
                    "Expenso offers a clean, lightning-fast, zero-bloat solution."
                ]
            }
        ],
        "metrics": [
            ("⚡ < 5s Logging", "Zero-friction entry workflow"),
            ("🔒 100% Private", "Local SQLite database storage"),
            ("📱 Zero Bloat", "Vanilla JS with no npm overhead")
        ]
    },

    # Slide 3: Problem Statement
    {
        "tag": "PROBLEM IDENTIFICATION",
        "title": "Problem Statement & Market Gaps",
        "type": "comparison",
        "left": {
            "title": "❌ Current Industry Problems",
            "bg": "FEF2F2",
            "border": "FCA5A5",
            "accent": "DC2626",
            "items": [
                "Tedious Logging: 5+ steps to record a single cup of tea/coffee.",
                "Privacy Invasions: Apps snoop SMS messages and sale leads.",
                "Bloated Frameworks: 10MB+ bundle sizes slow on budget devices.",
                "Cluttered UI: Cluttered with ads, loans, and credit card promotions.",
                "High Abandonment: Over 80% users stop tracking within 14 days."
            ]
        },
        "right": {
            "title": "✅ Expenso Solution",
            "bg": "F0FDF4",
            "border": "86EFAC",
            "accent": "16A34A",
            "items": [
                "Sub-5s Rapid Entry: Default payment mode (UPI) & optional fields.",
                "Strict Privacy: Data stays in local SQLite; zero external trackers.",
                "Modular Vanilla JS: Instant load times under 150ms without bloat.",
                "Clean Minimal UI: Ad-free, focused dashboard with smooth themes.",
                "Intelligent Auto-Detect: Predicts categories from keywords automatically."
            ]
        }
    },

    # Slide 4: Objectives
    {
        "tag": "PROJECT OBJECTIVES",
        "title": "Key Objectives & Goals",
        "type": "grid_4",
        "cards": [
            ("🎯 Rapid Expense Capture", "Enable users to log any transaction within 5 seconds with pre-selected UPI defaults and optional descriptions.", "1E3A8A"),
            ("🤖 NLP Keyword Auto-Detect", "Implement client-side category prediction so typing 'Pizza' instantly selects Food & Dining without manual clicks.", "2563EB"),
            ("🛡️ Secure Auth & Session", "Implement production-grade JWT stateless authentication, bcrypt password hashing, and role isolation.", "0D9488"),
            ("📊 Real-Time Analytics", "Render dynamic income vs expense breakdowns and category charts instantly updated via Chart.js.", "7C3AED")
        ]
    },

    # Slide 5: System Architecture
    {
        "tag": "SYSTEM ARCHITECTURE",
        "title": "Three-Tier System Architecture",
        "type": "architecture",
        "tiers": [
            {
                "tier": "Tier 1: Client Layer (Web)",
                "sub": "Modular Vanilla JavaScript (ES6+)",
                "details": ["Services (api.js, expenseService.js)", "Views (expenseList, charts, modals)", "Design Tokens (tokens.css, base.css)"]
            },
            {
                "tier": "Tier 2: Application Layer (API)",
                "sub": "FastAPI ASGI Server (Python 3.10+)",
                "details": ["Domain Routers (/auth, /expenses, /income)", "Pydantic v2 Request Validation", "Stateless JWT Auth & Bcrypt Security"]
            },
            {
                "tier": "Tier 3: Database Layer (Storage)",
                "sub": "SQLite via SQLAlchemy 2.0 ORM",
                "details": ["Normalized Relational Tables (Users, Transactions)", "Foreign Key Cascade Constraints", "ACID Compliance & Instant Querying"]
            }
        ]
    },

    # Slide 6: Technology Stack
    {
        "tag": "TECHNOLOGY STACK",
        "title": "Core Technology Stack",
        "type": "tech_stack",
        "domains": [
            {
                "title": "🐍 Backend Engine",
                "items": ["Python 3.10+ (Core Language)", "FastAPI (Async ASGI Framework)", "Uvicorn (Production Web Server)", "Pydantic v2 (Data Validation)"]
            },
            {
                "title": "🗄️ Database & ORM",
                "items": ["SQLite (Relational Database)", "SQLAlchemy 2.0 (Modern ORM)", "Foreign Key Cascading Rules", "Automated Schema Migrations"]
            },
            {
                "title": "🎨 Frontend & UI",
                "items": ["Modular Vanilla JavaScript (ES6+)", "CSS3 Custom Properties (Tokens)", "Chart.js (Interactive Charts)", "Zero NPM / Webpack Build Bloat"]
            },
            {
                "title": "🛡️ Security & Dev",
                "items": ["Passlib & Bcrypt (Password Hashing)", "python-jose (JWT Token Standards)", "Turborepo Monorepo Architecture", "Clean Architecture (<500 LOC/file)"]
            }
        ]
    },

    # Slide 7: Database Design
    {
        "tag": "DATABASE DESIGN",
        "title": "Relational Schema & Data Modeling",
        "type": "database",
        "users_table": [
            ("id", "INTEGER", "PK, Autoincrement"),
            ("username", "VARCHAR(50)", "Unique, Indexed"),
            ("email", "VARCHAR(100)", "Unique, Indexed"),
            ("full_name", "VARCHAR(100)", "User display name"),
            ("hashed_password", "VARCHAR(255)", "Bcrypt Salted Hash"),
            ("created_at", "TIMESTAMP", "Default UTC now")
        ],
        "transactions_table": [
            ("id", "INTEGER", "PK, Autoincrement"),
            ("user_id", "INTEGER", "FK -> users.id (CASCADE)"),
            ("type", "VARCHAR(10)", "'expense' | 'income'"),
            ("amount", "FLOAT", "Must be > 0.0"),
            ("category", "VARCHAR(50)", "Food, Travel, Bills, etc."),
            ("payment_mode", "VARCHAR(30)", "Default: 'UPI'"),
            ("date", "DATE", "Transaction Date"),
            ("description", "TEXT", "Optional memo/note")
        ]
    },

    # Slide 8: Smart Features
    {
        "tag": "KEY INNOVATIONS",
        "title": "Smart Features & User Experience",
        "type": "features",
        "features": [
            {
                "icon": "🤖",
                "name": "Intelligent Category Auto-Detect",
                "desc": "Real-time keyword dictionary maps typed text (e.g. 'burger', 'uber') directly to category badges without user clicks."
            },
            {
                "icon": "⚡",
                "name": "Sub-5-Second Fast Logging",
                "desc": "Payment mode is preset to UPI by default and descriptions are optional, enabling instant one-tap expense recording."
            },
            {
                "icon": "🔄",
                "name": "State Isolation Architecture",
                "desc": "Adding income never interferes with or resets expense form states, eliminating data cross-contamination."
            },
            {
                "icon": "📊",
                "name": "Real-Time Visual Cashflow",
                "desc": "Dynamic doughnut and monthly comparison bar charts update immediately after each transaction entry."
            }
        ]
    },

    # Slide 9: Implementation Details
    {
        "tag": "CODE ARCHITECTURE",
        "title": "Implementation & Engineering Design",
        "type": "implementation",
        "backend": [
            "Domain-Driven Folder Isolation: apps/api/domain/(auth, transactions).",
            "Pydantic Schema Guardians: Strict validation before touching database.",
            "Dependency Injection: FastAPI Depends(get_db) creates clean scoped sessions.",
            "Strict Line Limits: Every file strictly maintained under 500 lines of code."
        ],
        "frontend": [
            "Layered JavaScript: apps/web/public/js/ divided into services, views, components.",
            "Central API Wrapper: api.js automatically injects JWT Bearer header on every fetch.",
            "Dynamic Theme Engine: CSS variables allow seamless dark/light theme switching.",
            "Event-Driven Reactivity: Transaction events trigger automatic chart re-renders."
        ]
    },

    # Slide 10: Testing & QA
    {
        "tag": "VERIFICATION & QA",
        "title": "Testing, Validation & Quality Metrics",
        "type": "testing",
        "test_cases": [
            ("JWT Authentication", "Login with valid credentials returns 200 + token; invalid returns 401.", "PASS (100%)"),
            ("Expense Creation", "Creating expense stores in SQLite & returns valid JSON within 18ms.", "PASS (100%)"),
            ("Auto-Detection", "Tested 25 keywords across 8 categories; 100% correct pre-selection.", "PASS (100%)"),
            ("Cascade Delete", "Deleting a user removes all their associated transactions cleanly.", "PASS (100%)"),
            ("Form State Isolation", "Opening income modal after expense keeps all states completely separate.", "PASS (100%)")
        ],
        "stats": [
            ("⚡ 18 ms", "Average API Latency"),
            ("📦 < 150 KB", "Total Frontend Bundle"),
            ("🛡️ 0 Leakage", "Local SQLite Privacy")
        ]
    },

    # Slide 11: Conclusion & Roadmap
    {
        "tag": "CONCLUSION & FUTURE SCOPE",
        "title": "Project Achievements & Future Roadmap",
        "type": "conclusion",
        "achievements": [
            "Engineered a production-ready, full-stack personal finance web application.",
            "Achieved sub-5-second transaction logging with intelligent keyword auto-detection.",
            "Implemented enterprise Clean Architecture with strict < 500 LOC modularity.",
            "Eliminated third-party tracking, guaranteeing complete user financial privacy.",
            "Successfully hosted and running locally with zero maintenance or cloud fees."
        ],
        "roadmap": [
            "Cross-Platform Mobile App: Build lightweight mobile UI with React Native.",
            "Bank SMS Auto-Parsing: On-device parser to automatically read incoming UPI alerts.",
            "PDF/Excel Statement Export: Generate audited monthly expense reports.",
            "Predictive Spending AI: Local ML model predicting month-end budget burn."
        ]
    },

    # Slide 12: Acknowledgement
    {
        "tag": "CLOSING & ACKNOWLEDGEMENT",
        "title": "Acknowledgement & Discussion",
        "type": "closing"
    }
]
