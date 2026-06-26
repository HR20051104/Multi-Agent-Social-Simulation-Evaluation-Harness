# PROJECT CONTROL DASHBOARD

## 1. Project Vision

Build a simulation where AI may propose bounded interventions, but the simulation decides the consequences.

Core principle:

> AI can throw stones. The simulation generates ripples.

That means:

- AI does not directly mutate final world outcomes.
- AI does not directly decide trust, legitimacy, obedience, task success, or political collapse.
- Player input is also bounded and must pass through simulation mechanisms.

## 2. Current Status

**Current Version:** v2.9 M0 Communication Context Reframe completed

Archived markers (latest first):
- v2.8 M4 Signal / Memory / Trace Accumulation Stress completed ✅
- v2.8 M3 Background Propagation Stress completed ✅
- v2.8 M2 Social Ecology / Relation Graph Refinement completed ✅
- v2.8 M1 Resident Population Foundation completed ✅
- v2.7 M8 Presence-Mediated Playtest Audit completed ✅
- v2.7 M7.6 Player Presence / Speech Radius / Direct Routing Patch completed ✅
- v2.7 M7.5 Player Assistant / R101 Command Inbox completed ✅
- v2.7 M7 Interaction Integration Audit completed ✅
- v2.7 M6.5 Actor Availability / Consent / Avoidance Patch completed ✅
- v2.7 Milestone 6 Situated Interaction Channel completed ✅
- v2.7 M4.6 Information Access and Channel Reliability Patch completed ✅
- v2.7 M4.5 Command Semantics Patch completed ✅
- v2.7 M4 Save/Load and Scenario Package completed ✅
- v2.7 M3.5 Governance Posture Signal Patch completed ✅
- v2.7 M3 CLI Playable Loop completed ✅
- v2.7 M2 Projection API Runtime completed ✅
- v2.7 M1 Projection API Specification completed ✅
- v2.6 Release Candidate Freeze completed ✅
- v2.6 Milestone 6 Norm Network Interaction Runtime completed ✅
- v2.6 Milestone 5 Norm Network Interaction Planning completed ✅

**Test Status:**

- pytest: `2469 passed, 0 failed`
- warnings: `PytestCacheWarning` only

**Core Achievements:**

- Dynamic influence-signal three-layer architecture stable.
- WorldClock, task externalization, signal latency, blocking, leakage, cognitive projection in place.
- Expectation, memory, action tendency, parameter dynamics, actor promotion integrated.
- Real LLM stone pipeline exists, opt-in and bounded.
- **Action Chain** (v2.5.5→v2.5.9a):
  - Generic Action Requirement / World Affordance Resolver completed.
  - Arbitrary player intent resolves into required participants, venue, resources, authority, communication channel, execution chain, schedule, information, and risk acceptance.
  - Missing requirements become RequirementTaskRecord pending tasks.
  - Actors can accept, delay, refuse, deflect, need resources, or be blocked.
  - Assignments produce progress records without completing tasks.
  - Task progress deposits into world_state history and influences later assignment/progress.
  - Same world_state carries multiple rounds of social history (10-command smoke test).
- **Reaction Chain** (v2.5.10→v2.5.11):
  - Directly affected actors produce bounded ActorSocialReactionDraft records.
  - Real LLM reaction path validated and safe when enabled.
  - Coercive scenarios no longer collapse to generic concern_expression (diversity calibration).
  - Reaction history influences future reaction/assignment/progress.
- **Milestone** (v2.5.11a):
  - Social Network Milestone 1: PASS.
  - Action chain and reaction chain verified together in same real world_state.
  - World carries both progress history and reaction history.
  - Future influence verified without explicit record passing.
  - No sandbox copy-back. No outcome injection. No task completed. No guard actors. No A2 harm.
  - Normal report leak audit passed.
