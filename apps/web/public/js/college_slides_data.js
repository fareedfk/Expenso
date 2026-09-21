// College Slide Deck Data Model for Expenso (16 Slides)
// Strictly structured for modular rendering (< 500 LOC per file)

const COLLEGE_STUDENT_INFO = {
  name: "Fareed Khilji",
  roll: "23EA0CA030",
  course: "B.Tech — Computer Science & Engineering",
  college: "Arya Institute of Engineering Technology and Management (AIETM), Jaipur",
  year: "4th Year | Academic Year 2025–26",
  project: "Expenso — Personal Finance & Expense Tracker",
  submitted_to: "Dr. Sanjay Tiwari",
  designation: "(HOD, CSE Dept.)"
};

const COLLEGE_WEB_SLIDES = [
  {
    type: "cover",
    title: "Industrial Training Presentation",
    subtitle: "Expenso — Personal Finance & Expense Tracker"
  },
  {
    type: "two_column_cards",
    tag: "Executive Overview",
    title: "Project Overview & Core Concept",
    left: {
      title: "💡 What is Expenso?",
      stripe: "var(--primary-navy)",
      items: [
        "A full-stack, privacy-first personal finance web application.",
        "Engineered for sub-5-second daily expense and income logging.",
        "Interactive real-time analytics with Chart.js visualization.",
        "Self-hosted SQLite database with zero cloud data sharing."
      ]
    },
    right: {
      title: "🎯 Motivation & Need",
      stripe: "var(--accent-blue)",
      items: [
        "Existing apps require 5-6 clicks and rigid complex forms.",
        "Commercial apps read user SMS and monetize private habits.",
        "Heavy frontends cause sluggish performance on mobile devices.",
        "Expenso offers a clean, lightning-fast, zero-bloat solution."
      ]
    },
    pills: [
      { title: "⚡ < 5s Logging Speed", sub: "Zero-friction entry workflow" },
      { title: "🔒 100% Client Privacy", sub: "Local SQLite database storage" },
      { title: "📱 Zero NPM Overhead", sub: "Modular Vanilla JS & CSS3" }
    ]
  },
  {
    type: "two_column_cards",
    tag: "Problem Identification",
    title: "Problem Statement & Market Gaps",
    left: {
      title: "❌ Current Industry Problems",
      stripe: "var(--accent-red)",
      bg: "#FEF2F2",
      border: "#FCA5A5",
      items: [
        "<strong>Tedious Logging:</strong> 5+ steps to record a single cup of tea or snack.",
        "<strong>Privacy Invasions:</strong> Apps read private SMS messages and sell leads.",
        "<strong>Bloated Frameworks:</strong> 10MB+ bundle sizes slow on budget devices.",
        "<strong>Cluttered UI:</strong> Packed with unwanted ads, loan offers, and credit cards.",
        "<strong>High Abandonment:</strong> Over 80% of users quit tracking within 14 days."
      ]
    },
    right: {
      title: "✅ Expenso Solution",
      stripe: "var(--accent-green)",
      bg: "#F0FDF4",
      border: "#86EFAC",
      items: [
        "<strong>Sub-5s Rapid Entry:</strong> Default payment mode (UPI) & optional fields.",
        "<strong>Strict Privacy:</strong> Data stays in local SQLite; zero external trackers.",
        "<strong>Modular Vanilla JS:</strong> Instant load times under 150ms without bloat.",
        "<strong>Clean Minimal UI:</strong> Ad-free, focused dashboard with smooth themes.",
        "<strong>Intelligent Auto-Detect:</strong> Predicts categories from keywords automatically."
      ]
    }
  },
  {
    type: "grid_4",
    tag: "Goals & Objectives",
    title: "Objectives & Target Outcomes",
    cards: [
      { stripe: "var(--accent-blue)", title: "⚡ Zero Latency", desc: "Build an ultra-fast interface recording transactions in under 5 seconds with zero compilation lag." },
      { stripe: "var(--accent-green)", title: "🛡️ Privacy First", desc: "Keep 100% of financial data strictly on local device storage with zero third-party leakage." },
      { stripe: "var(--accent-purple)", title: "🧠 Smart Detection", desc: "Client-side keyword recognition mapping user notes to categories without manual dropdown searching." },
      { stripe: "var(--accent-gold)", title: "📊 Visual Insights", desc: "Dynamic income vs expense breakdown and category burn rates using interactive visual charts." }
    ]
  },
  {
    type: "tiers",
    tag: "System Design",
    title: "Three-Tier System Architecture",
    tiers: [
      {
        num: "Tier 1: Client Layer (Web)",
        sub: "Modular Vanilla JavaScript (ES6+)",
        bullets: ["Services: api.js, expenseService.js", "Views: expenseList, charts, modals", "Design Tokens: tokens.css, base.css"]
      },
      {
        num: "Tier 2: Application Layer (API)",
        sub: "FastAPI ASGI Server (Python 3.10+)",
        bullets: ["Domain Routers: /auth, /expenses, /income", "Pydantic v2 Request Validation", "Stateless JWT Auth & Bcrypt Security"]
      },
      {
        num: "Tier 3: Database Layer (Storage)",
        sub: "SQLite via SQLAlchemy 2.0 ORM",
        bullets: ["Normalized Relational Tables", "Foreign Key Cascade Constraints", "ACID Compliance & Instant Querying"]
      }
    ]
  },
  {
    type: "grid_4",
    tag: "Technology Stack",
    title: "Core Technology Stack Used",
    cards: [
      { stripe: "#3B82F6", title: "🐍 Backend Engine", list: ["Python 3.10+ (Core Language)", "FastAPI (Async ASGI Framework)", "Uvicorn (Production Server)", "Pydantic v2 (Data Validation)"] },
      { stripe: "#10B981", title: "🗄️ Database & ORM", list: ["SQLite (Relational Database)", "SQLAlchemy 2.0 (Modern ORM)", "Foreign Key Cascade Rules", "Base.metadata.create_all()"] },
      { stripe: "#8B5CF6", title: "🎨 Frontend & UI", list: ["Modular Vanilla JS (ES6+)", "CSS3 Custom Variables (Tokens)", "Chart.js (Interactive Charts)", "Zero Webpack/NPM Build Overhead"] },
      { stripe: "#F59E0B", title: "🛡️ Security & Dev", list: ["Passlib & Bcrypt (Password Hashing)", "python-jose (JWT Token Standards)", "Turborepo Monorepo Architecture", "Clean Code Standards (<500 LOC)"] }
    ]
  },
  {
    type: "database",
    tag: "Database Design",
    title: "Relational Schema & Data Modeling"
  },
  {
    type: "grid_4",
    tag: "Key Innovations",
    title: "Smart Features & User Experience",
    cards: [
      { stripe: "var(--accent-blue)", title: "🤖 Smart Auto-Detect", desc: "Real-time keyword dictionary maps typed text (e.g. 'burger', 'uber') directly to category badges." },
      { stripe: "var(--accent-green)", title: "⚡ Sub-5s Fast Logging", desc: "Payment mode preset to UPI by default and descriptions are optional for rapid one-tap entry." },
      { stripe: "var(--accent-purple)", title: "🔄 State Isolation", desc: "Adding income never interferes with or resets expense form states, preventing data leakage." },
      { stripe: "var(--accent-gold)", title: "📊 Real-Time Charts", desc: "Dynamic doughnut and monthly comparison bar charts update immediately after each transaction." }
    ]
  },

  // SLIDES 9 to 12: VISUAL SCREENSHOT WALKTHROUGHS
  {
    type: "screenshot",
    tag: "Live Demo • 1-Tap Quick Record",
    title: "Home Screen: Zero-Friction Expense Logger",
    img: "/static/screenshots/quick_record_ui.png",
    alt: "Quick Record Screen",
    accent: "#059669",
    bg: "#ECFDF5",
    border: "#A7F3D0",
    text_color: "#065F46",
    overview: "Designed for zero-effort habit tracking. Anyone can record daily expenses in under 2 seconds without navigating through complex sub-menus.",
    bullets: [
      "🟢 Big Green (+) Action: Centered for instant thumb reach; opens the entry popup in one single tap.",
      "💰 Live Balance Ticker: See your available balance (₹4,383) and today's total spending (₹3,851) at all times.",
      "⚡ Quick-Category Chips: One tap on Food (₹930) or Shopping (₹1,214) pre-fills your most frequent expenses.",
      "⌨️ Smart Natural Input (Ctrl+K): Type 'Add ₹250 for dinner' and AI detects the category automatically."
    ],
    tip: "No accounting knowledge needed. It works just like sending a quick chat message."
  },
  {
    type: "screenshot",
    tag: "Live Demo • Financial Dashboard",
    title: "Interactive Dashboard & Visual Analytics",
    img: "/static/screenshots/dashboard_ui.png",
    alt: "Financial Dashboard Screen",
    accent: "#2563EB",
    bg: "#EFF6FF",
    border: "#BFDBFE",
    text_color: "#1E40AF",
    overview: "Translates complex numbers into simple, colorful charts so beginners instantly know where their money went and how much they saved.",
    bullets: [
      "📊 4 Core Summary Cards: Clear numbers for Total Balance, Monthly Income, Monthly Expenses, and Savings.",
      "📈 Savings Rate (53.2%): Tells you in green if you are saving enough money this month.",
      "📉 Spending Overview Bar Chart: Compares cash coming in vs going out across months.",
      "🍩 Category Donut Chart: Shows exact percentage spent on Food, Transport, Shopping, and Health."
    ],
    tip: "You understand your complete monthly financial health in just 5 seconds."
  },
  {
    type: "screenshot",
    tag: "Live Demo • Financial Ledger",
    title: "Smart Ledger: Filterable Money Diary",
    img: "/static/screenshots/transactions_ui.png",
    alt: "Financial Transactions Ledger",
    accent: "#7C3AED",
    bg: "#F5F3FF",
    border: "#DDD6FE",
    text_color: "#5B21B6",
    overview: "An organized digital passbook where every rupee is tracked with clear color codes, instant search, and export capabilities.",
    bullets: [
      "🏷️ Color-Coded Badges: Green (+₹7,000) for Income and Red (-₹890) for Expenses — impossible to confuse.",
      "🔍 Instant Keyword Search: Find past spends like 'gym', 'movie', or 'groceries' in milliseconds.",
      "⚡ Category & Mode Filters: Filter by Payment Method (UPI, Cash) or Category with 1 click.",
      "📥 One-Click CSV Export: Download full transaction history to Excel for personal records or taxes."
    ],
    tip: "Never wonder where your cash disappeared at the end of the month."
  },
  {
    type: "screenshot",
    tag: "Live Demo • Category Budgets",
    title: "Budget Guardrails: Avoid Month-End Deficit",
    img: "/static/screenshots/budgets_ui.png",
    alt: "Category Budgets & Limits",
    accent: "#D97706",
    bg: "#FFFBEB",
    border: "#FDE68A",
    text_color: "#92400E",
    overview: "Set monthly spending limits for categories like Food and Shopping. Visual progress meters guide you before you overspend.",
    bullets: [
      "📊 Visual Progress Meters: Colored bars show percentage consumed (e.g., Shopping: 60.7%, Food: 46.5%).",
      "💵 Live Remaining Balances: Exact cash left displayed upfront (e.g. '₹1,070 remaining' for food).",
      "🛡️ Safe vs Danger Status: Clear 'NORMAL' green badge alerts you before a category limit is exceeded.",
      "⚙️ Flexible Custom Limits: Tap '+ Set New Budget' anytime to adjust limits as your lifestyle changes."
    ],
    tip: "Acts like a financial guardian, preventing impulse overspending before it happens."
  },

  // SLIDES 13 to 16: IMPLEMENTATION TO CLOSING
  {
    type: "two_column_cards",
    tag: "Code Architecture",
    title: "Implementation & Engineering Design",
    left: {
      title: "⚙️ FastAPI Backend Architecture",
      stripe: "var(--primary-navy)",
      items: [
        "<strong>Domain Isolation:</strong> apps/api/domain/(auth, transactions).",
        "<strong>Pydantic Schemas:</strong> Strict validation before database execution.",
        "<strong>Dependency Injection:</strong> Depends(get_db) creates clean scoped sessions.",
        "<strong>Strict Line Limits:</strong> Maintained under 500 lines of code per file."
      ]
    },
    right: {
      title: "💻 Frontend Modular Architecture",
      stripe: "var(--accent-green)",
      items: [
        "<strong>Layered JavaScript:</strong> apps/web/public/js/ (services, views, components).",
        "<strong>Central API Wrapper:</strong> api.js injects JWT Bearer header on every fetch.",
        "<strong>Dynamic Theme Engine:</strong> CSS variables allow seamless dark/light switching.",
        "<strong>Event-Driven Reactivity:</strong> Transaction events trigger auto chart re-renders."
      ]
    }
  },
  {
    type: "qa_testing",
    tag: "Verification & QA",
    title: "Testing, Validation & Quality Metrics",
    tests: [
      { name: "JWT Authentication", desc: "Login with valid credentials returns 200 + token; invalid returns 401.", status: "PASS (100%)" },
      { name: "Expense Creation", desc: "Creating expense stores in SQLite & returns valid JSON within 18ms.", status: "PASS (100%)" },
      { name: "Auto-Detection", desc: "Tested 25 keywords across 8 categories; 100% correct pre-selection.", status: "PASS (100%)" },
      { name: "Cascade Delete", desc: "Deleting a user removes all their associated transactions cleanly.", status: "PASS (100%)" },
      { name: "Form State Isolation", desc: "Opening income modal after expense keeps all states completely separate.", status: "PASS (100%)" }
    ],
    stats: [
      { val: "⚡ 18 ms", label: "Average API Latency" },
      { val: "📦 < 150 KB", label: "Total Frontend Bundle" },
      { val: "🛡️ 0 Leakage", label: "Local SQLite Privacy" }
    ]
  },
  {
    type: "two_column_cards",
    tag: "Summary & Roadmap",
    title: "Project Achievements & Future Roadmap",
    left: {
      title: "🏆 Key Project Accomplishments",
      stripe: "var(--primary-navy)",
      items: [
        "Engineered a production-ready, full-stack personal finance web application.",
        "Achieved sub-5-second transaction logging with intelligent keyword auto-detection.",
        "Implemented enterprise Clean Architecture with strict < 500 LOC modularity.",
        "Eliminated third-party tracking, guaranteeing complete user financial privacy.",
        "Successfully hosted and running locally with zero maintenance or cloud fees."
      ]
    },
    right: {
      title: "🚀 Future Development Roadmap",
      stripe: "var(--accent-gold)",
      items: [
        "<strong>Cross-Platform Mobile App:</strong> Build lightweight mobile UI with React Native.",
        "<strong>Bank SMS Auto-Parsing:</strong> On-device parser to automatically read incoming UPI alerts.",
        "<strong>PDF/Excel Statement Export:</strong> Generate audited monthly expense reports.",
        "<strong>Predictive Spending AI:</strong> Local ML model predicting month-end budget burn."
      ]
    }
  },
  {
    type: "closing",
    title: "Thank You!",
    subtitle: "Questions & Discussion (Q&A)"
  }
];
