# Functional Research Guide

Use this guide to recover the component's real purpose and expected behavior.
Implementation details alone are insufficient for downstream evaluation design.

## 1. Functional purpose

Establish:

- the problem this component solves;
- why it exists as a distinct component;
- who benefits from its output;
- what would be lost if it were removed;
- its role in the larger user or system journey.

Prefer concrete workflow language over generic statements such as "processes
requests" or "improves quality."

## 2. Primary goal

State the single most important outcome the component is expected to achieve.
Then describe secondary responsibilities that support that goal.

A useful primary goal explains the desired behavioral result, not the
implementation mechanism.

Weak:

> Calls the search API and returns documents.

Stronger:

> Selects the evidence most likely to let the downstream answer generator
> resolve the user's question while respecting scope and access constraints.

## 3. Consumers and downstream dependence

Identify:

- direct caller;
- final user or system beneficiary;
- downstream components that interpret the output;
- assumptions those consumers make;
- whether downstream components can correct mistakes;
- how errors propagate through the workflow.

This determines which mistakes are recoverable and which are critical.

## 4. Expected behavior

Describe behavior across:

- normal, representative inputs;
- ambiguous requests;
- incomplete information;
- conflicting information;
- unsupported requests;
- boundary values and unusually large or small inputs;
- known difficult domain scenarios;
- upstream failures or missing dependencies.

For each important situation, explain the desired behavioral choice rather than
only the desired output format.

## 5. Decision semantics

When the component makes choices, determine:

- what alternatives it selects between;
- what evidence should influence the choice;
- which mistakes are worse than others;
- whether conservative or aggressive behavior is preferred;
- when it should abstain, clarify, retry, escalate, or stop;
- what uncertainty handling is expected.

These details are especially important for routers, retrievers, planners,
agents, classifiers, and answer generators.

## 6. Invariants and prohibitions

Capture behavior that must always or never occur:

- permission and scope boundaries;
- required preservation of facts or intent;
- forbidden actions or outputs;
- mandatory use of supplied evidence;
- requirements to avoid invention;
- requirements to preserve user constraints;
- domain-specific safety or compliance rules.

Distinguish functional invariants from technical schema checks.

## 7. Quality tradeoffs

Identify expected tradeoffs, such as:

- precision versus recall;
- completeness versus concision;
- autonomy versus asking for clarification;
- relevance versus diversity;
- speed versus deeper reasoning;
- strictness versus graceful recovery;
- determinism versus creativity.

Explain which direction is preferred in which situations.

## 8. Failure modes and impact

For each meaningful failure mode, capture:

- what incorrect behavior looks like;
- who or what is affected;
- whether it is visible immediately;
- whether downstream logic can repair it;
- severity and frequency when evidenced;
- repository evidence or user confirmation.

Do not reduce failure analysis to exceptions. Semantic errors are usually more
important for LLM evaluations.

## 9. Variability and acceptable alternatives

Clarify which behavior can legitimately vary:

- multiple valid answers;
- equivalent action sequences;
- optional details;
- style or phrasing variation;
- model-dependent but acceptable choices;
- intentionally underspecified behavior.

This prevents downstream criteria from treating one golden output as the only
correct behavior.

## 10. Evaluation handoff

Without proposing criteria, provide the next stage with:

- critical expected behaviors;
- important undesirable behaviors;
- representative usage scenarios;
- difficult and failure scenarios;
- observable evidence for judging behavior;
- behavior that cannot currently be observed;
- unresolved functional questions.

The handoff should make clear what matters, while leaving criterion selection,
metric design, dataset design, and grader selection to later stages.
