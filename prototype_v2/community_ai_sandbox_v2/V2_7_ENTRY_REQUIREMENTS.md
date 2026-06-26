# v2.7 Entry Requirements

## Theme

Projection API / Playable Text Interface

## Goal

Expose player-facing views of the existing world_state without leaking true_state or hidden internals.

## Planned Milestones

- v2.7 M1: Projection API Specification
- v2.7 M2: Player dashboard schema
- v2.7 M3: Visible report renderer
- v2.7 M4: Known clue view
- v2.7 M5: Visible norm view
- v2.7 M6: Visible resident summary
- v2.7 M7: Recent event log
- v2.7 M8: Save / load (minimal)
- v2.7 M9: CLI playable loop (minimal)
- v2.7 M10: Scenario starter package

## Must Not

- expose hidden IDs / backend scores / semantic tags
- treat PlayerKnowledge as true_state
- create outcome injection
- bypass v2.6 mechanisms
- add punishment/reward/task-completion shortcuts just for playability

## Entry Condition

v2.6 Final Freeze must be PASS with test baseline locked.
