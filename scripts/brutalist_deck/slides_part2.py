# Slides 7 to 12: Security, Features, Tech Stack, Standards, Roadmap, Conclusion
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from scripts.brutalist_deck.theme import (
    SLIDE_WIDTH, SLIDE_HEIGHT, apply_slide_background, create_header,
    add_badge, add_neo_card, add_footer_brand,
    C_BG, C_BORDER, C_TEXT_DARK, C_TEXT_MUTED, C_WHITE,
    C_YELLOW, C_YELLOW_BG, C_GREEN, C_GREEN_BG, C_INDIGO, C_INDIGO_BG,
    C_RED, C_RED_BG, C_CYAN, C_CYAN_BG, FONT_HEADING, FONT_BODY, FONT_MONO
)

def make_slide_7(prs):
    """Slide 7: Security Architecture & Authentication."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "06 // SECURITY & AUTH", "Cryptographic Security & Defense-in-Depth",
                  "Multi-layer protection safeguarding user credentials and sensitive transaction data.", 7)

    c1 = ["Industry-standard salted password hashing via Passlib/Bcrypt.",
          "Plaintext passwords never logged, saved, or transmitted.",
          "Adaptive work factor prevents brute-force rainbow table attacks."]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Bcrypt Cryptography", c1, "PASSWORD SECURITY", C_INDIGO, C_WHITE, "🔐")

    c2 = ["Cryptographically signed tokens using HMAC-SHA256 (HS256).",
          "Stateless authorization: no memory overhead on backend servers.",
          "Carried securely in HTTP Authorization headers (Bearer <token>)."]
    add_neo_card(slide, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "JWT Access Tokens", c2, "STATELESS SESSIONS", C_GREEN, C_WHITE, "🛡️")

    c3 = ["Pydantic v2 schemas sanitize every incoming payload automatically.",
          "SQL injection mitigated entirely via parameterized queries.",
          "Configurable CORS middleware restricts unauthorized cross-origin requests."]
    add_neo_card(slide, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Input Sanitization & CORS", c3, "PAYLOAD DEFENSE", C_YELLOW, C_WHITE, "🚦")

    add_footer_brand(slide)
    return slide

def make_slide_8(prs):
    """Slide 8: Core Functional Modules."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "07 // FUNCTIONAL MODULES", "Core Platform Capabilities & User Experience",
                  "Essential features designed for daily speed and financial clarity.", 8)

    c1 = ["Fast toggle between Income and Expense modes.",
          "Preset and custom category badges (Food, Transit, Bills).",
          "One-click submission with instant local UI cache update."]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
                 "Smart Transaction Logger", c1, "DAILY USABILITY", C_INDIGO, C_WHITE, "⚡")

    c2 = ["Dynamic donut chart visualizing category spending ratios.",
          "Weekly burn-rate comparison bar graphs using Chart.js.",
          "Zero lag or layout shifts during live data re-renders."]
    add_neo_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(2.3),
                 "Visual Analytics Dashboard", c2, "DATA INTELLIGENCE", C_CYAN, C_WHITE, "📈")

    c3 = ["Monthly category caps (e.g. Max ₹5,000 for Dining).",
          "Progress bars dynamically color shift: Green -> Yellow -> Red.",
          "Instant warning toasts triggered upon crossing 80% ceiling."]
    add_neo_card(slide, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.3),
                 "Dynamic Budget Alerts", c3, "FINANCIAL DISCIPLINE", C_YELLOW, C_WHITE, "🎯")

    c4 = ["Export full historical ledger into CSV spreadsheet format.",
          "Compatible with Excel, Google Sheets, and tax filing software.",
          "Complete data portability ensures zero platform lock-in."]
    add_neo_card(slide, Inches(6.9), Inches(4.35), Inches(5.6), Inches(2.3),
                 "Statement Export & Portability", c4, "AUDITING & BACKUP", C_GREEN, C_WHITE, "📁")

    add_footer_brand(slide)
    return slide

