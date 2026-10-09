# Project facts

## Project Overview

* The project is called Chapterchop.

* Chapterchop splits audio recordings into logical chapters.

* Chapterchop is an offline audio processing library and application.

* Chapterchop operates exclusively on already available local audio data.

* Chapterchop does not download, stream, or discover audio content.

* The source code is hosted on GitHub.

* The project is distributed as a Python package on PyPI.

* The project requires Python 3.11 or newer.

* Production code is statically typed.

* FFmpeg is the only external system dependency.

## Project Scope

* Chapterchop never modifies source audio files.

* Audio processing always produces new outputs.

## Architecture Overview

* The architecture is modular, composable, and protocol-first where an abstraction is required.

* Audio processing follows the core AudioData → Analyzer → Cutter → Writer pipeline.

* An Analyzer may consume AudioData together with additional domain-specific input.

* `EvenSplitAnalyzer` consumes AudioData and determines equally sized chapter boundaries.

* `ChapterListAnalyzer` consumes AudioData together with a ChapterList containing externally defined chapter information.

* `PydubAudioData` and `ClfParser` provide independent inputs to the CLF-based chaptering workflow.

* In the CLF-based workflow, PydubAudioData does not provide input to ClfParser. Their outputs are combined by ChapterListAnalyzer.

* The processing pipeline is explicit and deterministic.

* Each pipeline stage has a single well-defined responsibility.

* Domain models remain independent from backend-specific implementations.

* Components communicate through protocol-based abstractions and immutable domain models where appropriate.

* Not every concrete component requires a protocol or abstract contract.

* Protocols specify structural compatibility and minimum functional requirements.

* Protocol compatibility does not imply behavioral compatibility.

* Components validate their inputs at architectural boundaries.

* Reference implementations are expected to form one fully compatible deterministic pipeline.

* The project may define its own domain-specific data models and file formats. Their specifications are documented under the `docs/` directory.

## Processing Components

### AudioData

* AudioData abstracts backend-specific audio storage.

* `PydubAudioData` is the current AudioData implementation.

### Analyzer

* Analyzer determines logical audio chapter boundaries.

* `EvenSplitAnalyzer` is an Analyzer implementation that creates equally sized chapters.

* `ChapterListAnalyzer` is an Analyzer implementation that creates chapters using externally supplied chapter definitions represented by ChapterList.

### Cutter

* Cutter converts chapter definitions into audio segments.

* `SimpleCutter` is the current Cutter implementation.

### Writer

* Writer persists generated audio segments.

* `DirectoryWriter` is the current Writer implementation.

### CLF parsing

* `ClfParser` parses CLF input into a ChapterList.

* `ClfParser` is a concrete component and intentionally does not currently require its own protocol or abstract contract.

* CLF parsing is independent from audio loading and audio processing.

## Core Domain Model

### Audio processing

* AudioData abstracts backend-specific audio storage.

* Chapter represents a logical audio range.

* Segment binds audio data with chapter metadata.

### External chapter definitions

* ChapterEntry represents a single externally defined chapter definition.

* ChapterList represents an immutable collection of externally defined chapter definitions.

* ChapterEntry and ChapterList represent input to chapter analysis and are distinct from the Chapter objects produced for the audio processing workflow.

## Workflow Composition

### Standard workflow

The standard workflow uses equal-size chapter analysis:

```text
PydubAudioData
    ↓
EvenSplitAnalyzer
    ↓
SimpleCutter
    ↓
DirectoryWriter
```

### CLF-based workflow

The CLF-based workflow combines two independent inputs:

```text
PydubAudioData ──┐
                 ├──> ChapterListAnalyzer ──> SimpleCutter ──> DirectoryWriter
ClfParser ───────┘
```

* PydubAudioData and ClfParser are independent inputs to ChapterListAnalyzer.

* PydubAudioData does not provide input to ClfParser.

* ClfParser does not load or process audio data.

* ChapterListAnalyzer combines the relevant audio and chapter-definition information to produce chapters for downstream processing.

## Error Model

* The project exposes a stable hierarchy of custom exceptions.

* Public APIs should raise Chapterchop exceptions rather than backend-specific exceptions.

# Design philosophy

## General principles

* Maintain high quality and clean modern Python code.

* Keep changes focused on the requested task.

* Avoid unrelated refactoring.

* Preserve backward compatibility unless the task explicitly requires a breaking change.

* Prefer explicit APIs over implicit behavior.

* Avoid hidden orchestration.

* Prefer simple solutions over unnecessary abstraction.

* Prefer readability over cleverness.

* Explicit is better than implicit.

* Simple is better than complex.

## Architectural principles

* Prefer protocols over ABC class inheritance when an abstraction is required.

* Do not introduce protocols or abstract contracts solely for architectural symmetry.

* Prefer composition over inheritance.

* Keep components focused on a single responsibility.

* Keep responsibilities explicit.

* Keep components deterministic.

* Validate data at component boundaries.

* Treat processing components as conceptually immutable.

* Prefer creating new objects over mutating existing ones.

* Preserve clear boundaries between pipeline components.

* Reuse existing pipeline components when composing new workflows.

* Do not duplicate downstream processing logic when an existing component can fulfill the responsibility.

## Long-term evolution

* Keep public APIs explicit and stable.

* Do not move responsibilities between pipeline components without architectural justification.

* Prefer extending existing domain models and abstractions over introducing parallel concepts.

* Introduce new abstractions only when required by current or clearly foreseeable use cases.

* Prefer the standard library whenever practical.

* Avoid unnecessary third-party dependencies.
