# Integration Readiness Checklist — v2.7 UI Mock

## Round 5: Integration Readiness Freeze

The UI mock is feature-frozen. This checklist verifies it is ready for backend M7.6 / M8 integration as a Projection API-compatible renderer.

---

## 1. Data Boundary

- [x] UI never reads hidden WorldState — all data comes through `ProjectionAdapter`
- [x] UI reads only Projection API-compatible fields (no `true_state`, `hidden_*`, `raw_*`, `source_*_id`)
- [x] UI submits only player input / visible intent / context state
- [x] All spatial objects come from `visible_spatial_objects` (data-driven, no hardcoded components)
- [x] All spatial proposals come from `visible_spatial_proposals`
- [x] All visual assets are refs (`render_asset_ref`, `preview_image_ref`), not world truth

## 2. Semantic Authority

- [x] Construction intent detection is mock-only (`_detectConstructionIntent()` in MockProjectionAdapter, labeled as mock)
- [x] Proposal status controls are mock-only (`setMockProposalStatus()`, labeled "mock only")
- [x] Completed proposal status is labeled "completed (mock projection)" — never implies real world completion
- [x] The adapter comment states: "This simulates future backend / AI semantic parsing. The final UI must not own this semantic authority."

## 3. Forbidden Actions

- [x] `punish_actor` blocked at adapter layer
- [x] `confirm_truth` blocked at adapter layer
- [x] `complete_task` blocked at adapter layer
- [x] `force_confession` blocked at adapter layer
- [x] `build_object_directly` blocked at adapter layer
- [x] `demolish_object_directly` blocked at adapter layer
- [x] `change_trust_directly` blocked at adapter layer
- [x] `change_authority_directly` blocked at adapter layer
- [x] `reveal_hidden_state` blocked at adapter layer
- [x] `approve_project_without_world_validation` blocked at adapter layer

## 4. R101 / Speech Safety

- [x] R101 inactive does not globally listen (sidebar states: `inactive` / `assistant_panel_active`)
- [x] Speech radius is visible hint only (canvas disclaimer: "可见说话范围提示，不代表真实听见结果")
- [x] R101 described as activatable proxy, not default mouth
- [x] R101 inbox messages state R101 can record but not decide or execute

## 5. Construction / Proposal Pipeline

- [x] Player construction language creates proposal preview, not completed object
- [x] Old shed is not removed during `proposal_logged` / `needs_review` / `under_discussion`
- [x] `completed` status shows "已建成 (mock projection)" on grid and "completed (mock)" in sidebar
- [x] Proposal ghost overlay varies by status (dashed, semi-solid, solid, rejected)
- [x] Proposal cards display required checks, risk flags, disclaimer
- [x] Disclaimer text: "提案预览，不代表已建成。该 UI 不直接改变世界对象。"

## 6. Adapter Boundary

- [x] `ADAPTER_MODE` config exists (`"mock"` / `"real"`)
- [x] `MockProjectionAdapter` simulates all 14 visible views + 3 write intents
- [x] `RealProjectionAdapter` placeholder documents expected endpoints (GET /projection/snapshot, POST /player/input, etc.)
- [x] Projection snapshot schema sample (`projection_snapshot_schema_sample.json`) matches UI expectations
- [x] UI state (focus, speech mode, R101, pan/zoom) is separate from mock projection state
- [x] Adapter exposes `resetMockState()` for clean test resets

## 7. Self-Action / Safety Redirects

- [x] Complex physical self-actions (绕开, 密道, 自己挖) are safety-redirected
- [x] Self-action log shows "该行动被转为高风险 self-action intent，不产生直接施工结果"
- [x] Self-action log shows "未提供操作指导"

## 8. Projection Safety Language

- [x] Confidence labels: "suspected", "weak_suspicion" — never "confirmed"
- [x] Uncertainty note: "目前信息不足以确认，建议进一步核查。"
- [x] No raw scores, backend IDs, semantic tags, or hidden summaries in rendered output

## 9. Adapter Mode Readiness

- [x] Setting `ADAPTER_MODE = "real"` will activate RealProjectionAdapter (not yet implemented)
- [x] UI consumes the same interface regardless of mode
- [x] RealProjectionAdapter endpoint shapes are documented

## 10. Documentation

- [x] README describes adapter boundary
- [x] UI_CONTRACT.md describes data sources and forbidden actions
- [x] Smoke demo steps in README
- [x] This checklist exists

---

**Status: READY FOR BACKEND INTEGRATION**

All 40+ checklist items verified. The UI mock is frozen as a Projection API-compatible renderer.
When backend M7.6 / M8 exposes compatible endpoints, set `ADAPTER_MODE = "real"` and implement RealProjectionAdapter.
The UI requires zero changes.
