# Code Review Checklist

Review findings should focus on issues that materially improve correctness, readability, maintainability or architectural consistency. Do not report formatting or style issues that are already enforced automatically by project tooling (e.g. Ruff).

## 1. Architecture

Questions:

- Does each component have a single responsibility?
- Are architectural boundaries preserved?
- Is the component consistent with the pipeline design?
- Were existing protocols respected?
- Was any responsibility moved between components?

## 2. Public API

Questions:

- Are names consistent?
- Is the API explicit?
- Are public methods necessary?
- Is the API easy to understand?

## 3. Error Handling

Questions:

- Are custom exceptions used consistently?
- Are backend exceptions wrapped?
- Is exception chaining preserved?
- Are exceptions documented where appropriate?

## 4. Typing

Questions:

- Are type annotations complete?
- Are unnecessary Any types avoided?
- Is typing readable?

## 5. Documentation

Questions:

- Are docstrings complete?
- Is terminology consistent?
- Is semantics explained?
- Does documentation match implementation?

## 6. Testing

Questions:

- Are new behaviors tested?
- Are protocol contracts covered?
- Are implementation-specific behaviors tested?
- Are tests deterministic?
- Are assertions behavioral?

## 7. Code Style & Readability

Questions:

- Does the code follow common modern Python idioms?
- Is the code easy to read without unnecessary mental effort?
- Are variable, function, class and attribute names descriptive and consistent?
- Are complex expressions split into simpler, more readable steps where appropriate?
- Are control-flow constructs (`if`, `for`, `match`, etc.) used clearly and naturally?
- Are functions and methods at an appropriate level of abstraction?
- Are comments used only where they provide information that is not obvious from the code itself?
- Is the intent of the code immediately understandable without reading the implementation in detail?
- Are there opportunities to simplify the code without changing its behavior?
- Does the implementation avoid unnecessarily clever or overly compact solutions?

## 8. Maintainability

Questions:

- Is the code readable?
- Is duplication acceptable?
- Can responsibilities be simplified?
- Is there unnecessary complexity?