- **v2.6 Dynamic Normative Objects**
  - Milestone 1: norm birth and bounded constraint sources persisted in `world_state`.
  - Milestone 2: norm alignment evaluation added.
  - Compliance / violation / dispute / bypass traces now map into Evidence-Signal records.
  - Normative traces can generate clue candidates and player knowledge.
  - Compliance is not task completion.
  - Violation is not punishment.
  - High-confidence violation requires audit / hard trace.
  - Rumor / resonance alone cannot confirm violation.
  - Coercive command disputes enforcement expectation but does not create harmful permission.
  - Milestone 3: normative lifecycle update records added.
  - Norm trace history now updates recognition / contestation / enforcement expectation / compliance pressure.
  - Norms can be reinforced, weakened, contested, or decayed.
  - Status changes now recalibrate bounded constraint influence.
  - Reinforced norms do not force compliance.
  - Contested norms do not trigger rebellion.
  - Weakened norms do not disappear silently.
  - Lifecycle evidence enters evidence-signal and cognitive projection.
  - Milestone 4: full normative object loop audited across 18 continuous rounds.
  - Norm birth / constraint influence / trace loop / lifecycle update verified together.
  - Normative loop integrated with action, reaction, evidence-signal, resonance, and cognitive projection.
  - Later rounds read norm history from `world_state`.
  - Player knowledge remains distinct from true state.
  - Hidden norm internals remain sealed.
  - Coercive high-risk command remains safe.
  - No punishment/reward/direct outcome introduced.
  - Consolidated architecture document created.
  - Runtime pipeline reference created.
  - Data model registry created.
  - Safety invariants document created.
  - Developer handoff created.
  - Static consolidation audit added.
  - No new runtime mechanism introduced.
  - Existing v2.5-v2.6 loops preserved.
  - Milestone 5: Norm network interaction architecture planned.
  - `NormInteractionRecord` specified.
  - Interaction types defined: supports, conflicts_with, exception_to, depends_on, proceduralizes, legitimizes, contests, supersedes, duplicates, and related forms.
  - At least 10 planned interaction mappings generated.
  - All planned effects remain bounded previews.
  - High-risk commands cannot become valid harmful exceptions.
  - No special law/policy/court system required.
  - No outcome engine introduced.
  - **Milestone 6: Norm Network Interaction Runtime** (42 tests):
    - Norm-to-norm interaction pipeline implemented (`identify_norm_interaction_candidates`, `evaluate_norm_interaction`, `persist_norm_interaction`, `compute_norm_network_influence`).
    - 4 interaction types operational: supports, conflicts_with, exception_to, depends_on. No LLM.
    - Interaction records flow through evidence-signal and cognitive projection.
    - 15-command multi-round smoke test covering coercive + resource + norm manipulation.
  - **v2.6 Norm Network Integration Audit** (60 tests):
    - Full norm network interaction loop integrated with action, reaction, evidence-signal, resonance, cognitive projection pipeline.
    - Norm interaction history read from world_state across rounds.
    - Coercive high-risk commands remain non-permissive under norm network interaction.
  - **v2.6 Release Candidate Freeze** (25 tests):
    - Architecture freeze: final architecture index, test baseline, v2.7 entry requirements documented.
    - No new mechanisms, no LLM.
