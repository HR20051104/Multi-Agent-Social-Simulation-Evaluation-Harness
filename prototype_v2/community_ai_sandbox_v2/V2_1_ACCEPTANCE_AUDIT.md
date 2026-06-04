# V2.1 Acceptance Audit

## 1. Test Summary
- `python -m pytest prototype_v2/community_ai_sandbox_v2/tests -q`
- Result: `10 passed`
- Failures: none
- Warnings: 2 `PytestCacheWarning` entries caused by cache path write denial under `.pytest_cache`
- Conclusion impact: none. The warnings only affect pytest cache persistence, not the execution or correctness of the test cases.

## 2. Manual Scenario Results
Note: the command sequences below were executed through the same `command_parser -> run_tick` path used by the CLI, but in a deterministic harness rather than `main.py` background ticking. This avoids background-thread nondeterminism while exercising the same command semantics.

### Scenario 1: Direct Social Impact
Input commands:
```text
public_rebuke A2
nodes
edges A2
signals
report
debug_true
```

Observed:
- `A2.stress` rose from its default baseline to `43`.
- `A2 -> CHIEF` trust dropped from the default `55` to `52`.
- `public_gesture` signal was created, plus a distorted `rumor` derivative.
- `debug_true` showed an active `public_rebuke` disturbance even though there was no world-object trace.
- `report` only exposed player-facing knowledge summaries, not the full disturbance list.

Assessment:
- Expected direct social impact: yes.
- Expected signal generation: yes.
- Expected separation between report and debug: yes.

Issues found:
- Social impact is currently stronger on node psychology than on relationship dimensions. `fear` on `A2 -> CHIEF` did not visibly increase in this run.

Status: pass

### Scenario 2: World Continues Without Player Input
Input commands:
```text
assign_task A2 build_storage 1000 20 5
wait 5
tasks
nodes
signals
report
debug_true
```

Observed:
- The world advanced to `Tick 6 / Day 4` without further player input.
- Task `T1` stayed `blocked` because no resources were approved.
- `A2.stress` climbed to `62` during unattended waiting.
- New signals, leaked signals, traces, clues, and a `resource_shortage` disturbance appeared while the player did nothing.
- `report` showed only clues/knowledge summaries; `debug_true` revealed the full trace list and active disturbance.

Assessment:
- World clock is real, not fake.
- Tasks, disturbances, and signals continue to evolve during `wait`.
- Task blockage now externalizes into traces/signals/disturbance rather than remaining a log-only event.

Issues found:
- The same blocked task can generate many near-duplicate `schedule_delay` traces and clue summaries, which hurts readability and can feel mechanically spammy.

Status: pass

### Scenario 3: Player Is Not Omniscient
Input commands:
```text
assign_task A2 build_storage 3000 40 6
approve_task T1 3000 40 6
force_task T1
wait 3
report
knowledge
debug_true
```

Observed:
- `report` only showed the visible task state and one discovered clue.
- `knowledge` contained a visible `signal_order` entry plus one clue-derived topic.
- `debug_true` showed much more: `A2.stress=87`, `A2.fear=35`, `A2 -> CHIEF trust=46`, plus true traces and hidden state.
- Active signals had already decayed out by the time of inspection, but the player-facing knowledge projection remained.

Assessment:
- Report/debug information gap exists.
- The player is not full-state omniscient.
- The P0 fix around `intended_receiver_ids` is holding: signals do not enter `player_knowledge` merely because CHIEF is a target.

Issues found:
- The clue-to-knowledge summarization currently nests repeated confidence text (`置信度 ... 置信度 ...`), which reduces readability.

Status: pass

### Scenario 4: Signal Latency
Input commands:
```text
promise G2 build_garbage_point 4
signals
tick
signals
wait 3
signals
knowledge
debug_true
```

Observed:
- Immediately after the promise command, the `promise` signal existed with holder `['CHIEF']`.
- In a direct state inspection, the signal also had `pending_holder_arrivals={'A3': 2}` before the next tick.
- After one more tick, the same signal reached additional holders and later decayed away.
- `knowledge` eventually showed `signal_promise` only after CHIEF had actually held the signal.
- No `broken_expectation`, deadline-based penalty signal, or negative promise memory was generated after the stated deadline.

Assessment:
- `SocialEdge.latency` is genuinely used through `arrival_tick` / `pending_holder_arrivals`.
- Signals are not same-tick omnipresent.
- The manual debug surface is incomplete: `debug_true` does not show pending arrivals, so latency is functioning but not easily inspectable from the player/dev console.

