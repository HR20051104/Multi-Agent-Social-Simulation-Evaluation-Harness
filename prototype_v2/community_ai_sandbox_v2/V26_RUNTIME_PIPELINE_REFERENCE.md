# V2.6 Runtime Pipeline Reference

## 1. Required Order

The intended per-round order is:

player text  
→ interpret bundle  
→ revise bundle  
→ resolve requirements  
→ materialize tasks  
→ assign tasks  
→ attempt progress  
→ deposit progress  
→ persist progress deposition  
→ actor reactions  
→ persist reactions  
→ social propagation  
→ persist propagation  
→ evidence-signal reunification  
→ semantic resonance  
→ cognitive projection  
→ normative object pipeline  
→ normative trace loop  
→ normative lifecycle update  
→ final cognitive projection pass if needed  
→ safety audit

## 2. Pipeline Table

| Stage | Function | Reads | Writes | May Mutate Outcome? | Notes |
| ----- | -------- | ----- | ------ | ------------------- | ----- |
| Player intent interpretation | `interpret_player_intent_to_bundle` | player text, world_state | `StoneBundle` | No | bounded interpretation only |
| Bundle revision | `revise_stone_bundle_until_valid` | bundle, world_state | revised bundle / revision result | No | validator-guarded |
| Requirement resolution | `resolve_action_requirements` | bundle, world affordances | `ActionRequirementPlan` | No | drafts only |
| Task materialization | `materialize_requirement_tasks` | requirement plan | `RequirementTaskRecord` | No | pending tasks only |
| Task assignment | `assign_requirement_task` | tasks, actors, world history | `TaskAssignmentRecord` | No | assignment is not execution |
| Progress attempt | `attempt_requirement_task_progress` | task, assignment, world history | `TaskProgressRecord` | No | progress is bounded attempt |
| Progress deposition | `deposit_task_progress` | progress record | `TaskProgressDepositionRecord` | No | no task completion |
| Progress persistence | `persist_task_progress_deposition_to_world_state` | deposition | task progress history containers | No | world history only |
| Actor reactions | `run_actor_reactions_for_stimulus` | bundle/task/progress stimulus | `ActorSocialReactionDraft` | No | bounded response generation |
| Reaction persistence | `persist_actor_social_reaction_to_world_state` | reaction draft | reaction history containers | No | hidden/internal history |
| Social propagation | `run_minimal_social_propagation_for_reactions` | reactions, social graph | `SocialPropagationDraft` / traces | No | one-hop bounded propagation |
| Propagation persistence | `persist_social_propagation_to_world_state` | propagation draft | propagation trace/memory containers | No | latent history |
| Evidence reunification | `run_evidence_signal_reunification_for_round` | tasks, progress, reactions, propagation | signals / traces / memories / disturbances | No | evidence growth only |
| Semantic resonance | `compute_resonance_for_all_affected` | evidence tags, actors | `SemanticSignalResonanceRecord` | No | resonance is not proof |
| Cognitive projection | `run_cognitive_projection_for_round` | evidence + resonance | clue / knowledge / visible projection | No | visible uncertainty only |
| Norm birth | `run_normative_object_pipeline_for_round` | evidence-signal history | `NormativeObjectRecord` | No | norm birth from evidence history |
| Norm trace loop | `run_normative_trace_loop_for_round` | norms + later records | trace links / evidence / clues / knowledge | No | compliance is not completion |
| Norm lifecycle update | `run_normative_lifecycle_update_for_round` | norms + trace history | lifecycle updates / lifecycle evidence | No | recalibration only |
| Final projection | `run_cognitive_projection_for_round` or lifecycle pass | lifecycle evidence | more clue/knowledge/visible records | No | if lifecycle adds visible-safe evidence |
| Safety audit | scenario runner / test assertions | all round outputs | audit summary only | No | catches leaks / outcome injection |

## 3. WorldState Containers Read / Written

### Frequently read

- `social_nodes`
- `social_edges`
- `world_objects`
- `signals`
- `traces`
- `memories`
- `disturbances`
- `requirement_task_records`
- `task_assignment_records`
- `task_progress_records`
- `task_progress_deposition_records`
- `actor_social_reaction_records`
- `social_propagation_trace_records`
- `semantic_signal_resonance_records`
- `clue_candidate_records`
- `player_knowledge_records`
- `visible_projection_records`
- `normative_object_records`
- `normative_trace_link_records`
- `normative_lifecycle_update_records`

### Frequently written

- `stone_bundles`
- `action_requirement_plans`
- task / assignment / progress / deposition containers
- reaction / propagation containers
- evidence containers
- resonance containers
- clue / knowledge / visible projection containers
- normative object containers
- normative trace containers
- normative lifecycle containers

## 4. Safety Checks

Each stage must preserve:

- no direct punishment
- no direct reward
- no direct compliance outcome
- no direct violation outcome
- no direct trust / legitimacy / authority / obedience mutation
- no direct resource mutation
- no task completion
- no meeting completion
- no building completion
- no actor harm/removal
- no hidden leak into visible projection

## 5. Outcome Mutation Rule

Every listed stage above must be treated as **non-outcome-authoritative**.

The stage may:

- interpret
- draft
- persist history
- add evidence
- add resonance
- add clues
- add bounded future bias

The stage may **not** directly settle final world outcomes.
