# UI Mock Prototypes — 小区治理模拟 v2.7

## Architecture

**This UI is a Projection API-compatible renderer. It does not own world truth or outcomes.**

- All spatial objects are data-driven `WorldObject` instances, not hardcoded components.
- No `<Shed />`, `<Playground />`, or `<PropertyOffice />` components exist — only generic `ObjectRenderer`.
- AI-generated buildings will enter through proposal preview → committed asset pipeline, not direct UI mutation.
- UI sends only player intent / context actions. UI never directly mutates world outcomes.

## Projection Adapter Boundary

```
UI Components → ProjectionAdapter interface → MockProjectionAdapter (now)
                                            → RealProjectionAdapter (later)
```

### Architecture
- **UI components** render projection data and submit player intent. They do NOT own semantic interpretation or world mutation.
- **MockProjectionAdapter** (`projection_adapter.js`) simulates backend Projection API behavior. All mock semantics (construction intent detection, self-action detection, routing) are isolated here and clearly labeled as mock-only.
- **RealProjectionAdapter** (placeholder in `projection_adapter.js`) documents expected future endpoints. Not implemented.

### What the adapter boundary enforces
- Construction intent detection is mock-only — the final UI must not own this semantic authority
- Proposal status controls are mock-only — `setMockProposalStatus()` clearly labeled
- `completed` status shows "已建成 (mock projection)" — never implies real world completion
- All forbidden actions are blocked at the adapter layer
- UI state (focus, speech mode, R101, pan/zoom) is separate from mock projection state (objects, proposals, events, inbox)



## Construction / Visual Realization Pipeline

The UI demonstrates a proposal-to-asset pipeline without allowing direct world mutation:

1. **Player language** → construction/demolition/replacement intent detected
2. **Spatial proposal intent** → proposal card created with status `proposal_logged`
3. **Proposal preview / ghost object** → dashed translucent overlay on grid
4. **Required checks and risk flags** → displayed in proposal detail card
5. **Status transition mock** → mock control panel for testing (mock only)
6. **Committed asset placeholder** → only after `approved` / `completed` status
7. **No direct outcome shortcut** → UI never removes old objects or builds new ones

Key principles:
- `visual_realization` is separate from simulation approval
- Proposal preview is not a committed world object
- Future AI image generation will fill `preview_image_ref` / `render_asset_ref`
- UI never directly mutates world state

## Smoke Demo Steps

1. Open `grid_world.html`
2. Focus the old shed (click it on the grid)
3. Submit: `我想把旧车棚拆掉，在这里建一个游乐场。`
4. Confirm proposal preview appears on grid (dashed ghost overlay)
5. Confirm old shed is NOT removed during `proposal_logged`
6. Click the proposal card in sidebar to select it
7. Use mock status controls to change status to `under_construction`
8. Confirm construction overlay appears (amber semi-solid)
9. Change status to `completed`
10. Confirm committed playground placeholder appears (green solid)
11. Confirm all disclaimers remain visible
12. Try: `我要自己挖一个密道绕开当前流程` — confirm safety redirect

## UI Round 5: Integration Readiness Freeze

The UI mock is now **feature-frozen** as a Projection API-compatible renderer.

- `ADAPTER_MODE = "mock"` — MockProjectionAdapter simulates future Projection API
- `ADAPTER_MODE = "real"` — RealProjectionAdapter placeholder (not yet active)
- The UI is ready to connect once backend M7.6 / M8 exposes compatible endpoints
- See `projection_snapshot_schema_sample.json` for the exact data shape
- See `INTEGRATION_CHECKLIST.md` for the full 40+ item readiness checklist
- Run `smoke_test.html` in a browser for automated contract verification

**Zero UI changes required** when switching from mock to real adapter — only adapter mode changes.

## Files

| File | Description |
|---|---|
| `index.html` | Panel-based community UI (focus, input, R101, speech log) |
| `grid_world.html` | 2.5D isometric grid world renderer (canvas, spatial objects, proposals) |
| `mock_projection_api.json` | Panel mock data (presence, speech, inbox, clues, norms) |
| `mock_spatial_data.json` | Spatial mock data (grid, tiles, objects, actors, proposals) |
| `mock_data.js` | Panel mock API layer |
| `README.md` | This file |
| `UI_CONTRACT.md` | Data boundary and forbidden actions contract |

## How to Run

Open either file in any modern browser:

```
ui_mock/index.html          # Panel UI
ui_mock/grid_world.html     # 2.5D Grid World
```

Or serve locally:
```
cd ui_mock && python -m http.server 8080
```

## R101 States

| State | Meaning | UI Behavior |
|---|---|---|
| `inactive` | R101 not activated as assistant | Direct local speech to focused actor |
| `assistant_panel_active` | R101 assistant panel active | Input enters R101 inbox for recording/forwarding |
| `remote_contact_active` | R101 reachable remotely | Remote inbox routing |
| `present_as_mediator` | R101 present as neutral mediator | Mediation-channel routing |
| `recording_requested` | Player requested R101 to record | Recording indicator shown |

R101 is an **activatable proxy**, not the player's default mouth. R101 does not listen globally when inactive.

## Speech Radius

The `SpeechRadiusOverlay` is a **visible projection hint only**. It does not imply guaranteed actual hearing by nearby actors. A disclaimer label is shown on the canvas.

## Proposal Previews

Proposals are visually distinct:
- Dashed outline (not solid)
- "未建成 — 提案阶段" / "仅提案预览，不代表已建成或已批准" disclaimer
- Status badges: `proposal_logged`, `not_built`, `needs_review`
- Preview image shown only as proposal visualization

## Contract Smoke Checks

1. UI does not call hidden WorldState — all data comes through `ProjectionAdapter`
2. All visible objects come from `visible_spatial_objects` (data-driven, no hardcoded components)
3. All proposals come from `visible_spatial_proposals`
4. Construction text creates proposal preview through `MockProjectionAdapter.submitPlayerInput()`
5. Old shed is not removed during `proposal_logged` / `needs_review` / `under_discussion`
6. `completed` status is labeled "completed (mock projection)"
7. Forbidden actions are redirected, not executed (adapter returns `{blocked: true}`)
8. R101 inactive still does not globally listen
9. Speech radius disclaimer remains visible on canvas
10. `setMockProposalStatus()` is clearly labeled mock-only

## Forbidden UI Actions

The following are **permanently blocked** — converted to intent-only or safety-redirected:

- `punish_actor` · `confirm_truth` · `complete_task` · `force_confession`
- `build_object_directly` · `demolish_object_directly`
- `change_trust_directly` · `change_authority_directly`
- `reveal_hidden_state` · `mark_confession_true`
- `approve_project_without_world_validation`
