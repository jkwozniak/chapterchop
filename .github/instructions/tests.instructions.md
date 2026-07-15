---
applyTo: "tests/**/*.py"
---

# Testing Overview

- The project uses pytest for unit testing.
- Production code is checked with strict static typing; tests are intentionally excluded from strict type checking.
- The test suite distinguishes between protocol contract tests and implementation-specific tests.
- Contract tests define the minimum behavior required by each protocol.
- Implementation tests verify implementation-specific semantics.
- Reusable testing infrastructure is separated from test cases.
- Test assets are stored separately from reusable Python testing utilities.
- Test assets are resolved through dedicated helpers rather than hardcoded paths.

# Testing design principles

- Extend both contract tests and implementation tests when adding new functionality.
- Keep protocol contract tests independent from implementation-specific tests.
- Contract tests should verify protocol guarantees rather than implementation details.
- Prefer deterministic tests.
- Keep test cases focused on a single behavior.
- Clearly document any intentionally untestable behavior.
- Prefer behavioral assertions over implementation details.
- Prefer simple stubs over complex mocking.
- Reuse existing test assets whenever possible before introducing new ones.
- Reuse existing stubs, fixtures and factories whenever practical.
- Prefer extending reusable test infrastructure over introducing one-off helpers.
- Keep reusable test support separate from test cases.
- New test support components should be placed in their designated directories.
- Test code should follow the same readability and maintainability standards as production code.
- Even though `tests` are exempt from strict static typing, still use typing where it improves clarity
