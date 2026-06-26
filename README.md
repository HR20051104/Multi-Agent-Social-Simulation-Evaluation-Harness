# Multi-Agent Social Simulation Evaluation Harness

> AI can throw stones. The simulation generates ripples.

A bounded simulation harness where AI may propose interventions, but the simulation — not the AI — decides consequences. Player input is also bounded and must pass through simulation mechanisms.

---

## Core Principle

- AI does **not** directly mutate final world outcomes
- AI does **not** directly decide trust, legitimacy, obedience, task success, or political collapse
- Player commands are interpreted through a layered semantic pipeline, not executed directly
- Hidden world state is sealed from player-facing reports
- **Projection API** is the only player-visible boundary — no raw internals leak

## Architecture

```
Player Intent → StoneBundle → Validator/Revision
  → ActionRequirementPlan → RequirementTaskRecord
  → TaskAssignmentRecord → TaskProgressRecord
  → Progress History → Future Influence

Supporting layers:
  Signal / Trace / Disturbance
  Expectation / Memory / ActionTendency
  ParameterDynamics (fast / medium / slow)
  Cognitive Projection → Player-visible Reports
  Governance Posture Signal → Bounded Reaction/Norm/Clue Bias
  Command Semantics → Time / Speech Act / Condition Detection
  Normative Objects → Birth / Trace / Lifecycle / Interaction
  Situated Interaction → Presence / Speech Radius / Availability / R101 Assistant
  Population → 100/150/200 Resident Generation / Social Ecology / Relation Graph
```

## Current Status

**v2.9 M0 — Communication Context Reframe**
- **2469 tests, 0 failed** (deterministic, no real LLM required)
- v2.6 Release Candidate frozen
- v2.7 stack: Projection API → CLI Playable Loop → Governance Posture → Command Semantics → Information Channel → Attention Priority → Situated Interaction → Actor Availability → Interaction Audit → R101 Assistant → Player Presence → Playtest Audit
- v2.8 stack: Resident Population (100/150/200) → Social Ecology / Relation Graph → Background Propagation → Signal/Memory/Trace Accumulation
- v2.9 M0: Communication Context Reframe

Full timeline: see [`PROJECT_CONTROL_DASHBOARD.md`](PROJECT_CONTROL_DASHBOARD.md)

## Key Design Decisions

| Decision | Rationale |
|---|---|
| AI does not determine outcomes | Simulation integrity; prevents LLM-as-god-mode |
| Projection API is sole player boundary | No hidden state leaks through reports |
| Norms are not laws | Compliance ≠ task completion; violation ≠ punishment |
| Governance posture is a signal, not an outcome | Bounded influence, no direct actor mutation |
| R101 is an activatable proxy, not a god-mode executor | Can record/coordinate, cannot decide/punish/execute |
| Construction is proposal-first | Dashed preview → check → approval → construction; never direct build |
| Population is deterministic | 100/150/200 residents via seeded generation |

## Repository Structure

```
├── README.md                          ← This file
├── PROJECT_CONTROL_DASHBOARD.md       ← Full project dashboard & timeline
├── community_ai_sandbox_masterplan_v0_4.md
├── community_ai_sandbox_core_system_design_v0_2.md
├── src/                               ← Backend simulation engine
│   ├── models.py                      ← All data models (WorldState, records, etc.)
│   ├── world.py                       ← World creation & simulation ticks
│   ├── llm_stone_engine.py            ← Full pipeline orchestrator
│   ├── signal_engine.py               ← Signal / Trace / Disturbance layer
│   ├── evidence_engine.py             ← Evidence-Signal reunification
│   ├── cognition_engine.py            ← Cognitive projection & clue pipeline
│   ├── social_network.py              ← Social graph & centrality
│   ├── promotion_engine.py            ← Actor promotion & lifecycle
│   ├── expectation_engine.py          ← Expectation / memory / action tendency
│   ├── parameter_dynamics.py          ← Fast/medium/slow parameter evolution
│   └── world_clock.py                 ← Simulation time
├── prototype_v2/
│   └── community_ai_sandbox_v2/
│       ├── src/                       ← v2.7 CLI & Projection API runtime
│       │   ├── cli_playable_loop.py   ← Terminal playable interface
│       │   ├── projection_api.py      ← Safe player-facing views
│       │   ├── save_load.py           ← Session persistence
│       │   └── scenario_package.py    ← Named scenario definitions
│       ├── tests/                     ← Full test suite (2469 tests)
│       ├── scripts/                   ← Audit & demo runners
│       ├── ui_mock/                   ← 2.5D grid world UI prototype
│       │   ├── grid_world.html        ← Isometric canvas renderer
│       │   ├── projection_adapter.js  ← Adapter boundary (mock → real)
│       │   ├── INTEGRATION_CHECKLIST.md
│       │   └── projection_snapshot_schema_sample.json
│       └── ARCHITECTURE_*.md          ← Architecture documents
└── V2_*.md                            ← Release & milestone reports
```

## Running Tests

```bash
# Full test suite (deterministic, no LLM required)
python -m pytest prototype_v2/community_ai_sandbox_v2/tests -q
# → 2469 passed, 0 failed
```

## UI Mock (2.5D Grid World)

Open in browser:
```
ui_mock/grid_world.html     ← Isometric community world renderer
ui_mock/smoke_test.html     ← Automated contract verification
```

The UI consumes only Projection API-compatible mock data. All spatial objects are data-driven — no hardcoded building components.

## License

Proprietary — research prototype.
