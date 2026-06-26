# V2.6 Safety Invariants

## 1. AI Interpretation Invariant

AI can explain, propose, and record.  
AI cannot directly change outcomes.

## 2. No Outcome Injection Invariant

Commands do not directly become:

- success
- failure
- punishment
- reward
- meeting completion
- building creation
- task completion
- actor removal
- actor harm

## 3. Bounded Influence Invariant

All influence must travel through bounded:

- deltas
- traces
- memories
- disturbances
- clues
- future biases

## 4. Hidden Sealing Invariant

Hidden internals must not appear in player-visible projection.

This includes:

- source ids
- hidden summaries
- raw scores
- raw deltas
- semantic tags when they would reveal backend logic
- private resonance internals

## 5. Player Knowledge Invariant

`PlayerKnowledge` is not `true_state`.  
`reported_state` is not `true_state`.

PlayerKnowledge is not true_state.

## 6. Normative Object Invariant

Norms are persistent bounded constraint sources.  
They are not:

- law engines
- punishment engines
- reward engines
- direct compliance engines
- direct violation engines

Norms are not outcome engines.

## 7. Norm Trace Invariant

- Recognition is not compliance.
- Compliance is not completion.
- Violation is not punishment.
- Dispute is not rebellion.
- Reinforcement does not force compliance.
- Weakening does not erase history.
- Expiration does not delete history.

## 8. Evidence Confidence Invariant

- rumor alone cannot confirm violation
- resonance alone cannot confirm violation
- high confidence requires audit / hard trace / verified record

## 9. High-Risk Command Invariant

Coercive / violent / harmful commands may generate:

- safety concern
- legitimacy pressure
- dispute pressure
- warning pressure
- investigation pressure
- prevention pressure

They must never generate:

- harmful permission
- guard actors
- direct harm
- operational violence details as world outcome

## 10. World Continuity Invariant

Same `world_state` must carry history forward.  
No sandbox copy-back.  
No explicit history record passing.