- **v2.7 Projection API & CLI Playable Loop**
  - **M1: Projection API Specification** (36 tests):
    - Architecture, Player View Schema (8 views: Dashboard, Report, Clue, Norm, Resident, Event, Context, Snapshot), Safety Rules, and Contract documents.
    - Forbidden fields cataloged: source IDs, semantic_tags, scores, hidden_summary.
  - **M2: Projection API Runtime** (36 tests):
    - Read-only safe player-facing projection API implemented.
    - Internal fields sealed from player views. Confidence labels sanitized.
    - Leak detection verifies no forbidden fields escape. No world_state mutation.
  - **M3: CLI Playable Loop** (36 tests):
    - Thin shell connecting v2.6 full pipeline + v2.7 Projection API.
    - CLI session management (create/tick/render). Built-in demo commands without real LLM.
    - Leak detection before each display. Never exposes true_state or hidden IDs/scores/tags.
  - **M3.5: Governance Posture Signal Patch** (38 tests):
    - Deterministic keyword-based posture detection: bounded/unbounded leniency, procedural firmness, trust granting, coercive pressure.
    - 10 posture dimensions scored [0,100]; all biases bounded.
    - Posture signals map to evidence-signal records (Signal, Memory, Disturbance, ClueCandidate).
    - Bounded influence: reaction/resonance/norm_lifecycle/clue_projection biases.
    - Projection API uses safe uncertainty language — no raw scores or posture IDs exposed.
    - Coercive commands detected as harmful_pressure_blocked — no outcome executed.
- **M4.5: Command Semantics Patch** (51 tests):
  - 12 time/deadline semantics types + 15 speech act types detected deterministically.
  - CommandSemanticsRecord with bounded biases → evidence-signal.
  - Compatible with Governance Posture (adjacent layers).
  - Projection uses safe uncertainty language. No raw scores/IDs exposed.
  - **M4.6: Information Access and Channel Reliability Patch** (56 tests):
    - InformationChannelSignalRecord added to world_state.
    - Deterministic detection of information source/channel types and access semantics.
    - Reliability tiers implemented for rumor/private/anonymous/inference/audit/inventory/report channels.
    - Social rumor, anonymous tip, private statement, actor statement, and inference channels cannot confirm facts by themselves.
    - Audit/inventory channels can support higher confidence only with hard evidence and never create direct outcomes.
    - Evidence-signal integration added via Signal / Memory / Disturbance / ClueCandidate.
    - Projection API and CLI turn rendering now use safe channel wording instead of raw reliability scores or IDs.
    - Compatible with Governance Posture, Save/Load, and Command Semantics layers.
  - **M5: CLI Playability Audit and First Playtest Package** (46 tests):
    - First playtest package created.
    - Playtest guide, command script, and feedback form created.
    - Automated CLI playability audit and transcript export created.
    - Import path sanity check added for root src vs prototype_v2 src entrypoints.
    - Save/load validated in a continuous playtest flow.
    - Governance Posture, Command Semantics, and Information Channel semantics validated together.
    - Projection API safety and high-risk command safety validated in first-playtest conditions.
    - Playtest ready score recorded.
  - **M5.5: Attention / Priority / Bandwidth Patch** (53 tests):
    - Attention priority signal model added.
    - Demand type detection implemented.
    - Priority tier detection implemented.
    - Actor bandwidth estimation added.
    - Attention load estimation added.
    - Overload / focus conflict / triage pressure represented.
    - Bounded influence added.
    - Projection API safe bandwidth wording added.
    - Save/load compatibility preserved.
    - Playtest package lightly updated.
    - M3.5 / M4.5 / M4.6 / M5 compatibility preserved.
