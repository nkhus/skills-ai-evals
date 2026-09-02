# Technical Research Guide

Use this guide to build a precise execution model of the component. Cover only
items that are relevant, but investigate each category before deciding it is
not applicable.

## 1. Repository boundary

Identify:

- implementation directories and source files;
- primary classes, functions, modules, prompts, and schemas;
- generated code or configuration that changes behavior;
- ownership boundaries with adjacent components;
- aliases or alternative names used for the same component.

Do not assume a directory name equals the true runtime boundary. Follow imports,
registration, dependency injection, factories, and configuration.

## 2. Entry points and callers

Determine:

- who invokes the component;
- whether invocation is synchronous, asynchronous, streamed, queued, or event-driven;
- public API, message, command, hook, or pipeline contracts;
- how the component is instantiated and configured;
- whether different callers use it differently.

Include representative caller paths and symbols.

## 3. Inputs

Document the semantic meaning of inputs, not only their types:

- required and optional fields;
- normalization or preprocessing;
- hidden context, session state, permissions, and defaults;
- accepted malformed or partial input;
- source of each input;
- input variations that change behavior.

Call out inputs that are technically optional but functionally required.

## 4. Execution flow

Trace the main path from input to output:

1. validation and normalization;
2. branching, routing, planning, or prompt construction;
3. model, retrieval, tool, API, or database calls;
4. intermediate transformations;
5. post-processing and output construction;
6. error and fallback paths.

Describe important branches and stopping conditions. Avoid exhaustive line-by-line
summaries.

## 5. Outputs and side effects

Identify:

- return values and schemas;
- streamed events or intermediate messages;
- state mutations and persisted data;
- tool calls and external actions;
- logs, traces, citations, retrieved items, or decision records;
- partial outputs and error outputs;
- downstream assumptions about the result.

Separate user-visible outputs from internal artifacts.

## 6. Dependencies and variability

Record dependencies that influence behavior:

- LLM models and generation settings;
- prompts, templates, policies, or system instructions;
- retrievers, indexes, rerankers, tools, services, and databases;
- feature flags and environment configuration;
- time, locale, permissions, tenant, or user state;
- nondeterministic providers or stochastic decisions.

Explain which dependencies are controllable during evaluation and which are not.

## 7. Reliability behavior

Investigate:

- validation failures;
- exception handling;
- retries and retry ownership;
- timeouts and cancellation;
- fallbacks and degraded modes;
- empty, partial, or stale results;
- duplicate execution and idempotency;
- concurrency and ordering assumptions.

Describe the externally observable result of each important failure path.

## 8. Observability

List signals available to later evaluation work:

- final outputs;
- model requests and responses;
- prompt versions;
- retrieved documents and scores;
- selected tools and arguments;
- execution trajectories;
- citations and evidence mappings;
- timing and error events;
- component-specific debug artifacts.

Explicitly identify important decisions that are currently hidden.

## 9. Existing behavioral evidence

Inspect:

- unit and integration tests;
- fixtures and snapshots;
- example applications;
- support incidents or regression cases stored in the repository;
- documentation examples;
- comments explaining unusual behavior.

Tests are evidence of intended behavior, but not necessarily the full functional
contract. Note when tests only verify technical validity.

## Technical research output

The final component README should allow a new agent to answer:

- Where does the component begin and end?
- How is it invoked?
- What information controls its behavior?
- What does it produce or change?
- Which intermediate decisions are observable?
- Which dependencies and failure paths affect evaluation?
