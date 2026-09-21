# 🎓 Expenso — Complete Viva & Presentation Guide
**Candidate:** Fareed Khilji (`23EA0CA030`)  
**Department:** Computer Science & Engineering (AIETM, Jaipur)  
**Project:** Expenso — Modern Personal Finance & Expense Intelligence System  
**Presentation Deck:** `Expenso_Fareed_Khilji.pptx` (Neo-Brutalist Edition)

---

## ⚡ Quick Pitch (Starting Ke 30 Seconds Mein Kaise Start Karein)
> *"Good morning respected evaluators and teachers. My name is Fareed Khilji (Roll No. 23EA0CA030). Today I am presenting my final year project 'Expenso'. Expenso is a fast, privacy-first personal finance platform built with FastAPI, SQLite, and modern clean architecture designed to eliminate the friction and privacy invasions found in mainstream consumer finance apps."*

---

## 📋 Slide-by-Slide Explanation & Viva Strategy

### Slide 1: Cover Slide
* **Aapko kya bolna hai:**
  * Title: "Expenso — Modern Personal Finance & Expense Intelligence Platform".
  * Mention your guide: Dr. Sanjay Tiwari (HOD, CSE Dept., AIETM).
  * Highlight the core tags: FastAPI v0.111, SQLite Privacy, and Turborepo Monorepo.

### Slide 2: Project Overview & Core Mission
* **Key Points:**
  1. **Speed (< 5s):** Fast single-click transaction logging.
  2. **100% Privacy:** No third-party data tracking, self-hosted database.
  3. **Actionable Insights:** Live Chart.js analytics and budget threshold alerts.
* **Talking Sentence:** *"Existing apps require multiple screens just to log a daily ₹20 tea. Expenso reduces logging time to under 5 seconds with zero cloud data harvesting."*

### Slide 3: Problem Statement
* **Key Points:**
  1. **Friction:** 68% of users drop expense tracking within 2 weeks due to slow apps.
  2. **Privacy Abuse:** Free apps snoop SMS messages and sell credit profiles to third parties.
  3. **Bloat:** Heavy frameworks (>15MB JS bundles) lag on budget devices.

### Slide 4: Proposed Solution (Expenso Paradigm)
* **Key Points:**
  * Contrast Table: Conventional Fintech vs. Expenso.
  * Show how Expenso gives 100% data ownership back to the user without ads or SMS access.

### Slide 5: System Architecture & Monorepo
* **Key Points:**
  * **Frontend (apps/web):** Vanilla ES6 modules with CSS token layer (zero npm bloat).
  * **API (apps/api):** FastAPI asynchronous ASGI framework with Pydantic v2 schemas.
  * **Persistence:** Thread-safe SQLite relational database.
  * **Orchestration:** Monorepo managed with Turborepo (`turbo.json`).

### Slide 6: Database Design & Schema
* **Key Points:**
  * Core entities: `Users`, `Transactions`, `Budgets`.
  * Explain why SQLite: Zero-config, ACID-compliant, sub-2ms query speed, perfect for privacy-first single-tenant systems.

### Slide 7: Security Architecture & Authentication
* **Key Points:**
  * **Bcrypt:** Cryptographic salted hashing for passwords.
  * **JWT (HMAC-SHA256):** Stateless Bearer authorization header.
  * **CORS & Pydantic:** Automatic payload sanitization mitigating SQL Injection and XSS attacks.

### Slide 8: Functional Modules & UX
* **Key Points:**
  * Smart Transaction Logger (Income & Expense toggle).
  * Category spending charts & monthly burn rate graphs.
  * Dynamic budget alert meters (color shifts green -> yellow -> red at 80%).
  * One-click CSV statement export for tax auditing.

### Slide 9: Tech Stack & Rationale
* **Key Points:**
  * **FastAPI vs. Django:** FastAPI is asynchronous, 3x faster, with automatic Swagger docs.
  * **Vanilla JS vs. React:** Instant sub-100ms browser load time with 0KB compilation overhead.

### Slide 10: Engineering Standards & Clean Code
* **Key Points:**
  * **Strict LOC Rule (< 500 lines):** Every file is concise, modular, and easy to maintain.
  * **Feature Isolation:** Feature folders (`auth`, `transactions`, `budgets`) encapsulate their own schemas, models, and routes.

### Slide 11: Future Roadmap
* **Key Points:**
  * Phase 2: AI Receipt Scanner (Tesseract OCR + OpenCV).
  * Phase 2: Offline-first PWA with IndexedDB sync.
  * Phase 3: Roommate bill splitting (Min-cash-flow algorithm).

### Slide 12: Conclusion & Viva Defense
* **Closing Line:** *"In conclusion, Expenso combines modern backend performance with user privacy and clean software architecture. Thank you, I am now open for any questions and evaluation."*

---

## 🎯 Top 5 Viva Questions & Best Technical Answers

#### Q1: "Why did you use SQLite instead of MongoDB or PostgreSQL?"
> **Answer:** *"Sir, Expenso is engineered on a Privacy-First / Local-First paradigm. SQLite requires zero background server daemon, eliminates network latency (reads take < 2ms), provides full ACID compliance, and keeps 100% of user financial records contained on their local instance without cloud leakage."*

#### Q2: "How does JWT authentication work in your application?"
> **Answer:** *"When the user logs in, their password is verified against the Bcrypt salt in the database. Upon verification, the FastAPI backend signs a stateless token containing the `user_id` and expiry time using HMAC-SHA256 with a secret key. The frontend stores this token in session state and passes it as a `Bearer <token>` in the HTTP Authorization header for protected routes."*

#### Q3: "What prevents SQL Injection in your project?"
> **Answer:** *"We use Pydantic v2 schemas at the API boundary to strictly validate and cast all input data types. Furthermore, database queries use parameterized SQL / ORM bindings, meaning user inputs are treated strictly as data literals and never directly concatenated into executable SQL queries."*

#### Q4: "Why did you choose FastAPI over Flask or Django?"
> **Answer:** *"FastAPI is built on Starlette and Pydantic, running natively on the ASGI standard (Uvicorn). This allows asynchronous non-blocking I/O handling, which handles concurrent traffic much faster than WSGI-based Flask. Additionally, FastAPI generates interactive OpenAPI/Swagger documentation out of the box."*

#### Q5: "What is your Monorepo Turborepo structure?"
> **Answer:** *"Our monorepo splits concerns into `apps/api` (FastAPI backend) and `apps/web` (client app), managed by Turborepo with pipeline caching. This allows unified dependency management while maintaining strict feature isolation (< 500 LOC per file)."*