- **M6: Situated Interaction Channel** (69 tests):
  - Situated interaction session model added.
  - Interaction turn model added.
  - Private conversation / group meeting / public announcement / delegated inquiry / audit interview / warning / reassurance channels supported.
  - Safe actor reply summaries added.
  - Evidence-signal integration added.
  - Projection API visible interactions added.
  - CLI `interactions` built-in added.
  - Save/load compatibility preserved.
  - No truth access / no direct confession / no outcome shortcut.
  - M3.5 / M4.5 / M4.6 / M5 / M5.5 compatibility preserved.
  - **M6.5: Actor Availability / Consent / Avoidance Patch** (69 tests):
    - Actor availability / consent model added.
    - Avoidance / deferral / mediator need represented.
    - Written response / public-only / mediated channel alternatives supported.
    - Availability records map to evidence-signal.
    - Projection API visible availability added.
    - CLI `availability` and `consent` built-ins added.
    - Save/load compatibility preserved.
    - No guilt implication from avoidance.
    - No compliance implication from consent.
    - No violation implication from refusal.
    - M3.5 / M4.5 / M4.6 / M5.5 / M6 compatibility preserved.
  - **M7: Interaction Integration Audit** (70 tests):
    - Full interaction stack integration audit added.
    - Continuous multi-round scenario validated.
    - Semantic layers jointly verified.
    - Interaction and availability jointly verified.
    - Projection API safety verified.
    - Save/load continuity verified.
    - Safety matrix generated.
    - Transcript generated.
    - No truth access / no direct confession / no outcome shortcut verified.
    - v2.7 ready for scale stress test.
  - **M7.5: Player Assistant / R101 Command Inbox**
    - Player assistant inbox added.
    - R101 command proxy routing added.
    - Assistant message records added.
    - Routing decision records added.
    - Player self-action intent records added.
    - `assistant` / `inbox` / `r101` / `self` built-ins added.
    - Projection-only queries supported.
    - World-affecting routed commands supported.
    - High-risk self-action safety redirect added.
    - Projection API visible assistant inbox and self actions added.
    - Save/load compatibility preserved.
    - No omnipotent R101 / no outcome shortcut.
  - **M7.6: Player Presence / Speech Radius / Direct Routing Patch**
    - Presence context model added.
    - Speech event model added.
    - R101 activation state added.
    - Speech mode / audible scope represented.
    - Focus actor / direct interaction routing added.
    - Nearby actor audibility added.
    - R101 no longer default listener.
    - Assistant proxy retained as explicit route.
    - Self-action complex physical construction redirected to project / delegation / safety intent.
    - Future scene / UI click interface prepared.
    - Projection API visible presence and visible speech events added.
    - Save/load compatibility preserved.
    - No omnipotent R101 / no direct world-structure outcome.
  - **M8: Presence-Mediated Playtest Audit** (152 tests):
    - Full playtest audit over v2.7 presence-mediated routing stack.
    - 25-command continuous playtest across all speech modes, R101 states, focus/unfocus, save/load.
    - All 14 audit targets verified with no regression, no hidden-state leakage, and no direct world-structure or outcome shortcut.
    - No new mechanisms, no real LLM required.
  - **v2.8 M1: Resident Population Foundation** (145 tests):
    - Deterministic population generation for 100, 150, and 200 residents.
    - 5 new record types + 5 WorldState containers. Lightweight profiles.
    - Safe Projection API views: population_summary, resident_directory, social_clusters, building_groups.
    - 3 new scenario variants. CLI built-ins: population, residents, buildings, clusters.
    - Save/load compatible. All generation deterministic. No new authority systems.
  - **v2.8 M2: Social Ecology / Relation Graph Refinement** (114 tests):
    - Deterministic relation graph for 100/150/200 residents.
    - Household, building, floor, cluster, role, weak cross-building edges.
    - Bridge actor detection, neighborhood pockets, cluster overlap.
    - 4 new record types + safe Projection API views + CLI built-ins.
    - Save/load compatible. No new authority, truth, or outcome systems.
  - **M4: Save/Load and Scenario Package** (38 tests):
    - Save/Load module: 10 helpers for session persistence with WorldState dataclass reconstruction.
    - Scenario Package module: 8 helpers for named scenarios (b2_resource_governance, high_tension, smoke_test).
    - CLI built-ins: save, load, saves, scenarios, new, scenario, snapshot — none advance world turns.
    - Save files contain backend state internally but are never rendered to players.
    - Save/list/load commands display only safe metadata.
    - 16-point integrity verification passes across save/load cycle.
    - Governance commands after load advance rounds correctly through full v2.6 pipeline.

**Current Risks:**

