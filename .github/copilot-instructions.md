# Project facts

## Project Overview

- The project is called Chapterchop.
- Chapterchop splits audio recordings into logical chapters.
- Chapterchop is an offline audio processing library and application.
- Chapterchop operates exclusively on already available local audio data.
- Chapterchop does not download, stream, or discover audio content.
- The source code is hosted on GitHub.
- The project is distributed as a Python package on PyPI.
- The project requires Python 3.11 or newer.
- Production code is statically typed.
- FFmpeg is the only external system dependency.

## Project Scope

- Chapterchop never modifies source audio files.
- Audio processing always produces new outputs.

## Architecture Overview

- The project follows a protocol-first architecture.
- The architecture is modular and composable.
- Audio processing follows the AudioData → Analyzer → Cutter → Writer pipeline.
- Some analyzers may consume additional domain-specific input besides AudioData.
- The processing pipeline is explicit and deterministic.
- Each pipeline stage has a single well-defined responsibility.
- Domain models remain independent from backend-specific implementations.
- Components communicate through protocol-based abstractions and immutable domain models.
- Protocols specify structural compatibility and minimum functional requirements.
- Components validate their inputs at architectural boundaries.
- Protocol compatibility does not imply behavioral compatibility.
- Reference implementations are expected to form one fully compatible deterministic pipeline.
- The project may define its own domain-specific data models and file formats. Their specifications are documented under the `docs/` directory.

## Core Domain Model

Audio processing:

- AudioData abstracts backend-specific audio storage.
- Chapter represents a logical audio range.
- Segment binds audio data with chapter metadata.

External chapter definitions:

- ChapterEntry represents a single externally defined chapter boundary.
- ChapterList represents an immutable collection of chapter definitions.

## Error Model

- The project exposes a stable hierarchy of custom exceptions.
- Public APIs should raise Chapterchop exceptions rather than backend-specific exceptions.


# Design philosophy

## General principles

- Maintain high quality and clean modern Python code.
- Keep changes focused on the requested task.
- Avoid unrelated refactoring.
- Preserve backward compatibility unless the task explicitly requires a breaking change.
- Prefer explicit APIs over implicit behavior.
- Avoid hidden orchestration.
- Prefer simple solutions over unnecessary abstraction.
- Prefer readability over cleverness.
- Explicit is better than implicit.
- Simple is better than complex.

## Architectural principles

- Prefer protocols over ABC class inheritance.
- Prefer composition over inheritance.
- Keep components focused on a single responsibility.
- Keep responsibilities explicit.
- Keep components deterministic.
- Validate data at component boundaries.
- Treat processing components as conceptually immutable.
- Prefer creating new objects over mutating existing ones.
- Preserve clear boundaries between pipeline components.

## Long-term evolution

- Keep public APIs explicit and stable.
- Do not move responsibilities between pipeline components without architectural justification.
- Prefer extending existing domain models and abstractions over introducing parallel concepts.
- Prefer the standard library whenever practical.
- Avoid unnecessary third-party dependencies.
