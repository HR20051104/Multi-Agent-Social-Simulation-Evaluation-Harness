# V2.6 Norm Network Interaction Spec

## 1. Allowed Interaction Types

- `supports`
- `conflicts_with`
- `overrides`
- `depends_on`
- `scopes`
- `duplicates`
- `weakens`
- `reinforces`
- `proceduralizes`
- `legitimizes`
- `contests`
- `supersedes`
- `exception_to`

## 2. Planned Future Record

### `NormInteractionRecord`

Planned fields:

- `interaction_id`
- `source_norm_id`
- `target_norm_id`
- `interaction_type`
- `interaction_strength`
- `confidence_score`
- `source_evidence_ids`
- `source_trace_ids`
- `source_memory_ids`
- `source_lifecycle_update_ids`
- `shared_scope_tags`
- `conflicting_scope_tags`
- `reason_summary`
- `bounded_effect_preview`
- `visibility_scope`
- `sealed_from_player_report`
- `created_tick`
- `source`

Planned future `WorldState` container:

- `norm_interaction_records`

## 3. Planned Future Helper Names

- `identify_norm_interaction_candidates`
- `evaluate_norm_interaction_type`
- `persist_norm_interaction_record`
- `compute_norm_network_constraint_influence`
- `project_norm_interaction_to_clue`
- `run_norm_network_interaction_pipeline_for_round`

These names are planning references only.  
They are not implemented in runtime by M5.

## 4. Planned Runtime Order

Future intended placement:

norm birth  
→ norm trace loop  
→ norm lifecycle update  
→ norm interaction candidate identification  
→ norm interaction evaluation  
→ bounded interaction record persistence  
→ future norm-network-aware influence

## 5. Planned Integration Points

Norm interactions may later influence:

- norm candidate merging
- duplicate suppression
- recognition calculation
- contestation calculation
- lifecycle update weighting
- constraint influence calibration
- clue wording
- player knowledge uncertainty

## 6. Planned Test Strategy

Future runtime tests should verify:

- supports increases bounded confidence only
- conflicts increase ambiguity / contestation only
- exception lowers violation confidence only when exception conditions are plausible
- proceduralization routes interpretation through procedure without declaring outcomes
- supersession never deletes history directly
- duplicates do not silently merge without audit logic

## 7. Future Migration Notes

- keep interaction records thin and evidence-linked
- do not create special law / policy / court systems
- preserve hidden sealing
- keep player-visible projection uncertainty-based
- preserve outcome-injection safeguards
