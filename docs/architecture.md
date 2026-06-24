# Chapterchop - architecture description
___


- [1. Project overview](#1-project-overview)
- [2. Core processing pipeline](#2-core-processing-pipeline)
- [3. Data model](#3-data-model)
- [4. Component contracts](#4-component-contracts)
- [5. Error model](#5-error-model)
- [6. Testing](#6-testing)

___


# 1. Project overview

Chapterchop is a Python tool designed to be used both as a package within more complex projects and as a standalone tool that can be run directly from the CLI.
The project's architecture formally defines the core functionality of individual components through protocols, while leaving implementation details and algorithms to individual implementations. The application is modular, separating the responsibilities of individual components.

The only system dependency that extends beyond the Python virtual environment is [FFmpeg](https://www.ffmpeg.org/).

The project is open source and released under the GPL-2.0-or-later license.


## Project goals

Chapterchop is intended to:

- process only offline audio data
- act in a deterministic and repeatable manner
- follow the protocol-first approach
- provide practical utility
- present a coherent and clear structure
- maintain clean, modern, statically typed code


## Non-goals

Chapterchop intentionally does not:

- download media
- stream audio
- fetch remote metadata
- orchestrate pipelines
- provide plugin infrastructure


## Design principles

- simplicity
- readability
- composability
- explicit contracts
- implementation flexibility
- no hidden orchestration
- minimal dependencies

Chapterchop components are expected to behave in a conceptually immutable manner.
Operations such as slicing or exporting should not mutate existing AudioData instances and should instead create new objects or side effects explicitly defined by the component contract.


## Public API

Only documented protocols, domain models, and explicitly exported implementations should be considered stable public API.


# 2. Core processing pipeline

The audio data is processed sequentially by successive system components according to the following scheme:

```
AudioData -> Analyzer -> Cutter -> Writer
```

1. Audio is loaded into an AudioData object.
2. The selected Analyzer defines the boundaries of the audio division based on its algorithm and creates a list of Chapter objects that define individual segments. Each implementation of the Analyzer can use its own algorithm for determining chapters (e.g., dividing into equal parts, detecting silence, using internal MP3 chapter markers, etc.)
3. Cutter creates a list of Segments based on the provided list of chapters and the source audio. The Segments contain separate instances of AudioData representing the specified sections. Different implementations of the component may vary in terms of the validation rules they use and the strictness of their coverage of the source audio segments (e.g., regarding gaps between tracks, overlapping tracks, etc.)
4. The selected Writer consumes a list of segments and stores audio data according to its implementation (e.g., writing individual files to a directory, writing to multiple directories, writing with compression, etc.)


# 3. Data model

## AudioData

**Language Construct:** typing.Protocol, @runtime_checkable

**Role:** Abstract representation of audio data.

**Location:** chapterchop/audio/protocols.py

**API contract:**

Contains:
- `duration_ms -> int`
- `channels -> int | None`
- `sample_rate -> int | None`

Performs:
- `slice(start_ms: int, end_ms: int) -> Self`

Semantic details:
- start_ms is inclusive
- end_ms is exclusive
- 0 <= start_ms < end_ms <= duration_ms
- invalid ranges should raise an appropriate exception

**Optional features:**

Implementations do not have to, but may support data export functionality (see: [WritableAudioData](#writableaudiodata)).

Implementations do not have to, but may provide convenience constructors for loading audio from files.
When supported, to ensure consistency across implementations, the recommended API is::

        @classmethod
        def from_file(cls, path: str | PathLike[str]) -> Self:
            ...


**Notes:**

The AudioData protocol specifies only the minimum requirements that an audio container must meet to be compatible with the other parts of the package. However, concrete AudioData implementations, in addition to the fields and methods defined by the protocol, must store audio data in an appropriate manner (e.g., for a PydubAudioData implementation using Pydub as the backend, the data container is the `pydub.AudioSegment` structure). To maintain the readability and predictability of the application, the content of AudioData is expected to be immutable, and any operations on the audio, in particular cutting, should result in the creation of new objects.


## WritableAudioData


**Language Construct:** typing.Protocol, runtime_checkable

**Role:** Optional capability for AudioData implementations that support exporting.

**Location:** chapterchop/audio/protocols.py

**API contract:**

Performs:
- `export(self, output_path: str | PathLike[str], format: str) -> None`

Semantic details:
- output_path specifies the full destination path
- backend failure should raise exception

**Notes:**


## Chapter

**Language Construct:** dataclass

**Role:** Logical representation of a chapter.

**Location:** chapterchop/models/chapter.py

**API contract:**

Contains:
- start_ms: int
- end_ms: int
- title: str | None = None
- metadata: dict[str, object] | None = None


Semantic details:
- start_ms is inclusive
- end_ms is exclusive
- 0 <= start_ms < end_ms

**Notes:**

Stores the start and end timestamps of a specific part of the source audio file that should be treated as a separate chapter.
Does not contain audio data.


## Segment

**Language Construct:** dataclass

**Role:** Logically links the audio data to the chapter that describes it.

**Location:** chapterchop/models/segment.py

**API contract:**

Contains:
- audio: AudioData
- chapter: Chapter


# 4. Component contracts

## Analyzer

**Language Construct:** typing.Protocol, runtime_checkable

**Role:** Determines the boundaries for dividing the audio into chapters.

**Location:** chapterchop/analyzers/base.py

**API contract:**

Performs:
- `analyze(self, audio: AudioData) -> list[Chapter]`

Semantic details:
- may return empty list if no relevant segments are found
- may raise `AnalyzerError` for input that is invalid or cannot be meaningfully analyzed.

**Reference implementation:** EvenSplitAnalyzer (chapterchop/analyzers/even_split.py)

**Notes:**

Implementations may use arbitrary strategies (e.g. silence detection, fixed splits, external metadata) and may optionally attach additional chapter metadata such as titles or tags. Returned chapters have to be valid, i.e. 0 <= start_ms < end_ms <= audio.duration_ms.
The contract does not specify the detailed rules for dividing the audio into chapters, such as the number of chapters, full coverage of the audio material, the absence/presence of breaks between chapters, or overlapping chapters, which depend on the specific implementation.

Although it is not formally required, implementations are encouraged to behave deterministically for identical input data and configuration.


## Cutter

**Language Construct:** typing.Protocol, runtime_checkable

**Role:** Splits audio data into physical segments based on chapter boundaries provided as input.

**Location:** chapterchop/cutters/base.py

**API contract:**

Performs:
- `cut(self, audio: AudioData, chapters: list[Chapter]) -> list[Segment]`

Semantic details:
- each segment created contains audio corresponding to the portion specified by `chapter.start_ms` and `chapter.end_ms` in the original audio source material
- each input Chapter results in exactly one Segment in output
- should return [] if provided list of chapters is empty
- may raise `CutterError` for invalid input

**Reference implementation:** SimpleCutter (chapterchop/cutters/simple.py)

**Notes:**

The created Segments should preserve the order of the content from the source material; i.e. the returned list of Segments should be sorted by `chapter.start_ms`.
The contract does not specify the detailed validation rules. Handling of gaps or overlapping chapters is not guaranteed by the contract and depends on the implementation.

Although it is not formally required, implementations are encouraged to behave deterministically for identical input data and configuration.


## Writer

**Language Construct:** typing.Protocol, runtime_checkable

**Role:** Exports audio segments as files in the local filesystem.

**Location:** chapterchop/writers/base.py

**API contract:**

Performs:
- `write(self, segments: list[Segment]) -> list[Path]`

Contract guarantees:
- creates one output file for each input `Segment`
- returns a list of paths to the created output files
- returns `[]` when provided with an empty segment list

Implementations:
- may define their own output format
- may define their own filename generation strategy
- may define their own directory layout
- may define their own export configuration
- may raise `WriterError` if exporting fails or the input data is invalid

**Reference implementation:** `DirectoryWriter` (`chapterchop/writers/directory.py`)

**Notes:**

The `write` method does not receive export configuration parameters directly. Configuration should instead be stored in the `Writer` instance itself.

Typical implementations are expected to use the `WritableAudioData.export` method and raise `WriterError` if `Segment.audio` does not implement the `WritableAudioData` protocol. However, this is not a strict protocol requirement, and alternative implementation strategies are allowed when justified by the design.

Although not formally required, implementations are encouraged to behave deterministically for identical input data and configuration.


## Component compatibility

**Protocol compatibility intentionally does not imply behavioral compatibility between all implementations.**

Protocols define structural compatibility, however different implementations may impose stricter behavioral constraints. This could lead to situations where certain implementations of components are not compatible with one another.
For instance `SimpleCutter` as input expects a list of chapters that fully cover the source audio material, whereas some implementations of `Analyzer` may return a chapter list that does not meet this requirement.

For this reason:

* Each new component implementation should contain a meaningful docstring description and clearly define valid input and output data.
* Data validation should take place at component boundaries.
* Individual implementations, besides contract tests, should have additional unit tests verifying their compliance with the declared behavior (see: [6. Testing](#6-testing)).
* If a new implementation of a component does not work correctly with other currently available components, its creator should provide at least one set of implementations of the remaining components that could together create a functional data flow.



# 5. Error model


Chapterchop defines a small, explicit exception hierarchy centered around the `ChapterChopError` base class. The goal of the error model is to provide predictable public failure semantics while remaining independent from backend-specific exceptions.

The project distinguishes between three broad categories of errors: domain model errors, processing constraint errors and component errors.


### Domain model errors

Domain model errors represent violations of domain model object invariants.
These errors are independent from any specific backend or implementation detail.

Examples include:
* chapters with negative start positions,
* chapters where `end_ms <= start_ms`.

Domain model errors indicate globally invalid model state.


### Processing constraint errors

This category represents violations of semantic constraints required by a specific processing context or implementation.

Examples include:
* chapters exceeding audio bounds,
* presence of gaps between chapters,
* presence of overlapping chapters,
* lack of full audio coverage by chapter list.

Processing constraint errors indicate that otherwise valid data does not meet the semantic requirements of a specific processing context or component implementation.


### Component errors

Component errors represent failures in operations performed by processing components.

Examples include:

* analyzer failures,
* cutting failures,
* writer/export failures,
* audio backend or decoding failures.

Each major pipeline component exposes its own top-level exception type:

* `AnalyzerError`
* `CutterError`
* `WriterError`

Audio backend and representation failures are exposed via:

* `AudioBackendError`

This allows callers to handle failures at an appropriate architectural level without depending on backend-specific exception types.


## Exception wrapping

Chapterchop components are encouraged to wrap lower-level exceptions raised by external libraries, subprocesses, or backend-specific implementations.

For example:

* ffmpeg execution failures,
* pydub decoding errors,
* filesystem export errors,
* invalid backend state.

Wrapped exceptions should:

* preserve the original exception via `raise ... from ...`,
* expose a stable Chapterchop exception type,
* avoid leaking backend-specific implementation details into the public API.

This approach keeps the public error model deterministic and consistent while still retaining full debugging context.

The exception hierarchy may expand over time as new processing features and validation rules are introduced.


# 6. Testing

The project uses `pytest` as the primary framework for automated testing.

The test suite is organized to clearly separate:

* reusable testing infrastructure,
* static test resources,
* test case definitions.


## Test Infrastructure

Reusable testing utilities are stored in `tests/support/`.
This directory contains helper code shared across multiple test modules, including:

* fixtures,
* factories,
* stubs,
* helper functions,
* assets registry,
* and other reusable testing utilities.

`tests/support` contains executable test support code only.


## Test Assets

Static files used during testing are stored in `tests/assets/`.
This directory is intended for non-code resources such as:

* sample audio files,
* corrupted media files,
* expected output data,
* and other filesystem-based test resources.

The `tests/assets` directory stores static data, while `tests/support/assets` contains a registry of all available assets in the form of Enum classes (`registry.py`) with a simple path resolver (`path_resolver.py`).


## Test Structure

Test cases themselves are grouped by component and test type.
The project distinguishes between:

* contract tests, which verify compliance with protocol-level guarantees,
* and implementation tests, which verify behavior specific to a concrete implementation.


Simplified test directory tree structure:
```
tests
├── analyzers
│   ├── contract
│   │   └── test_analyzer_contract.py
│   ├── implementation_1
│   │   └── test_implementation_1.py
│   └── implementation_2
│       └── test_implementation_2.py
├── assets
│   └── audio
├── audio_data
│   ├── contract
│   │   └── test_audio_data_contract.py
│   ├── implementation_1
│   │   └── test_implementation_1.py
│   └── implementation_2
│       └── test_implementation_2.py
├── cutters
│   ├── contract
│   │   └── test_cutter_contract.py
│   ├── implementation_1
│   │   └── test_implementation_1.py
│   └── implementation_2
│       └── test_implementation_2.py
├── support
│   ├── assets
│   ├── factories
│   ├── fakes
│   ├── fixtures
│   ├── helpers
│   └── stubs
└── writers
    ├── contract
    │   └── test_writer_contract.py
    ├── implementation_1
    │   └── test_implementation_1.py
    └── implementation_2
        └── test_implementation_2.py
```


## Contract vs Implementation testing

For each component, there are two sets of unit tests - contract tests (common to all implementations of a given component) and tests specific to a particular implementation.


### Contract tests

Contract tests define the minimum behavioral guarantees required from all implementations of a given component. They verify only the guarantees, rules, and invariants defined by the protocol interface and its documented semantics.

Because most protocol semantics are expressed exclusively through docstrings, **contract tests are responsible for enforcing compliance with the established contract**. Therefore, any change to the protocol’s semantics must be reflected in the corresponding contract tests.

**Note:** The `AudioData` protocol intentionally exposes only a minimal behavioral surface. Contract tests therefore validate only protocol-visible semantics, while backend-specific audio representation details are verified at the implementation level.

Contract tests for a given component are defined in the file: `tests/plural-component-name/contract/test_component-name_contract.py` (for instance: `tests/analyzers/contract/test_analyzer_contract.py` for the `Analyzer` component).
Parametrized fixtures, stored in `tests/support/fixtures/plural-component-name.py`, are used to automatically apply contract test cases to all registered implementations. These fixtures use the component factories defined in `tests/support/factories/plural-component-name.py`, which provide a unified instantiation interface across all implementations (see example below).
A given implementation is included in contract tests (and thus registered as available) by adding its factory function to the `COMPONENT-NAME_FACTORIES` list in the `tests/support/fixtures/plural-component-name.py` (see example below).
To avoid code redundancy, simple contract fixtures are typically generated from parametrized factory helpers (`tests/support/fixtures/helpers.py`). Implementations requiring pytest-managed runtime resources define their fixtures explicitly instead.


**Example - `Analyzer` component:**

| Role                              | File                                                 |
|-----------------------------------|------------------------------------------------------|
| Component contract                | `chapterchop/analyzers/base.py`                      |
| Contract tests                    | `tests/analyzers/contract/test_analyzer_contract.py` |
| Fixtures and factory list         | `tests/support/fixtures/analyzers.py`                |
| Component factory implementations | `tests/support/factories/analyzers.py`               |
| Fixture helpers                   | `tests/support/fixtures/helpers.py`                  |

`Analyzer` fixture definition (`tests/support/fixtures/analyzers.py`):
```
analyzer = simple_parametrized_fixture_factory(
    ANALYZER_FACTORIES,
)
```
List of available `Analyzer` implementation factories (`tests/support/fixtures/analyzers.py`):
```
ANALYZER_FACTORIES: list[AnalyzerFactory] = [
    make_even_split_analyzer,
]
```
In the example above:
* `analyzer` - a fixture name
* `simple_parametrized_fixture_factory` - helper fixture factory (common for various components)
* `make_even_split_analyzer` - component factory for `EvenSplitAnalyzer` (particular `Analyzer` implementation)


### Implementation tests

Implementation-specific tests should be stored in: `tests/plural-component-name/implementation-name/test_implementation-name_component-name.py`.
The implementation-specific component fixture is typically defined in the `tests/support/fixtures/plural-component-name.py`. However, when the fixture is only a wrapper for the constructor call, it could be placed directly in the test file.

**Example - `EvenSplitAnalyzer` implementation:**

| Role                    | File                                                     |
|-------------------------|----------------------------------------------------------|
| Implementation source   | `chapterchop/analyzers/even_split.py`                    |
| Contract tests          | `tests/analyzers/even_split/test_even_split_analyzer.py` |
| Fixture                 | `tests/analyzers/even_split/test_even_split_analyzer.py` |

`EvenSplitAnalyzer` fixture is just a basic constructor invocation:
```
@pytest.fixture
def analyzer() -> EvenSplitAnalyzer:
    return EvenSplitAnalyzer(parts=4)
```
Since it uses a hard-coded value, placing it together with the test definitions can be helpful in understanding the test case logic.


## Typing policy for tests

Chapterchop uses strict mypy checking for production code located in `src/`.
Test code is intentionally excluded from strict type checking. This decision avoids excessive complexity caused by pytest's highly dynamic fixture model and keeps test code focused on readability and behavioral validation rather than static typing constraints.
Type annotations in tests are still encouraged where they improve clarity, but strict mypy compliance is not required for the test suite.
