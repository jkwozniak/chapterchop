# Production Code

## General

- Use modern Python 3.11 syntax.
- Follow PEP 8.
- Use strict static typing.
- Prefer explicit typing.
- Use absolute imports.
- Use pathlib.Path.
- Preserve exception context.

## API Design

- Provide docstrings.
- Keep naming consistent.
- Keep docstring structure consistent.
- Public APIs should remain explicit.

## Error Handling

- Use Chapterchop custom exceptions.
- Wrap backend exceptions.
- Use raise ... from ...
