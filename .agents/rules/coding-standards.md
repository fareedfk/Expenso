---
description: Strict coding standards regarding line counts, feature isolation, and monorepo architecture
---

# Workspace Coding Standards

1. **Maximum File Size**: No file can have LOC > 500.
2. **Feature Addition**: Every new feature must be introduced via a new file/submodule.
3. **Monorepo Conventions**: All apps live in `apps/`, shared modules in `packages/`.
4. **Architecture**: Domain-driven separation with explicit interfaces and zero circular dependencies.