Issues found:
- Promise deadlines are currently cosmetic in the command layer. There is no follow-up `broken_expectation` flow after deadline expiry.
- The command `promise G2 ...` does not guarantee propagation toward `G2`; propagation follows actual network edges, which may surprise a CLI auditor.

Status: partial

### Scenario 5: Centrality Shift
Input commands:
```text
node R1
appoint R1 position_supply_coordinator
tick
node R1
edges R1
report
debug_true
```

Observed:
- The command returned success text: `已任命 R1 为 position_supply_coordinator。`
- In reality, nothing meaningful changed because `position_supply_coordinator` is not present in the default world.
- After one tick, `R1` still had no edges and no meaningful access/resource/authority increase.
- `R1.overall_core_score` actually fell from its initial seed value `5` to the recomputed value `0`.

Assessment:
- The default manual scenario is not runnable as written against the stock world.
- The centrality engine itself is multidimensional, but the CLI path here silently no-ops when the position object is missing.
- This means the acceptance claim "edge node can naturally enter core circle" is not demonstrated in the default interactive path.

Issues found:
- `command_parser._cmd_appoint()` reports success even when `_handle_appoint()` exits early because the position does not exist.
- The default world lacks a ready-made `position_supply_coordinator`, so the intended centrality scenario is not available from stock CLI.
- Centrality change is currently dependent on explicit network/object changes, but this specific workflow does not produce them.

Status: fail

## 3. Architecture Compliance
| Item | Status | Notes |
|---|---|---|
| WorldClock 持续推进 | pass | `wait` advances tasks, traces, signals, clues, and node stress without player input. |
| Direct social impact | pass | `public_rebuke` directly changed `A2` psychology and `A2 -> CHIEF` trust without any world-object intermediary. |
| Disturbance source attribution | pass | P0 regression test confirms concurrent disturbances from different sources no longer cross-attribute trust changes. |
| Signal latency | partial | `pending_holder_arrivals` and `edge.latency` are real, but visibility/debugging is weak and latency is currently minimal. |
| Signal blocking/leakage | partial | Leakage and secrecy participate in propagation; `blocked_by_node_ids` exists and is checked, but there is no strong scenario proving active blocking behavior end-to-end. |
| TaskObject externalization | pass | Task lifecycle is handled in `task_engine`; social consequences are emitted as trace/signal/disturbance rather than being the top-level engine itself. |
| Player cognitive projection | pass | `current_holder_ids` and `clue.holder_node_id == CHIEF` gate player knowledge; `intended_receiver_ids` no longer leak visibility. |
| Hidden information separation | pass | `report`/`knowledge` show projection; `debug_true` exposes fuller hidden state. |
| Centrality shift | partial | The engine is multidimensional, but the default CLI appointment scenario silently fails and does not demonstrate a real edge-to-core transition. |
| Report readability | partial | The projection layer is functional, but clue summaries and repeated weak clues are noisy and sometimes redundant. |

## 4. Remaining Issues
### P0
- No new P0 architecture bug was found beyond the already-fixed v2.1 items.

### P1
- Centrality-shift acceptance path fails in stock CLI because `position_supply_coordinator` does not exist in the default world, while `appoint` still reports success.
- Promise deadline semantics are not implemented. The command text carries a deadline, but no `broken_expectation` or negative follow-up state emerges after expiry.
- Signal latency is implemented but only minimally surfaced. `debug_true` does not expose `pending_holder_arrivals`, making timing behavior hard to audit live.
- Disturbance effects still primarily modify `SocialNode` state and `trust_to_source`; broader edge-level effects like fear/obedience/flow reshaping remain limited.

### P2
- `report` and `knowledge` can become repetitive because many low-strength traces generate nearly identical clues and summaries.
- Clue-to-knowledge summarization repeats confidence text multiple times, reducing readability.
- The command-driven manual acceptance experience depends heavily on deterministic seeds for stable interpretation.
- `run_tick()` computes `is_new_day` before advancing the clock, so the returned flag is not a reliable indicator of the just-completed transition.

## 5. Recommended v2.2 Scope
Do not add a new major system. Keep scope inside mechanism quality:

- Tighten propagation, leakage, pressure, and trust tuning so effects feel less spammy and more socially legible.
- Improve report readability: deduplicate clue summaries, compress repeated weak evidence, and expose better player-facing explanations.
- Make centrality shift demonstrable in stock CLI by aligning appointment flows, default positions, and network-side consequences.
- Refine task externalization so blocked/progress-mismatch/deadline events feel less repetitive and more semantically distinct.
- Add more regression tests around signal blocking, promise expiry, and successful edge-node promotion workflows.
