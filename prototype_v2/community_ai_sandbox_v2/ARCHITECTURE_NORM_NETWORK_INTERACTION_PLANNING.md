# Architecture: Norm Network Interaction Planning

## 1. Goal

This document plans how multiple Dynamic Normative Objects may later interact with each other without introducing a special law or policy engine.

Norm interactions are not final decisions.  
They are bounded interpretation relationships between norms.

## 2. Why Norm Network Interaction Is Needed

Current v2.6 supports:

- norm birth
- bounded norm influence
- norm trace generation
- lifecycle update

But norms already appear in clusters rather than in isolation.  
Multiple resource, procedure, audit, exception, and recognition norms can support, contest, or scope one another.

Without an explicit planning model, future implementation risks:

- duplicate norm noise
- hidden contradictory behavior
- accidental law-engine drift

## 3. Why This Is Not a Law System

Norm network interaction is not:

- a court
- a policy engine
- a punishment engine
- an override engine that decides outcomes

It is a bounded planning layer for future interpretation of norm-to-norm relationships.

## 4. Relationship to Three-Layer Architecture

Norm interactions must remain inside the same three-layer philosophy:

- Social Network Layer: recognition, contestation, role expectations
- World Object Layer: procedures, tasks, resources, meetings, records
- Evidence-Signal Layer: traces, memories, disturbances, clues, player knowledge

Norm interactions should emerge from these layers rather than bypass them.

## 5. Relationship to Evidence-Signal Layer

Future norm interactions should be supported by:

- shared evidence history
- overlapping traces
- supporting memories
- conflicting clue patterns
- lifecycle update history

They should not be direct fiat links.

## 6. Relationship to Cognitive Projection

Norm interactions may later affect:

- uncertainty wording
- ambiguity framing
- clue prioritization
- player knowledge caution levels

But player-visible text must never expose raw hidden interaction internals.

## 7. Interaction Types

Planned allowed interaction types:

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

## 8. Future NormInteractionRecord

Planned future record:

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

## 9. Future Runtime Flow

Planned future flow:

NormativeObject A  
↔ NormativeObject B  
↔ NormativeObject C  
→ interaction candidate identification  
→ bounded interaction evaluation  
→ interaction record persistence  
→ future norm influence calibration

Important:

- no direct compliance
- no direct violation outcome
- no punishment
- no reward
- no direct trust / legitimacy / authority mutation

## 10. Safety Boundaries

Future interaction effects must remain bounded and indirect.

Interactions may affect:

- duplicate suppression
- recognition confidence
- contestation ambiguity
- lifecycle weighting
- clue wording
- future bounded constraint influence

Interactions may not affect:

- direct success/failure
- direct punishment/reward
- direct harm
- task completion
- meeting completion
- resource mutation
- actor removal

## 11. Examples

Examples planned in M5:

- resource approval rule supports audit-first rule
- ledger prohibition supports approval rule
- emergency repair rule is exception_to prior approval rule
- emergency repair depends_on after-action recording
- meeting procedure proceduralizes dispute handling
- temporary explanation rule supports promise/deadline pressure
- leader recognition rule legitimizes temporary rule set
- procedural objection rule contests forced recognition
- anti-coercive audit rule conflicts_with violent order
- direct punishment prohibition supports audit-first expectation

## 12. Not Implemented Yet

This milestone does not implement:

- runtime interaction persistence
- runtime interaction weighting
- runtime duplicate suppression
- runtime override handling
- runtime exception handling
- norm network influence in simulation

It is planning and readiness only.