- Full multi-turn dialogue mode remains minimal.
- Actor consent remains rule-based.
- Scene system is still placeholder-level.
- CLI remains text-only.
- Population scale foundation laid (100/150/200), but not yet stress tested with full social propagation or multi-round tick runs.
- Social ecology and relation graph (M2) not yet implemented.
- Evidence-signal accumulation under population load not yet tested (M4).
- No full UI yet.
- Dual import path structure still exists but is recorded.
- No social propagation yet.
- No task completion lifecycle yet.
- Real LLM paths remain opt-in and must stay validator-guarded.

## 3. Version Timeline

- [x] v2.0 Core three-layer simulation baseline
- [x] v2.1 Core bug fixes and regression baseline
- [x] v2.2 Mechanism readability and closure fixes
- [x] v2.2.1 Promise/blocking/report cleanup
- [x] v2.2.2 Long causal chain verification
- [x] v2.2.3 Long-term centrality cleanup
- [x] v2.3 Actor Promotion Minimal Loop
- [x] v2.3.1 Promoted Actor Lifecycle
- [x] v2.4 Action Tendency Minimal Loop
- [x] v2.4.1 ActionIntent abstraction
- [x] v2.4.2 Expectation unification
- [x] v2.4.3 Expectation to action feedback
- [x] v2.4.4 Parameter dynamics unification
- [x] v2.4.5 Parameter dynamics integration audit
- [x] v2.5 Situation interpreter + StoneProposal loop
- [x] v2.5.1 Real LLM Stone Trial
- [x] v2.5.1a AI Intervention Levels + StoneBundle Interface
- [x] v2.5.2 Bounded Impact Diversity Trial
- [x] v2.5.2a Seed Stability / Scenario Audit
- [x] v2.5.3 Player Intent Bundle Trial
- [x] v2.5.3a Bundle Execution Dry Run
- [x] v2.5.3b Real LLM Player Intent Bundle Trial
- [x] v2.5.3c Command vs Dry-run Gap Audit
- [x] v2.5.3d Bundle Repair Before Fallback
- [x] v2.5.3e Iterative Bundle Revision Loop
- [x] v2.5.4 Resource Accountability Outcome Micro-Trial
- [x] v2.5.4a Personality-driven Response Modifiers
- [x] v2.5.4b Response Memory Deposition
- [x] v2.5.4c Memory-Influenced Future Response
- [x] v2.5.4d Deposition Persistence / State Integration Policy
- [x] v2.5.4e Real World Tick Integration Trial
- [x] v2.5.5 Generic Action Requirement / World Affordance Resolver
- [x] v2.5.6 Requirement Plan → Task Draft Integration
- [x] v2.5.7 Task Assignment / Actor Acceptance Micro-Trial
- [x] v2.5.8 Task Progress / Execution Attempt Micro-Trial
- [x] v2.5.9 Progress Deposition + Future Influence
- [x] v2.5.9a Simple Social Loop Smoke Test
- [x] v2.5.10 Directly Affected Actor AI Reaction Trial
- [x] v2.5.10a Real LLM Actor Reaction Manual Trial
- [x] v2.5.10b Actor Reaction Diversity Calibration
- [x] v2.5.11 Actor Reaction Future Influence
- [x] v2.5.11a Social Network Milestone 1 Audit
- [x] v2.5.12 Minimal Social Propagation
- [x] v2.5.12a Minimal Social Propagation Audit
- [x] v2.5.13 Evidence-Signal Reunification
- [x] v2.5.14 Semantic Signal Resonance Calibration
- [x] v2.5.15 Cognitive Projection / Clue Pipeline Alignment
- [x] v2.5.16 Evidence-Signal Multi-Round Audit
- [x] v2.5.17 Pre-v2.6 Dynamic Normative Object Readiness Review
- [x] v2.6 M1: Norm Birth & Bounded Constraint
- [x] v2.6 M2: Norm Violation / Compliance Trace Loop
- [x] v2.6 M3: Norm Contestation / Decay / Reinforcement
- [x] v2.6 M4: Normative Integration Audit
- [x] v2.6 Consolidation / Architecture Cleanup
- [x] v2.6 M5: Norm Network Interaction Planning
- [x] v2.6 M6: Norm Network Interaction Runtime
- [x] v2.6 Norm Network Integration Audit
- [x] v2.6 Release Candidate Freeze
- [x] v2.7 M1: Projection API Specification
- [x] v2.7 M2: Projection API Runtime
- [x] v2.7 M3: CLI Playable Loop
- [x] v2.7 M3.5: Governance Posture Signal Patch
- [x] v2.7 Milestone 4: Save/Load and Scenario Package
- [x] v2.7 M4.5: Command Semantics Patch
- [x] v2.7 M4.6: Information Access and Channel Reliability Patch
- [x] v2.7 Milestone 5: CLI Playability Audit and First Playtest Package
- [x] v2.7 M5.5: Attention / Priority / Bandwidth Patch
- [x] v2.7 Milestone 6: Situated Interaction Channel
- [x] v2.7 M6.5: Actor Availability / Consent / Avoidance Patch
- [x] v2.7 M7: Interaction Integration Audit
- [x] v2.7 M7.5: Player Assistant / R101 Command Inbox
- [x] v2.7 M7.6: Player Presence / Speech Radius / Direct Routing Patch
- [x] v2.7 M8: Presence-Mediated Playtest Audit
- [x] v2.8 M1: Resident Population Foundation
- [x] v2.8 M2: Social Ecology / Relation Graph Refinement
- [x] v2.8 M3: Background Propagation Stress
- [x] v2.8 M4: Signal / Memory / Trace Accumulation Stress
- [ ] v2.8 M5: Large Population Projection API Safety
- [ ] v2.8 M6: Long-Run Presence-Mediated Governance Playtest
- [ ] v2.8 M7: Final 100-200 Resident Stress Audit
- [ ] v2.8 M8: Release Candidate Cleanup / Handoff Package
- [x] v2.9 M0 Communication Context Reframe
- [ ] v2.9 Playable Vertical Slice Polish
- [ ] v3.0 2D Community Demo