def make_slide_9(prs):
    """Slide 9: Tech Stack & Architecture Decisions."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "08 // TECH STACK", "Technical Stack & Architectural Tradeoffs",
                  "Deliberate technology choices made for performance, maintainability, and privacy.", 9)

    c1 = ["FastAPI (Python 3.11+): ASGI asynchronous execution.",
          "Why not Django/Flask? FastAPI is 300% faster with native async and auto OpenAPI docs.",
          "Pydantic v2: C-compiled validation engine for maximum serialization speed."]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Backend Engine", c1, "PYTHON FASTAPI", C_INDIGO, C_WHITE, "🐍")

    c2 = ["SQLite 3: Zero-config serverless relational storage.",
          "Why not PostgreSQL? Eliminates external DB daemon overhead, ideal for single-tenant local privacy.",
          "Sub-2ms transaction commit latency on standard consumer SSDs."]
    add_neo_card(slide, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Storage & Database", c2, "SQLITE 3", C_GREEN, C_WHITE, "💾")

    c3 = ["Modern Vanilla ES6 JS & Modular CSS.",
          "Why not React/Next.js? Zero compilation overhead, 0 npm vulnerabilities, loads in < 100ms.",
          "Chart.js: Lightweight canvas rendering for smooth charts."]
    add_neo_card(slide, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Client Frontend", c3, "VANILLA JS / CSS", C_YELLOW, C_WHITE, "🌐")

    add_footer_brand(slide)
    return slide

def make_slide_10(prs):
    """Slide 10: Engineering Standards & Monorepo Governance."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "09 // CODE QUALITY", "Engineering Standards & Monorepo Governance",
                  "Enforcing rigorous clean code architecture and maintainable software patterns.", 10)

    c1 = ["Strict rule: No file in the codebase exceeds 500 lines.",
          "Modules kept between 80–220 LOC for maximum readability.",
          "Prevents giant spaghetti files and simplifies peer code reviews."]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Strict Line Count Limits", c1, "RULE: < 500 LOC", C_RED, C_WHITE, "📏")

    c2 = ["Monorepo orchestrated with Turborepo (turbo.json).",
          "apps/api: Pure Python REST API service.",
          "apps/web: Standalone client application with decoupled state/.",
          "Parallel build, test, and lint pipelines."]
    add_neo_card(slide, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Turborepo Monorepo", c2, "MONOREPO STRUCTURE", C_INDIGO, C_WHITE, "📦")

    c3 = ["Core / Domain separation ensures zero tight coupling.",
          "Business logic isolated from route controller handlers.",
          "Automated schema testing and deterministic error responses."]
    add_neo_card(slide, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Domain-Driven Design", c3, "CLEAN ARCHITECTURE", C_GREEN, C_WHITE, "🏗️")

    add_footer_brand(slide)
    return slide

def make_slide_11(prs):
    """Slide 11: Future Roadmap & Enhancements."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "10 // FUTURE ROADMAP", "Future Scope & Technology Evolution",
                  "Planned features for Phase 2 and commercial scalability roadmap.", 11)

    c1 = ["Mobile camera receipt scanning using Tesseract OCR & OpenCV.",
          "Machine learning categorization: Auto-tags Merchant & Tax.",
          "Reduces logging time down to 1 second via photo capture."]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "AI Receipt OCR Scanner", c1, "PHASE 2 (MACHINE LEARNING)", C_CYAN, C_WHITE, "📷")

    c2 = ["Service Worker integration for complete offline functionality.",
          "Client-side IndexedDB caching with background sync queue.",
          "Installable on Android, iOS, and Desktop as a native app."]
    add_neo_card(slide, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Progressive Web App (PWA)", c2, "PHASE 2 (OFFLINE-FIRST)", C_INDIGO, C_WHITE, "📱")

    c3 = ["Group expense splitting for college roommates and trips.",
          "Automated debt settlement calculations (Min-cash-flow algorithm).",
          "Multi-currency conversion support for international travel."]
    add_neo_card(slide, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
                 "Bill Splitting & FX", c3, "PHASE 3 (COLLABORATIVE)", C_GREEN, C_WHITE, "👥")

    add_footer_brand(slide)
    return slide

def make_slide_12(prs):
    """Slide 12: Conclusion & Viva Evaluation."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    create_header(slide, "11 // CONCLUSION", "Project Conclusion & Technical Evaluation",
                  "Final summary of deliverables, learning outcomes, and viva defense.", 12)

    # 2 Key Summary Cards
    c_learnings = [
        "Mastered production FastAPI ASGI architecture and asynchronous endpoints.",
        "Implemented secure Bcrypt hashing & stateless JWT token lifecycle.",
        "Built modular Vanilla JS architecture without relying on heavy npm dependencies.",
        "Applied Clean Code standards and strict < 500 LOC modularization across monorepo."
    ]
    add_neo_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.4),
                 "Key Engineering Learnings", c_learnings, "PROJECT TAKEAWAYS", C_INDIGO, C_WHITE, "🎓")

    c_summary = [
        "Expenso successfully addresses modern financial privacy and logging friction.",
        "Delivers sub-50ms API responses and sub-5-second entry workflow.",
        "Complete source code adheres to Turborepo monorepo standards.",
        "Ready for immediate local deployment and student use."
    ]
    add_neo_card(slide, Inches(6.9), Inches(1.8), Inches(5.6), Inches(3.4),
                 "Production Readiness", c_summary, "FINAL VERDICT", C_GREEN, C_WHITE, "🚀")

    # Big Final Thank You / Viva Q&A Card
    q_items = [
        "Fareed Khilji  |  Roll No: 23EA0CA030  |  B.Tech CSE, 4th Year",
        "Project: Expenso  |  College: AIETM, Jaipur  |  Guide: Dr. Sanjay Tiwari (HOD, CSE)"
    ]
    add_neo_card(slide, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.4),
                 "Thank You! Open for Viva Evaluation & Questions", q_items, "VIVA DEFENSE", C_YELLOW, C_WHITE, "💬")

    add_footer_brand(slide)
    return slide
