# ARCHITECTURE V2.6 CONSOLIDATED

## 1. Project Philosophy

AI may interpret, draft, and record.  
AI may not directly decide outcomes.  
The world changes only through mechanisms and history.

This project treats AI as a bounded interpretation and proposal layer, not as a direct world-state authority.

## 2. Three-Layer Architecture

### Social Network Layer

- social actors
- social edges
- reactions
- propagation
- recognition / contestation context

### World Object Layer

- resources
- world objects
- tasks
- assignments
- progress
- latent historical state

### Evidence-Signal Layer

- signals
- traces
- memories
- disturbances
- clue candidates
- player knowledge
- visible projection

The normative system sits on top of evidence history rather than bypassing it.

## 3. v2.5 Chain Summary

### Action Chain

Player Intent  
→ StoneBundle  
→ ActionRequirementPlan  
→ RequirementTaskRecord  
→ TaskAssignmentRecord  
→ TaskProgressRecord  
→ TaskProgressDepositionRecord

### Reaction Chain

Stimulus from bundle / task / progress  
→ ActorSocialReactionDraft  
→ reaction persistence  
→ future reaction / assignment / progress bias

### Propagation Chain

Reaction  
→ SocialPropagationDraft  
→ SocialPropagationTraceRecord  
→ propagation memory

### Evidence-Signal Reunification

Tasks, progress, reactions, and propagation deposit into signals / traces / memories / disturbances.

### Semantic Resonance

Signals and evidence can resonate semantically across affected actors and topics.

### Cognitive Projection

Evidence history  
→ ClueCandidateRecord  
→ PlayerKnowledgeRecord  
→ VisibleProjectionRecord

PlayerKnowledge is not true_state.  
reported_state is not true_state.

## 4. v2.6 Dynamic Normative Objects

### Norm Birth

NormativeObjectRecord is born from recognized evidence-signal history.

### Norm Constraint Influence

Norms create bounded reaction / assignment / progress deltas.  
They do not directly create outcomes.

### Norm Trace Loop

Later records can be interpreted relative to norms:

- compliance
- violation
- dispute
- bypass
- attempted_compliance
- ambiguous

### Norm Lifecycle Update

Trace history can:

- reinforce
- weaken
- contest
- decay
- expire

while keeping norms as bounded constraint sources.

### Norm Integration Audit

Milestone 4 verified that the full loop works across continuous world_state with the rest of the architecture.

## 5. Full Runtime Flow

Player Intent  
→ StoneBundle  
→ Requirement / Task  
→ Assignment / Progress / Deposition  
→ Reaction / Propagation  
→ Evidence-Signal  
→ Resonance  
→ Clue / PlayerKnowledge / VisibleProjection  
→ NormativeObject  
→ Norm Alignment / Trace  
→ Norm Lifecycle  
→ Future Influence

## 6. Bounded Influence Principle

Norms, resonance, evidence, clues, and reactions only create bounded deltas, traces, memories, clue pressure, or future biases.

Norms are not outcome engines.

They do not directly create:

- success
- failure
- punishment
- reward
- meeting completion
- building completion
- actor harm
- actor removal

## 7. Hidden vs Visible

### Hidden backend records

- raw traces
- latent memories
- source ids
- resonance internals
- normative lifecycle internals

### Sealed hidden records

These may influence later mechanisms while remaining hidden from visible projection.

### Clue candidates

Intermediate interpretation objects that may become player knowledge.

### Player knowledge

A bounded knowledge surface for the player.  
It is not equivalent to true state.

PlayerKnowledge is not true_state.

### Visible projection

Human-readable uncertainty-based text.  
It must not expose hidden internals.

## 8. Safety Boundary

High-risk coercive commands create:

- safety concern
- legitimacy pressure
- dispute pressure
- warning or investigation pressure

They never create:

- harmful permission
- guard actors
- direct harm outcome
- operational violence outcome

## 9. Current Limits

- no task completion lifecycle yet
- no full UI / projection API yet
- formulas remain rule-based
- norm network interactions remain minimal
- code grew quickly through milestones and may need later modular refactor
