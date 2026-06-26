# UI Contract — v2.7 UI Mock Prototypes

## Projection Adapter Boundary

```
UI Components → ProjectionAdapter interface → MockProjectionAdapter (now)
                                            → RealProjectionAdapter (later)
```

The adapter boundary enforces:
- UI components render projection data and submit player intent only
- UI does NOT own semantic interpretation (construction detection is mock-only)
- UI does NOT own world mutation (all state changes go through adapter)
- MockProjectionAdapter simulates backend behavior — all mock semantics are labeled
- RealProjectionAdapter documents future endpoints — not yet implemented

## Core Boundary

**This UI is a Projection API-compatible renderer. It does not own world truth or outcomes.**

The UI consumes only Projection API compatible mock data. It never directly reads WorldState, true_state, hidden IDs, backend scores, or raw traces.

## Spatial Objects Are Data-Driven WorldObjects

Buildings and facilities are **not hardcoded frontend components**. All spatial objects are rendered through a generic `ObjectRenderer` that consumes:

- `object_type` → sprite/color selection
- `render_asset_ref` → asset reference
- `footprint_tiles` → position and extent on grid
- `height_layer` → visual elevation
- `physical_status` → status overlay color
- `governance_status` → governance badge
- `available_visible_intents` → action buttons

No `<Shed />`, `<Playground />`, `<PropertyOffice />`, or similar components exist in the codebase. Object types influence visual style but not component identity.

## AI-Generated Buildings Pipeline

Future AI-generated buildings will enter through:
1. Proposal preview (dashed overlay + disclaimer)
2. World validation + asset pipeline
3. Committed to visible_spatial_objects

They will **never** enter through direct UI mutation.

## Data Sources (Mock → Real Mapping)

| Mock View | Real Projection API Equivalent |
|---|---|
| `visible_scene_grid` | Scene grid from projection API |
| `visible_tiles` | Tile data from world state |
| `visible_spatial_objects` | WorldObject projection views |
| `visible_spatial_proposals` | Proposal projection views |
| `visible_actors` | SocialNode projection views |
| `visible_presence` | Player presence context |
| `visible_speech_events` | Speech event log |
| `visible_assistant_inbox` | R101 inbox |
| `visible_self_actions` | Self-action redirect log |
| `visible_interactions` | Interaction log |
| `visible_availability` | Actor availability/consent |
| `visible_clues` | Player knowledge records |
| `visible_norms` | Normative object records |
| `visible_snapshot` | Projection API snapshot |

## R101 States

| State | Description |
|---|---|
| `inactive` | R101 not activated — direct speech to focused actor |
| `assistant_panel_active` | Assistant panel active — inbox routing |
| `remote_contact_active` | Remote contact — remote inbox |
| `present_as_mediator` | Present as neutral mediator |
| `recording_requested` | Recording mode requested |

R101 is an **activatable proxy**, not the player's default mouth. R101 does not listen globally when inactive.

## Speech Radius

`SpeechRadiusOverlay` is a **visible projection hint only**. It does not imply guaranteed actual hearing.

## UI Actions (Intent Only)

| UI Action | Sends | Never Does |
|---|---|---|
| `set_focus(actor_or_object_ref)` | Focus intent | Does not reveal hidden state |
| `unset_focus()` | Clear focus | — |
| `set_r101_state(state)` | Toggle intent | Does not change R101 actor internals |
| `set_speech_mode(mode)` | Mode intent | Does not change world audio |
| `submit_player_input(text)` | Player text intent | Does not mutate world directly |
| `request_snapshot()` | Snapshot request | Read-only |
| `submit_visible_intent(intent, target)` | Intent submission | Intent only, no outcome |

## Forbidden Actions

The following are **permanently blocked**:

- `punish_actor()` — No direct punishment
- `confirm_truth()` — No truth confirmation shortcut
- `complete_task()` — No task completion shortcut
- `force_confession()` — No forced confession
- `build_object_directly()` — No direct construction
- `demolish_object_directly()` — No direct demolition
- `change_trust_directly()` — No direct trust mutation
- `change_authority_directly()` — No direct authority mutation
- `reveal_hidden_state()` — No hidden state exposure
- `mark_confession_true()` — No confession marking
- `approve_project_without_world_validation()` — No bypass of world validation

## Speech Mode → Audible Scope

| Speech Mode | Audible Scope | Visual Indicator |
|---|---|---|
| `whisper` | private / small radius | 🟣 whisper badge |
| `normal` | local | 🔵 normal badge |
| `raised` | room | 🟠 raised badge |
| `announcement` | public | 🔴 announcement badge |

## Proposal Previews

Proposals must remain visually distinct from completed construction:
- Dashed outline (not solid fill)
- "未建成 — 提案阶段" / "仅提案预览" disclaimer
- Status badges: `proposal_logged`, `not_built`, `needs_review`

## Uncertainty Language

- "疑似" (suspected) — not "确认"
- "弱怀疑" (weak_suspicion) — not "已知违规"
- "需要核查" (needs_audit) — not "已证实"
- Never: raw scores, backend IDs, hidden summaries, semantic tags
