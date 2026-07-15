# AI coding assistant instruction files

The Chapterchop project contains a set of instruction files intended for coding agents and AI assistants:
```
.github
├── AGENTS.md
├── copilot-instructions.md
└── instructions
    ├── docs.instructions.md
    ├── src.instructions.md
    └── tests.instructions.md
```
These files provide stable project context shared across AI-assisted development tools. Their purpose is to help coding assistants produce changes that remain consistent with the project's architecture, coding conventions, and long-term design goals.

Each of the above files has a different scope of responsibility:

- repository-wide instructions:
    * `AGENTS.md` - how AI agents should approach work in this repository
    * `copilot-instructions.md` - architectural principles and project-wide coding expectations
-  scope-specific instructions:
    * `src.instructions.md` - conventions for production code development
    * `tests.instructions.md` - conventions for writing and maintaining tests
    * `docs.instructions.md` - conventions for maintaining project documentation

`docs/architecture.md` complements the AI instruction files by providing a comprehensive description of the project's architecture, component contracts, and design decisions.

The above files should be treated as part of the project's maintained documentation.
Whenever architectural decisions, development conventions, or project philosophy change, the relevant instruction files should be updated accordingly.

The information contained in these files should not duplicate each other. Whenever possible, each design decision or development rule should be documented in exactly one place.

As the project evolves, additional instruction files may be introduced.
This document should be updated whenever the AI instruction structure changes.
