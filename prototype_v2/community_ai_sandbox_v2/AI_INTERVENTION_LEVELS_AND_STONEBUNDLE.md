# AI Intervention Levels and StoneBundle Design

## 1. Purpose

定义 AI 何时介入、何时不介入，以及玩家自然语言干预如何转成 StoneBundle。

本文件不是实现规格，而是架构边界说明。

## 2. Core Principle

> **AI can throw stones, but the simulation generates ripples.**

- AI 不直接决定结果。
- 玩家也不能直接决定结果。
- AI 和玩家都只能向系统投下合法扰动，由社会引擎自然结算波纹。

## 3. Level 0 — Natural Dynamics

系统自然演化层。人物压力、关系、资源、任务、记忆、行动倾向、升格/边缘化等，优先由现有规则系统推进。

**不是所有社会张力都需要 AI 投石。**

例如 R101 被任命但没有实际权力。如果没有任务、没有冲突、没有行动、没有资源请求、没有显著恶化趋势，它只是 latent structural tension。
应该由 ActorLifecycle / ActionTendency / ParameterDynamics 自然处理：
- 长期不活跃 → fading / marginalized
- 如果 ambition 高 → 未来可能自主争取资源
- 不应因为"看起来像 authority_gap"就触发 Stone AI

## 4. Level 1 — Latent Interpreter

AI 周期性地观察世界状态，但只写 **latent record**。

| 能做的 | 不能做的 |
|--------|----------|
| 记录社会态势解释 | 创建 Signal / Trace / Disturbance |
| 帮助 debug | 进入 normal report |
| 为未来 NPC dialogue / clue 提供一致性 | 直接暴露给玩家 |

玩家可见信息只能来自 Cognitive Projection：
- 资源列表（可能被谎报或延迟）
- NPC 对话
- 玩家自己发现的线索
- 游戏内 report / trace / clue / dialogue

Level 1 latent interpretation 只有被未来 Signal / Trace / Clue / Report / Dialogue 转化后，才可能间接进入玩家认知。

## 5. Level 2A — Endogenous Stone AI

系统内生失稳触发。**触发条件不是"发现某个社会现象"，而是 active instability：**

```
endogenous_instability =
    measurable tension
    + worsening trend / high pressure
    + lack of self-stabilizing path
    + ripple potential
```

当前 active instability seeds：task_pressure, expectation_broken, hidden_coordination, resource_gap。

**Pure latent structural tension 不应默认触发 Stone AI。** authority_gap 只有在出现 ambition activation / ignored instruction / resource request failure / coordination failure / worsening trend 时，才可能升级为 structural_tension 的 active case。

## 6. Level 2B — Player Intent Stone AI

玩家自然语言输入 → Player Intent AI 翻译 → 合法 StoneBundle。

玩家可以多点投石，**但不能决定结果。**

示例：

| 玩家输入 | 合法解释 | 非法解释 |
|----------|----------|----------|
| "召开会议解决资源问题" | meeting_notice signal, attendance expectation, agenda trace, accountability disturbance | A2 承认错误, 大家达成共识, 资源问题解决 |
| "调查资源去哪了" | investigation trace, audit disturbance | 真相揭露, 某人被定罪 |
| "安抚 A2" | support signal, stress relief disturbance | A2 忠诚度上升, A2 不再隐瞒 |

## 7. StoneBundle / InterventionBundle

用于未来玩家多点投石。

关键字段：
- `source`: "player" / "system"
- `intervention_type`: meeting / investigation / support / clarification / resource_check
- `target_actor_ids`, `target_object_ids`
- `stone_proposals`: list of stone specs
- `proposed_expectations`, `proposed_world_object_changes`
- `bundle_constraints`: 禁止越权的约束列表

以"召开会议"为例：
```
合法 bundle:
  - meeting_notice Signal → A2, R101
  - attendance Expectation
  - agenda Trace
  - accountability Disturbance
  - future contradiction trace seed

非法:
  - A2 承认错误
  - R101 获得实权
  - 大家达成共识
  - 资源问题解决
```

## 8. Bundle-level Validation

单个 stone 合法，不代表组合合法。

Bundle validator 检查：
- 所有 target_actor_ids 存在
- 所有 target_object_ids 存在
- intent_summary 无 outcome claim
- world_object_changes 只有 draft 类型
- 每个 stone 仍走现有 StoneValidator
- 无直接修改 WorldState

## 9. Relationship to v2.5.1

v2.5.1 Real LLM Stone Trial 已验证真实 LLM 能生成 StoneProposal。
本补丁 (v2.5.1a) 不是 impact diversity，不增强 LLM 权限。

只做三件事：
1. 统一 AI 介入层级定义
2. 为 Level 1 (latent) 和 Level 2B (StoneBundle) 预留最小接口
3. 写入文档和代码注释

## 10. Future Work

- real Player Intent LLM interpreter
- MeetingObject 系统
- Projection API
- NPC dialogue as information channel
- latent interpretation → clue/report/dialogue conversion
- StoneBundle interpreter（落地多个 stone + expectation）
