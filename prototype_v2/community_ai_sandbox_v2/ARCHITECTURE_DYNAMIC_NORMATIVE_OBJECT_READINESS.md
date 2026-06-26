# Dynamic Normative Object Architecture Readiness

## 1. Definition

**Dynamic Normative Object:**
A world object formed from socially recognized signals, policies, promises, roles, rules, or procedures, which persists as a constraint source and influences future tasks, reactions, evidence, resonance, and cognitive projection without directly deciding outcomes.

动态规范对象：由被社会承认的信号、政策、承诺、职位、规则或程序沉积而成的世界对象；它作为持续约束源影响未来任务、反应、证据、语义共振和玩家认知，但不能直接决定结果。

## 2. Norms Are Not Modules

Norms are not special standalone systems. They are:

1. **World Object Layer carriers** — persistent records that constrain future actions.
2. **Evidence-Signal Memory** — recognized signals, memories, traces that give the norm social weight.
3. **Social Recognition** — SocialNode/SocialEdge changes that reflect compliance, resistance, bypassing.
4. **Cognitive Projection** — player sees reported enforcement, violation traces, disputes through clues/knowledge.

## 3. Normative Object Lifecycle (v2.6 planning)

```
proposed_signal
  → recognized_signal
  → provisional_norm_memory
  → normative_object_candidate
  → bounded_constraint_source
  → enforcement / violation / dispute traces
  → player knowledge projection
  → reinforcement / decay / contestation
```

## 4. Mapping to v2.5.16 Architecture

| Normative concept | Signal/Trace/Memory | WorldObject carrier | Social Layer | Cognitive Projection |
|-------------------|---------------------|---------------------|--------------|---------------------|
| obligation | procedural_pressure, accountability | Task/Expectation | compliance_tendency | report/audit clue |
| prohibition | prohibition, access_constraint | Document/Resource | concealment_tendency | violation trace clue |
| promise | promise signal, deadline | Expectation record | trust (A→CHIEF only) | fulfillment/delay clue |
| policy | policy_pressure, procedural_expectation | Rule/Policy draft | recognition, compliance | enforcement report |
| procedural authority | procedural_pressure, coordination | Position/Role | authority_centrality | meeting statement clue |
| access rule | access_constraint, resource_accountability | Resource ledger | resource_control_score | anomaly trace clue |
| enforcement | accountability_pressure, audit_pressure | Task/Investigation | fear, obedience | audit result clue |
| violation trace | violation_trace, resource_anomaly | Trace on WorldObject | concealment, resentment | weak_clue → suspicion |
| disputed recognition | legitimacy_pressure, procedural_caution | Position constraint | contestation edge | disputed status clue |

## 5. Forbidden Design

```
command → norm exists → direct compliance     ❌
violation → direct punishment                 ❌
promise → direct trust mutation               ❌
law → direct legitimacy mutation              ❌
```

## 6. Correct Design

```
command → signal
signal → recognition / memory
memory + world object → normative object
norm → bounded future influence
violation → trace / clue / reaction
player sees projected evidence
outcome emerges through future chains
```

## 7. High-Risk Safety Rule

Normative objects involving violence, coercion, exclusion, punishment, confinement, or harmful enforcement must only generate safety concern, legitimacy pressure, refusal risk, warning, investigation, and prevention chains.

They must not generate operational harm or direct harm outcomes.
