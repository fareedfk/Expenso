# Expenso Presentation Data Model (12 Comprehensive Slides)

SLIDES_DATA = [
    # Slide 1: Title
    {
        "tag": "COMPUTER SCIENCE & ENGINEERING • CAPSTONE PROJECT",
        "title": "Expenso: High-Speed Personal Finance Engine",
        "subtitle": "A Privacy-First, Zero-Latency Expense Tracker Built with Clean Architecture",
        "badge": "FINAL VIVA DEFENSE",
        "boxes": [
            {
                "title": "🎯 Project Vision & Core Problem",
                "color": "10B981",
                "lines": [
                    "Engineered to record daily expenses in under 5 seconds (< 5s benchmark).",
                    "Eliminates 6-step tedious friction found in commercial mobile trackers.",
                    "Zero Data Leakage: 100% self-hosted, user-isolated, and private.",
                    "Clean Monorepo Turborepo architecture strictly enforcing < 500 LOC per file."
                ]
            },
            {
                "title": "🛠️ Technology Stack Breakdown",
                "color": "3B82F6",
                "lines": [
                    "Backend: Python 3.10+, FastAPI (Asynchronous ASGI), Pydantic v2",
                    "Database: SQLite / RDBMS with SQLAlchemy ORM & Foreign Key Cascades",
                    "Security: Stateless JWT (HS256) & Passlib salted bcrypt password hashing",
                    "Frontend: Modular Vanilla JS (IIFE Services/Views), Semantic CSS Tokens, Chart.js"
                ]
            }
        ]
    },

    # Slide 2: Problem Statement
    {
        "tag": "INDUSTRY CONTEXT & MOTIVATION",
        "title": "Problem Statement: Why Modern Finance Apps Fail",
        "subtitle": "Analysis of existing commercial solutions and the friction users face daily",
        "badge": "GAP ANALYSIS",
        "boxes": [
            {
                "title": "1. Multi-Screen Friction",
                "color": "EF4444",
                "lines": [
                    "Logging a single cup of tea takes 5 to 6 screens and multiple dropdown clicks.",
                    "Users experience cognitive fatigue and abandon habit tracking within 14 days.",
                    "No intelligent auto-categorization based on contextual keywords."
                ]
            },
            {
                "title": "2. Invasive Data Harvesting",
                "color": "F59E0B",
                "lines": [
                    "Free apps read user SMS inboxes and sell spending patterns to ad brokers.",
                    "Financial data is monetized without transparent user consent.",
                    "Lack of self-hosted, confidential finance management alternatives."
                ]
            },
            {
                "title": "3. Excessive Framework Bloat",
                "color": "8B5CF6",
                "lines": [
                    "Heavy 15MB+ Single Page Application (SPA) bundles cause high memory pressure.",
                    "Slow startup latency on budget mobile devices and spotty network connections.",
                    "Complex compilation toolchains make maintenance difficult."
                ]
            }
        ]
    },

    # Slide 3: Proposed Solution
    {
        "tag": "SOLUTION ARCHITECTURE",
        "title": "Expenso: Minimum Clicks, Maximum Clarity",
        "subtitle": "Key engineering innovations designed to make expense tracking effortless",
        "badge": "CORE INNOVATIONS",
        "boxes": [
            {
                "title": "⚡ Smart Keyword Recognition",
                "color": "10B981",
                "lines": [
                    "User types 'Pizza 250' -> Auto-detects & selects 'Food & Dining'.",
                    "User types 'Uber 180' -> Auto-detects & selects 'Transport'.",
                    "Zero manual searching through exhaustive category dropdowns."
                ]
            },
            {
                "title": "🛡️ Isolated Transaction Engine",
                "color": "3B82F6",
                "lines": [
                    "Complete state separation between Expense and Income modes.",
                    "Optional Description for expenses; simplified Amount+Category for income.",
                    "Default UPI payment mode with automatic zero-click fallback."
                ]
            },
            {
                "title": "⌨️ Power-User Navigation",
                "color": "8B5CF6",
                "lines": [
                    "Ctrl+K: Instant Command Palette for rapid keyboard logging.",
                    "E: Quick Expense Modal | I: Quick Income Modal | /: Ledger Search.",
                    "Esc: Dismiss active overlays with zero mouse interaction."
                ]
            }
        ]
    },

    # Slide 4: System Architecture
    {
        "tag": "MONOREPO & SOFTWARE DESIGN",
        "title": "Clean Monorepo Architecture & Standards",
        "subtitle": "Strict domain isolation, maintainability, and clean code enforcement",
        "badge": "ENTERPRISE PATTERNS",
        "boxes": [
            {
                "title": "📁 Monorepo Layout (Turborepo)",
                "color": "3B82F6",
                "lines": [
                    "apps/api: Asynchronous FastAPI service divided into clean domain modules.",
                    "apps/api/core: Cross-cutting database engines, security, and middleware.",
                    "apps/api/domain: Feature slices (auth, transactions, budgets, analytics, recurring).",
                    "apps/web: Zero-framework client with layered services, components, and views."
                ]
            },
            {
                "title": "📏 Strict < 500 LOC Engineering Rule",
                "color": "10B981",
                "lines": [
                    "Core Project Constraint: No file in the codebase may exceed 500 lines of code.",
                    "Forces high modularity, atomic responsibilities, and easy unit testability.",
                    "Proactive decomposition whenever a file approaches 350 lines."
                ]
            }
        ]
    },

    # Slide 5: Database Schema
    {
        "tag": "RELATIONAL DATA MODELING",
        "title": "Database Schema & Entity Relationships",
        "subtitle": "Normalized relational design with foreign keys and cascading integrity",
        "badge": "RDBMS SCHEMA",
        "boxes": [
            {
                "title": "🗄️ Core Relational Entities",
                "color": "8B5CF6",
                "lines": [
                    "users: (id, name, email, password_hash, currency, created_at)",
                    "transactions: (id, user_id, amount, type, description, category_id, date, notes)",
                    "categories: (id, user_id, name, type, icon, color, is_default)",
                    "payment_methods: (id, user_id, name, type)",
                    "budgets: (id, user_id, category_id, amount, month, year)",
                    "recurring_expenses: (id, user_id, name, amount, frequency, next_date)"
                ]
            },
            {
                "title": "🛡️ Referential Integrity & Indexing",
                "color": "10B981",
                "lines": [
                    "Foreign Keys with ON DELETE CASCADE: Clean deletion without orphaned records.",
                    "Indexed Queries: B-tree indexes on (user_id, transaction_date) for fast ranges.",
                    "SQLAlchemy Eager Loading: joinedload eliminates N+1 query bottlenecks."
                ]
            }
        ]
    },

    # Slide 6: Backend & Security
    {
        "tag": "BACKEND SERVICES & API SECURITY",
        "title": "FastAPI Implementation & Defense-in-Depth",
        "subtitle": "Asynchronous REST endpoints, cryptographic security, and token verification",
        "badge": "REST API & AUTH",
        "boxes": [
            {
                "title": "🔐 Cryptographic Authentication",
                "color": "10B981",
                "lines": [
                    "Passlib bcrypt: Passwords hashed with unique random salt rounds before storage.",
                    "Stateless JWT Tokens: Signed with HS256 algorithm, payload contains user ID.",
                    "FastAPI Dependency Injection: Depends(get_current_user_id) guards private routes.",
                    "Profile Management: Direct endpoints for name, currency, and password updates."
                ]
            },
            {
                "title": "🛡️ API Defense & Validation",
                "color": "EF4444",
                "lines": [
                    "SQL Injection Immunity: Parameterized queries generated via SQLAlchemy ORM.",
                    "Pydantic Validation: Enforces strict data types, positive amounts, and email formats.",
                    "Cross-User Isolation: Every database query enforces WHERE user_id == current_user."
                ]
            }
        ]
    },

    # Slide 7: Frontend Architecture
    {
        "tag": "CLIENT-SIDE ENGINEERING",
        "title": "Semantic CSS & Layered JavaScript Architecture",
        "subtitle": "High-aesthetic glassmorphism and instant performance without virtual DOM overhead",
        "badge": "NATIVE WEB STACK",
        "boxes": [
            {
                "title": "🎨 Semantic CSS Layering",
                "color": "3B82F6",
                "lines": [
                    "tokens.css: HSL design tokens, elevation shadows, border radii, and accent colors.",
                    "base.css: Grid layouts, sticky topbar with blur filter, and sidebar navigation.",
                    "components.css: Glassmorphic cards, responsive tables, badge pills, metric items.",
                    "Dynamic Theme Engine: Instant Dark/Light mode toggle persisted in localStorage."
                ]
            },
            {
                "title": "📦 Modular JavaScript Layers",
                "color": "8B5CF6",
                "lines": [
                    "services/api.js: Centralized HTTP client with automatic Authorization header.",
                    "services/state.js: Single source of truth for user state, currency, and timezone.",
                    "views/: Decoupled controllers for Home, Dashboard, Ledger, Calendar, and Settings.",
                    "components/profile.js: Interactive floating account dropdown with edit modal."
                ]
            }
        ]
    },

    # Slide 8: Smart Transaction Logger
    {
        "tag": "CORE ENGINE SPOTLIGHT",
        "title": "Smart Transaction Engine & Keyword Detection",
        "subtitle": "Real-time client-side keyword parsing for zero-friction transaction entry",
        "badge": "INTELLIGENT UX",
        "boxes": [
            {
                "title": "🧠 Contextual Keyword Mapping",
                "color": "10B981",
                "lines": [
                    "Food Keywords: 'pizza', 'burger', 'chai', 'lunch', 'zomato' -> Food & Dining 🍔",
                    "Transport Keywords: 'uber', 'ola', 'auto', 'petrol', 'metro' -> Transport 🚕",
                    "Shopping Keywords: 'amazon', 'blinkit', 'clothes', 'grocery' -> Shopping 🛒",
                    "Bills Keywords: 'bijli', 'wifi', 'electricity', 'recharge' -> Bills & Utilities 💡"
                ]
            },
            {
                "title": "⚡ Streamlined Entry Rules",
                "color": "3B82F6",
                "lines": [
                    "Optional Description: Expense logs with just Amount + Category if user is in a hurry.",
                    "Add Income Isolation: Description field hidden to prevent carryover of expense text.",
                    "Default UPI: Modal opens with UPI pre-selected, auto-fallback on submission.",
                    "Instant Undo Toast: Deleted transactions can be restored within a 5-second window."
                ]
            }
        ]
    },

    # Slide 9: Analytics & Live Sync
    {
        "tag": "DATA VISUALIZATION & TIMEZONE SYNC",
        "title": "Visual Intelligence & Live IST Clock",
        "subtitle": "Translating raw ledger data into actionable personal financial insights",
        "badge": "CHART.JS ENGINE",
        "boxes": [
            {
                "title": "📊 Interactive Chart.js Dashboards",
                "color": "8B5CF6",
                "lines": [
                    "Monthly Trend Line Chart: 6-month historical cashflow comparing Inflow vs Outflow.",
                    "Category Breakdown Doughnut: Visual percentage distribution of monthly expenses.",
                    "Live Metric Cards: Net Balance, Monthly Income, Monthly Burn, and Savings Rate.",
                    "Formula: Savings Rate = ((Monthly Income - Monthly Expense) / Monthly Income) * 100."
                ]
            },
            {
                "title": "🕒 Live IST Timezone Synchronization",
                "color": "10B981",
                "lines": [
                    "Indian Standard Time (IST) Clock: Live ticker on dashboard updated every 10 seconds.",
                    "Contextual Greetings: Good morning (🌅), afternoon (☀️), evening (🌆), or night (🌙).",
                    "Timezone-Safe Date Utility: Uses Intl.DateTimeFormat with Asia/Kolkata timezone."
                ]
            }
        ]
    },

    # Slide 10: Budgets & Automation
    {
        "tag": "FINANCIAL PLANNING & AUTOMATION",
        "title": "Budgets, Recurring Bills & Interactive Calendar",
        "subtitle": "Active spending guardrails, automated renewals, and date-wise ledger",
        "badge": "ACTIVE CONTROLS",
        "boxes": [
            {
                "title": "🎯 Category Spend Caps",
                "color": "F59E0B",
                "lines": [
                    "Set monthly spending limits for high-burn categories (e.g. Dining ₹5,000).",
                    "Progress bar visual status: Normal (Green) -> Warning (Amber) -> Exceeded (Red).",
                    "Live percentage calculation prevents surprise month-end overspending."
                ]
            },
            {
                "title": "🔄 Automated Recurring Subscriptions",
                "color": "3B82F6",
                "lines": [
                    "Tracks recurring liabilities (Netflix, Gym, Rent, Internet).",
                    "Automated endpoint /api/recurring/process-due posts due bills on cycle dates.",
                    "Maintains active subscriptions list with next due dates."
                ]
            },
            {
                "title": "📅 Day-by-Day Interactive Calendar",
                "color": "8B5CF6",
                "lines": [
                    "Monthly calendar grid aggregating daily expenditure totals on each date cell.",
                    "Click any calendar cell to filter and review that specific day's financial activity."
                ]
            }
        ]
    },

    # Slide 11: Verification & Benchmarks
    {
        "tag": "SYSTEM VALIDATION & BENCHMARKS",
        "title": "Performance Metrics & Testing Standards",
        "subtitle": "Rigorous performance profiling and test coverage across the full stack",
        "badge": "QA & BENCHMARKS",
        "boxes": [
            {
                "title": "🚀 Performance Profiling",
                "color": "10B981",
                "lines": [
                    "Sub-50ms API Latency: FastAPI ASGI server handles high concurrent throughput.",
                    "Client Load Time: < 60ms initial page load due to zero framework bundle overhead.",
                    "Server-Side Pagination: Transactions endpoint limits payloads (50 items/page).",
                    "Database Queries: EXPLAIN QUERY PLAN confirms index utilization on transaction queries."
                ]
            },
            {
                "title": "🧪 Test Coverage & Verification",
                "color": "3B82F6",
                "lines": [
                    "Authentication Edge Cases: Verified rejection of expired and tampered JWT tokens.",
                    "Data Boundary Tests: Verified handling of zero amounts, empty notes, and long strings.",
                    "Cross-Browser Compatibility: Validated in Chromium, Firefox, and Safari rendering engines."
                ]
            }
        ]
    },

    # Slide 12: Conclusion & Roadmap
    {
        "tag": "SUMMARY & FUTURE SCOPE",
        "title": "Conclusion, Learnings & Commercial Roadmap",
        "subtitle": "Reflection on engineering achievements and commercial expansion vision",
        "badge": "PROJECT DEFENSE",
        "boxes": [
            {
                "title": "🎓 Academic & Engineering Learnings",
                "color": "10B981",
                "lines": [
                    "Full-Stack Mastery: Seamless coordination between FastAPI, SQLAlchemy, and DOM APIs.",
                    "Security Best Practices: Implemented real-world token-based auth, hashing, and defense.",
                    "Clean Code Discipline: Successfully kept entire monorepo compliant with < 500 LOC rule."
                ]
            },
            {
                "title": "🔮 Future Scope & Commercial Expansion",
                "color": "8B5CF6",
                "lines": [
                    "AI Receipt OCR: Camera bill scanning with automatic optical character recognition.",
                    "Android Background SMS Sync: Auto-capturing banking transaction SMS alerts.",
                    "Splitwise Group Splitting: Automated shared expense calculation with roommates."
                ]
            }
        ]
    }
]