## 4. Active Stage

**v2.8 M2 — Social Ecology / Relation Graph Refinement**

Status: ✅ completed

Focus:

- Deterministic relation graph construction for 100, 150, and 200 residents.
- Household, building, floor, cluster, role-based, and weak cross-building edges.
- Bridge actor detection and neighborhood pocket generation.
- 4 new record types: ResidentRelationEdge, ResidentRelationGraphSummary, BridgeActorCandidate, LocalNeighborhoodPocket.
- 4 new safe Projection API views. CLI built-ins: ecology, relations, bridges, pockets.
- Save/load compatible. All generation deterministic. No new authority, truth, or outcome systems.

## 5. Next Recommended Stage

### v2.8 M3 — Background Propagation Stress

Use the M1 population graph and M2 relation graph to run bounded 1-hop and 2-hop rumor/concern propagation stress tests across 100, 150, and 200 resident populations, verifying that propagation remains bounded, does not create truth/punishment shortcuts, and is compatible with all existing v2.7-v2.8 systems.

## 6. Do-Not-Do-Yet List

- [ ] Do not implement full social propagation yet.
- [ ] Do not implement global rumor spread yet.
- [ ] Do not implement group-level fear cascade yet.
- [ ] Do not implement task completion lifecycle yet.
- [ ] Do not create MeetingObject yet.
- [ ] Do not create completed buildings yet.
- [ ] Do not create guard actors.
- [ ] Do not allow AI to directly decide outcomes.
- [ ] Do not mutate resources / trust / authority / legitimacy directly.
- [ ] Do not bypass validator boundaries.
- [ ] Do not leak latent/private/debug fields into normal report.
- [ ] Do not build UI in this phase.
- [ ] Do not expand population scale.

## 7. Architecture Summary

**Action Chain:**

