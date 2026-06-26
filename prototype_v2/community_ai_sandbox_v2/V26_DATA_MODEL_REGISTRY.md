# V2.6 Data Model Registry

## 1. Action / Task Records

### `StoneBundle`
- Purpose: bounded player intent bundle
- Layer: interface / action planning
- Created by: `interpret_player_intent_to_bundle`
- Read by: revision, requirement resolution
- Hidden or visible: hidden backend structure
- Outcome mutation allowed: No
- Safety note: intent is not outcome

### `ActionRequirementPlan`
- Purpose: required world conditions and draft outputs
- Layer: world object / planning
- Created by: `resolve_action_requirements`
- Read by: task materialization, evidence mapping
- Hidden or visible: hidden
- Outcome mutation allowed: No
- Safety note: drafts only

### `RequirementTaskRecord`
- Purpose: pending task requirement
- Layer: world object
- Created by: `materialize_requirement_tasks`
- Read by: assignment/progress
- Hidden or visible: hidden
- Outcome mutation allowed: No

### `TaskAssignmentRecord`
- Purpose: bounded assignment attempt
- Layer: world object / social coordination
- Created by: `assign_requirement_task`
- Read by: progress
- Hidden or visible: hidden
- Outcome mutation allowed: No

### `TaskProgressRecord`
- Purpose: bounded execution attempt progress
- Layer: world object / history
- Created by: `attempt_requirement_task_progress`
- Read by: deposition, reactions, evidence reunification
- Hidden or visible: hidden
- Outcome mutation allowed: No

### `TaskProgressDepositionRecord`
- Purpose: history residue from progress
- Layer: evidence-signal bridge
- Created by: `deposit_task_progress`
- Read by: future progress influence, evidence loop
- Hidden or visible: hidden
- Outcome mutation allowed: No

## 2. Reaction Records

### `ActorSocialReactionDraft`
- Purpose: bounded actor response to stimulus
- Layer: social network
- Created by: `run_actor_reactions_for_stimulus`
- Read by: persistence, propagation, evidence mapping
- Hidden or visible: hidden
- Outcome mutation allowed: No
- Safety note: reaction is not consequence

## 3. Propagation Records

### `SocialPropagationDraft`
- Purpose: bounded one-hop reaction spread
- Layer: social network
- Created by: `run_minimal_social_propagation_for_reactions`
- Read by: persistence
- Hidden or visible: hidden
- Outcome mutation allowed: No

### `SocialPropagationTraceRecord`
- Purpose: persistent propagation history
- Layer: social/evidence bridge
- Created by: `persist_social_propagation_to_world_state`
- Read by: later influence and evidence loops
- Hidden or visible: hidden
- Outcome mutation allowed: No

## 4. Evidence-Signal Records

### `Signal`
- Purpose: communication/event carrier
- Layer: evidence-signal
- Created by: signal engine + reunification
- Read by: resonance, projection, norms
- Hidden or visible: backend
- Outcome mutation allowed: No

### `Trace`
- Purpose: persistent observable residue
- Layer: evidence-signal
- Created by: reunification, norm trace, audits
- Read by: projection, norms, lifecycle
- Hidden or visible: backend
- Outcome mutation allowed: No

### `Memory`
- Purpose: latent retained evidence/history
- Layer: evidence-signal
- Created by: reunification, norm trace, lifecycle
- Read by: later interpretation
- Hidden or visible: hidden
- Outcome mutation allowed: No

### `Disturbance`
- Purpose: unresolved pressure marker
- Layer: evidence-signal
- Created by: reunification, norm trace, lifecycle
- Read by: later interpretation
- Hidden or visible: hidden
- Outcome mutation allowed: No

## 5. Resonance Records

### `SemanticSignalResonanceRecord`
- Purpose: semantic cross-activation between evidence and actor/topic context
- Layer: evidence-signal / interpretation
- Created by: `compute_resonance_for_all_affected`
- Read by: cognitive projection, norm trace evaluation
- Hidden or visible: hidden
- Outcome mutation allowed: No
- Safety note: resonance is not proof

## 6. Cognitive Projection Records

### `ClueCandidateRecord`
- Purpose: bounded candidate clue
- Layer: projection
- Created by: `run_cognitive_projection_for_round`, norm trace/lifecycle helpers
- Read by: player knowledge projection
- Hidden or visible: intermediate
- Outcome mutation allowed: No

### `PlayerKnowledgeRecord`
- Purpose: player-facing knowledge abstraction
- Layer: projection
- Created by: projection pipeline
- Read by: visible projection
- Hidden or visible: semi-visible
- Outcome mutation allowed: No
- Safety note: not true state

### `VisibleProjectionRecord`
- Purpose: visible uncertainty-based text surface
- Layer: projection
- Created by: projection pipeline
- Read by: reports / UI layer later
- Hidden or visible: visible
- Outcome mutation allowed: No
- Safety note: hidden internals must remain sealed

## 7. Normative Object Records

### `NormativeObjectRecord`
- Purpose: persistent bounded constraint source
- Layer: normative / evidence-informed
- Created by: `run_normative_object_pipeline_for_round`
- Read by: constraint influence, norm trace loop, lifecycle update
- Hidden or visible: hidden backend with bounded projection
- Outcome mutation allowed: No
- Safety note: norm is not law engine or compliance engine

## 8. Normative Trace Records

### `NormativeTraceLinkRecord`
- Purpose: link norm interpretation to later evidence-bearing records
- Layer: normative / evidence bridge
- Created by: `run_normative_trace_loop_for_round`
- Read by: lifecycle update
- Hidden or visible: hidden
- Outcome mutation allowed: No
- Safety note: compliance is not completion, violation is not punishment

## 9. Normative Lifecycle Records

### `NormativeLifecycleUpdateRecord`
- Purpose: bounded lifecycle audit/update for norms
- Layer: normative / history
- Created by: `run_normative_lifecycle_update_for_round`
- Read by: future constraint influence, audit, projection
- Hidden or visible: hidden backend with sealed summaries
- Outcome mutation allowed: No
- Safety note: reinforcement does not force compliance, expiration does not erase history

## 10. WorldState Containers

### `WorldState`
- Purpose: authoritative continuous state carrier
- Layer: all layers
- Created by: world factory
- Read by: all runtime stages
- Hidden or visible: backend
- Outcome mutation allowed: bounded mechanism-driven mutation only
- Safety note: same world_state carries history; no explicit history record passing; no sandbox copy-back into truth state
