# Expenso — Engineering Rules & Operational Standards

All development and AI agent interactions within this codebase must strictly adhere to the following core rules:

## Rule 1: Strict Line Count Limit (< 500 LOC)
- **No file in the codebase may exceed 500 lines of code.**
- Aim for modular, concise files between 50 and 200 lines.
- If a file approaches 350-400 lines, proactively decompose it into domain submodules, service helpers, or discrete components.

## Rule 2: Feature Isolation & Single Responsibility
- **Always create any new feature in a new dedicated file.**
- Do not overload or append unrelated functionality to existing files.
- Each module, service, controller, and view must have a single, well-defined responsibility.

## Rule 3: Monorepo Turborepo Structure
- Maintain the official Turborepo monorepo architecture:
  - `apps/api`: FastAPI backend service.
  - `apps/web`: Modular client application.
  - `packages/*`: Shared packages and configs.
  - Root `package.json` with `workspaces` and `turbo.json` task pipelines.

## Rule 4: Advanced Clean / Domain-Driven Architecture
- **Backend**:
  - `core/`: Cross-cutting technical infrastructure (config, database, security, middleware).
  - `domain/<feature>/`: Feature isolation containing data models, validation schemas, business logic/services, and API routers.
- **Frontend**:
  - CSS decomposed into semantic layers: `tokens.css`, `base.css`, `components.css`, `modals.css`, `responsive.css`.
  - JS decomposed into layered architecture: `services/`, `components/`, `views/`, and a thin orchestrator `app.js`.