```
Player Intent → StoneBundle → Validator/Revision
→ ActionRequirementPlan → RequirementTaskRecord
→ TaskAssignmentRecord → TaskProgressRecord
→ TaskProgressDepositionRecord → progress history
→ future assignment / progress influence
```

**Reaction Chain:**

```
StoneBundle / task / progress stimulus
→ directly affected actors → ActorSocialReactionDraft
→ actor reaction history → ActorReactionInfluenceRecord
→ future reaction / assignment / progress influence
```

**Norm Chain (v2.6):**

```
NormativeObjectRecord → NormTraceRecord (compliance/violation/dispute/bypass)
→ NormLifecycleUpdateRecord (reinforce/weaken/contest/decay)
→ NormInteractionRecord (supports/conflicts_with/exception_to/depends_on)
→ norm interaction history → future norm evaluation influence
```

**Projection API (v2.7):**

```
world_state (internal, all records)
→ Projection API (read-only sanitize)
→ Player Views (Dashboard, Report, Clue, Norm, Resident, Event, Context, Snapshot)
→ CLI Playable Loop (session/create/tick/render)
```

**Supporting systems:**

- Signal / Trace / Disturbance
- Expectation / Memory / ActionTendency
- ParameterDynamics (fast/medium/slow)
- BackgroundResident → SocialNode promotion + lifecycle
- Cognitive Projection for report/knowledge
- Evidence-Signal reunification + resonance

## 8. Test Status Detail

Latest full-suite result: `2158 passed, 0 failed`

Coverage includes:

- v2.0–v2.6 M4 (all earlier milestones): ~836 tests
- v2.6 M6 Norm Network Interaction Runtime: 42 tests (15-command multi-round smoke test)
- v2.6 Norm Network Integration Audit: 60 tests
- v2.6 Release Candidate Freeze: 25 tests
- v2.7 M1 Projection API Specification: 36 tests
- v2.7 M2 Projection API Runtime: 36 tests
- v2.7 M3 CLI Playable Loop: 36 tests
- v2.7 M3.5 Governance Posture Signal Patch: 38 tests
- v2.7 M4 Save/Load and Scenario Package: 38 tests
- v2.7 M4.5 Command Semantics Patch: 51 tests
- v2.7 M4.6 Information Access and Channel Reliability Patch: 56 tests
- v2.7 M5 CLI Playability Audit: 46 tests
- v2.7 M5.5 Attention / Priority / Bandwidth Patch: 53 tests
- v2.7 M6 Situated Interaction Channel: 69 tests
- v2.7 M6.5 Actor Availability / Consent / Avoidance Patch: 69 tests
- v2.7 M7 Interaction Integration Audit: 70 tests
- v2.7 M7.5 Player Assistant / R101 Command Inbox: 81 tests
- v2.7 M7.6 Player Presence / Speech Radius / Direct Routing: 80 tests
- v2.7 M8 Presence-Mediated Playtest Audit: 154 tests
- v2.8 M1 Resident Population Foundation: 145 tests
- v2.8 M2 Social Ecology / Relation Graph Refinement: 114 tests

All tests deterministic — no real LLM required in pytest.

## 9. Open Risks

1. No social propagation yet — reactions stay local to directly affected actors.
2. No group-level rumor/fear spread yet.
3. No multi-hop social propagation yet.
4. No task completion lifecycle yet.
5. Reaction influence and progress influence are still rule-based.
6. Real LLM paths remain opt-in and must stay validator-guarded.
7. Report/debug readability needs periodic audit as layers expand.
8. Norm lifecycle formulas remain rule-based and conservative.
9. Norm network interactions are rule-based and minimal (4 types).
10. Architecture files may need cleanup after rapid milestones.
11. Projection API is spec + runtime complete but no external consumer yet (beyond CLI loop).
12. Multi-seed audit is smoke-level, not exhaustive.
13. No population scale test beyond default world.
14. First full playtest package not created yet.
15. src/ has uncommitted changes (+1741 lines across 10 files) that need commit.

