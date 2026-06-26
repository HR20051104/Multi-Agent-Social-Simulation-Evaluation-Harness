# V2.6 Developer Handoff

## 1. Current Status

v2.5-v2.6 now has:

- action chain
- reaction chain
- propagation chain
- evidence-signal reunification
- semantic resonance
- cognitive projection
- dynamic normative objects with birth, trace, lifecycle, and integration audit

## 2. What Works

- continuous multi-round world_state history
- bounded player intent interpretation
- requirement/task/progress deposition
- actor reactions and limited propagation
- evidence and projection layers
- normative birth, trace evaluation, lifecycle recalibration

## 3. What Does Not Exist Yet

- task completion lifecycle
- meeting completion lifecycle
- building completion lifecycle
- full UI / projection API
- norm network interaction planning
- institutional law / court systems

## 4. How to Add a New Feature Without Breaking Architecture

1. Represent new behavior through existing record types first.
2. Prefer tags, traces, memories, disturbances, clues, and bounded deltas.
3. Add audit tests before broadening runtime behavior.
4. Preserve the invariant that AI cannot directly decide outcomes.
5. If a new feature seems to require a standalone punishment/law/rebellion system, stop and redesign it through existing architecture.

## 5. How to Add a Test Scenario

1. Reuse a continuous real `world_state`.
2. Avoid explicit record passing.
3. Prefer `write_files=False` runner helpers for tests.
4. Assert both behavior and safety.
5. Assert hidden-leak absence.

## 6. How to Debug a Failed Round

Check in order:

1. bundle interpretation / revision
2. requirement plan
3. task / assignment / progress
4. reactions
5. propagation
6. evidence-signal reunification
7. resonance
8. clue / knowledge / visible projection
9. normative birth
10. norm trace
11. norm lifecycle

## 7. How to Verify No Hidden Leak

Inspect:

- visible projection text
- status report excerpts
- player knowledge text

Look for forbidden leakage:

- ids
- hidden summaries
- raw scores
- raw deltas
- private resonance keys
- semantic tag dumps

## 8. How to Verify No Outcome Injection

Always assert:

- no task completion
- no meeting held
- no building created
- no guard actors
- no A2 harm/removal
- no direct trust / legitimacy / authority / resource mutation
- no punishment / reward

## 9. How to Extend Norms Safely

Do not add special systems for:

- corruption
- law
- punishment
- rebellion
- promise
- secrecy
- rumor
- deception

Represent them through:

- tags
- records
- traces
- evidence
- resonance
- cognitive projection
- bounded constraints

## 10. Recommended Next Stages

- v2.6 Milestone 5: Norm Network Interaction Planning
- later UI / projection work only after architectural cleanup stays stable
- keep using audit milestones before introducing new runtime depth
