When working on an issue:

1. Understand the task before modifying code.
2. Keep changes focused.
3. Do not perform unrelated refactoring.
4. Preserve project architecture.
5. Update tests together with production code.
6. Update documentation when required.
7. Do not introduce unnecessary dependencies.
8. Keep commits logically coherent.
9. Before introducing new domain models, file formats or protocols, check whether an existing project-specific solution already exists.

## Development Environment

- Poetry is the project's dependency and virtual environment manager.
- The project already has a configured Poetry-managed virtual environment.
- Never create a separate virtual environment for the project.
- Never install project dependencies globally.
- Run project commands inside the Poetry environment using `poetry run`.
- Prefer the project's existing Poetry environment over creating or activating another environment.

### Common Commands

- Run CLI commands with `poetry run chapterchop ...`.
- Run tests with `poetry run pytest`.
- Run linting with `poetry run ruff`.
- Run type checking with `poetry run mypy`.
- Run pre-commit checks with `poetry run pre-commit`.