## 10. Decision Log

- v2.x: AI does not directly determine outcomes.
- v2.3: Background residents can emerge into full social actors.
- v2.4: Action semantics stay structured, not freeform.
- v2.5: LLM enters only as bounded interpretation/proposal assistance.
- v2.5.2: Impact proposals diversify only within whitelist and validator bounds.
- v2.5.3: Player intent can be represented as attempted bundles.
- v2.5.4: Resource accountability outcomes are sandbox-only classifications.
- v2.5.4d: Deposition persists into sandbox state; future reads from history.
- v2.5.4e: Real world tick integration — sandbox validates mechanisms, does NOT commit results to real world. Real world generates its own latent response history.
- v2.5.5: Generic Action Requirement / World Affordance Resolver — any player intent resolves into required world conditions before any outcome.
- v2.5.6: Missing requirements become pending RequirementTaskRecords.
- v2.5.7: Task assignment enters actor acceptance layer — accept/delay/refuse/deflect/needs_resources.
- v2.5.8: Task progress attempts produce bounded progress records without completing tasks.
- v2.5.9: Progress deposits into world history and influences future assignment/progress.
- v2.5.9a: 10-command simple social loop smoke test — same world_state carries history.
- v2.5.10: Directly affected actors produce bounded ActorSocialReactionDrafts.
- v2.5.10a: Real LLM actor reaction manually validated — safe when enabled.
- v2.5.10b: Coercive reaction diversity calibrated — no longer collapses to concern_expression.
- v2.5.11: Actor reaction history influences future reaction/assignment/progress.
- v2.5.11a: Social Network Milestone 1 Audit PASSED. Intent-to-social-history loop verified without explicit record passing or sandbox copy-back.
- v2.6 M1-M4: Normative objects born, traced, contested, reinforced without punishment/reward engine.
- v2.6 M5: Norm network interaction taxonomy planned — no runtime mechanism introduced yet.
- v2.6 M6: Norm network interaction runtime implemented (4 types, rule-based). No outcome engine.
- v2.6 RC: Architecture freeze. v2.7 entry requirements defined.
- v2.7 M1: Projection API spec — read-only, deterministic, forbidden fields cataloged.
- v2.7 M2: Projection API runtime — all internal fields sealed, leak detection operational.
- v2.7 M3: CLI Playable Loop — thin shell, deterministic demo, no real LLM.
- v2.7 M3.5: Governance Posture Signal Patch — posture detection via deterministic keywords; bounded biases into evidence-signal, norm lifecycle, and projection; coercive pressures marked harmful_pressure_blocked; no outcome engine.
- v2.7 M4.5: Command Semantics Patch — time/deadline and speech act detection via deterministic keywords; bounded biases into evidence-signal; coercive speech flagged as coercive_threat; compatible with Governance Posture as adjacent layer.
- v2.7 M4: Save/Load and Scenario Package — sessions persist as JSON; 3 named scenarios; WorldState reconstructed as proper dataclass; save files internal-only, never rendered to player; Projection API remains sole player-facing boundary.
- v2.7 M4.6: Information Access and Channel Reliability Patch — information source, access mode, and channel reliability now constrain confidence, verification need, and projection wording without deciding truth or creating direct outcomes.
- v2.8 M1: Resident Population Foundation — deterministic generation of 100/150/200 background residents with lightweight profiles, household/building/cluster metadata, safe Projection API views, and save/load compatibility. No new authority, truth, or outcome systems introduced. Population capacity added without changing core v2.7 architecture.
- v2.8 M2: Social Ecology / Relation Graph Refinement — deterministic relation graph construction spanning households, buildings, floors, clusters, roles, and weak cross-building links; bridge actor detection and neighborhood pockets. All relations are structural hints, never truth/guilt/authority claims.
