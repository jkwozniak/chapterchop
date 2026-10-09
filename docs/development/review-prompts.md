# Predefined prompts for AI-driven review

| Prompt                          | When to use                                                          |
| ------------------------------- | -------------------------------------------------------------------- |
| **Architectural Change Review** | after changes are made to the application architecture or data flow  |
| **Public API Review**           | when making changes to the public API or adding new components       |
| **Architecture Review**         | when a new implementation of an existing component was added         |
| **Implementation Review**       | when a new production code was introduced                            |
| **Test Review**                 | after adding or modifying tests                                      |
| **Documentation Review**        | after updating the README, `docs/architecture.md`, or docstring      |
| **Full Component Review**       | before the component implementation is considered complete           |
| **Pre-merge Review**            | immediately before merging the branch                                |

___


## Architectural Change Review

Review this architectural change using the following sections of `docs/development/review-checklist.md`:

- Architecture
- Public API
- Documentation

Additionally verify that:

- architectural responsibilities remain well separated,
- new concepts fit the existing architecture,
- the design philosophy remains consistent,
- project documentation reflects the architectural changes,
- AI instruction files should be updated if the architectural model has changed.

Do not review implementation details unless they affect the architecture.
List only findings and recommendations.


## Public API Review

Review the public API using the **Public API** section of `docs/development/review-checklist.md`.

Focus on:

- API clarity,
- naming consistency,
- discoverability,
- explicitness,
- public surface consistency,
- unnecessary public members.

Ignore implementation details unless they affect the public API.
List only findings and recommendations.


## Architecture Review

Review the modified code using the **Architecture** section of `docs/development/review-checklist.md`.

Focus on:

- component responsibilities,
- architectural boundaries,
- protocol usage,
- pipeline consistency,
- immutability assumptions,
- overall architectural coherence.

Do not comment on naming, formatting, documentation or tests unless they directly affect the architecture.
List only findings and recommendations.


## Implementation Review

Review the implementation using the following sections of `docs/development/review-checklist.md`:

- Error Handling
- Typing
- Code Style & Readability
- Maintainability

Focus on:

- correctness,
- readability,
- Python idioms,
- exception handling,
- type annotations,
- maintainability,
- unnecessary complexity,
- duplication.

Ignore formatting issues already handled by Ruff.
List only findings and recommendations.


## Test Review

Review the test suite using the **Testing** section of `docs/development/review-checklist.md`.

Check whether:

- protocol contracts are fully covered,
- implementation-specific behavior is tested,
- important behaviors are missing,
- tests remain deterministic,
- assertions verify behavior rather than implementation details,
- reusable testing infrastructure is used consistently.

Do not review the production code unless necessary to explain a finding.
List only findings and recommendations.


## Documentation Review

Review all documentation changes using the **Documentation** section of `docs/development/review-checklist.md`.

Focus on:

- accuracy,
- consistency,
- terminology,
- completeness,
- docstring quality,
- synchronization between code and documentation.

List only findings and recommendations.


## Full Component Review

Review this implementation using the complete `docs/development/review-checklist.md`.

Review the code from the following perspectives:

- Architecture
- Public API
- Error Handling
- Typing
- Testing
- Documentation
- Code Style & Readability
- Maintainability

Focus on identifying issues rather than praising the implementation.
Ignore formatting issues already enforced by project tooling.
Organize the findings under the corresponding checklist sections.
If no issues are found in a category, explicitly state that no findings were identified.


## Pre-merge Review

Review the complete set of changes before merging.

Use the complete `docs/development/review-checklist.md`.

Additionally verify that:

- the implementation fully satisfies the stated requirements,
- no unrelated changes were introduced,
- the public API remains consistent,
- documentation has been updated where required,
- tests cover all newly introduced behavior,
- the changes remain focused on the original issue.

Report findings grouped by checklist category.
Ignore formatting issues already covered by project tooling.
