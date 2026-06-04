# PROJECT CONTROL DASHBOARD

> Living Roadmap · 项目总控文件  
> 更新频率：每完成一个版本号更新一次  
> 目标：始终知道在哪、去哪、不做什么

---

## 1. Project Vision / 最终愿景

本项目最终目标是构建一个 **AI 原生社会模拟器**。小区只是第一个场景，不是最终边界。

核心理念：

> **AI 负责扔石头，社会引擎负责生成波纹。**

- 玩家不是点击按钮触发预设结果，而是向一个持续运行的社会系统投放扰动。
- 世界由 Social Network Layer、World Object Layer、Evidence-Signal Layer、WorldClock、ActionIntent、Expectation、Memory、Cognitive Projection 组成。
- AI 不直接决定结果，只负责自然语言理解、行为逻辑生成、报告表达和关键节点穿针引线。
- 社会波纹由底层参数网络、信号传播、资源约束、记忆沉积、认知投影自然结算。

未来可扩展场景包（内核一致）：
- 小区治理（当前）
- 末日避难所
- 公司权斗
- 学校治理
- 空间站
- 王国 / 城邦
- 封闭园区

---

## 2. Current Status / 当前状态

**Current Version:** v2.4.5 completed

**Test Status:**
- pytest: `126 passed, 0 failed`
- 28 个测试文件

**Core Achievements:**
- Dynamic Influence-Signal 三层架构已落地
- WorldClock 持续运行，玩家不操作世界也推进
- Signal propagation / latency / blocking / leakage 已实现
- TaskObject 已下沉为 WorldObject handler
- Player cognitive projection 与 debug_true 已分离
- Promise / request / appointment 已统一为 Expectation
- Expectation 可结算为 fulfilled / partial / delayed / broken / ignored
- Expectation 结果会生成 Memory 并反馈到 ActionTendency
- BackgroundResident（20人）可升格为 SocialNode
- 四条升格路径：appointment / witness / resource_position / self_driven
- Promoted actor 有生命周期：core → active → fading → marginalized
- ActionCandidate 已升级为开放 ActionIntent（16 语义维度）
- 10 个固定 action types 只是 ActionTemplate，不是系统边界
- 长期后果链：conceal→leak, request→disappointment, ally→suspicion, blame→rebound
- **ParameterDynamics 已统一**：快/中/慢三级分类，塑性公式，5 个核心引擎已接入
- centrality/lifecycle/evidence/expectation/action_tendency 的参数更新走统一闸门

**Current Main Risks:**
- 还未接 LLM
- 还未实现动态职位 / 法律 / 制度对象（NormativeObject）
- 还未做 Projection API / 2D UI
- 规模尚未扩展到百人以上
- 低优先级引擎（social_network/event_engine/signal_engine）仍有少量直接参数修改

---

## 3. Version Timeline / 版本时间线

- [x] v2.0 — 三层架构落地（SocialNetwork + WorldObject + EvidenceSignal）
- [x] v2.1 — P0 bug 修复与回归测试（disturbance source attribution, intended_receiver 泄露）
- [x] v2.2 — 关键闭环补完（promise fulfillment, signal blocking/leakage, centrality）
- [x] v2.2.1 — promise / blocking / leakage / report 清洁
- [x] v2.2.2 — 长期因果链验证
- [x] v2.2.3 — 长期中心性与持续表现指标
- [x] v2.3 — Actor Promotion 最小闭环（BackgroundResident → SocialNode, 4 条路径）
- [x] v2.3.1 — Promoted Actor Lifecycle（core/active/fading/marginalized）
- [x] v2.4 — Action Tendency Minimal Loop（10 种 NPC 行动模板）
- [x] v2.4.1 — ActionIntent 抽象 + 行动长期后果链
- [x] v2.4.2 — Expectation Unification（promise/request/appointment 统一）
- [x] v2.4.3 — Expectation → Action Feedback（Memory 反馈到 ActionTendency 评分）
- [x] v2.4.4 — Parameter Dynamics Unification（快/中/慢三级分类，塑性公式）
- [x] v2.4.5 — ParameterDynamics Full Integration Audit（centrality/lifecycle/evidence 接入）
- [ ] v2.5 — LLM natural_logic 小规模接入（当前推荐）
- [ ] v2.6 — Dynamic Normative Objects（动态职位、法律、制度）
- [ ] v2.7 — Projection API / UI 前置接口
- [ ] v2.8 — 100～200 人背景居民压力测试
- [ ] v3.0 — 2D 小区 Demo

---

## 4. Active Stage / 当前阶段

**v2.4.5 — ParameterDynamics Full Integration Audit**

状态：✅ completed

内容：
- centrality_engine：authority/resource/info centrality 通过 apply_delta
- lifecycle_engine：task outcome 和 core_score drift 通过 apply_delta
- evidence_engine：audit consequence 通过 apply_delta
- expectation/action_tendency 已在 v2.4.4 接入
- 参数别名（sustained_core_score_structural → sustained_core_score）

---

## 5. Next Recommended Stage / 下一推荐阶段

### v2.5 — LLM natural_logic 小规模接入

**为什么现在做：**
- ParameterDynamics 已统一，底部物理规则就绪
- ActionIntent 开放语义维度已就绪
- Expectation → Memory → ActionTendency 闭环完整
- 126 tests 全绿
- AI 石头扔进来，波纹不会再乱

**目标：**
- LLM 为 ActionIntent 生成 natural_logic 文本
- LLM 不决定 intent 维度，规则引擎计算 intent space
- LLM 不直接修改世界状态
- 系统仍然通过 Signal/Disturbance/Trace 结算
- 小规模：先接一个 action type（如 report_issue 或 request_resource）

**本阶段不做：**
- 不做自由自然语言命令输入（玩家侧仍用 CLI）
- 不做 2D
- 不做复杂人格系统
- 不让 AI 绕过三层架构

---

## 6. Do-Not-Do-Yet List / 暂缓事项

- [ ] 不要立刻接完整 LLM 自由输入
- [ ] 不要立刻做 2D UI
- [ ] 不要立刻扩展到 1000 人
- [ ] 不要立刻做完整法律/制度系统
- [ ] 不要做完整派系系统
- [ ] 不要做复杂家庭/职业/日程
- [ ] 不要做商业化 DLC 结构
- [ ] 不要让 AI 直接决定世界结果
- [ ] 不要在 Expectation/Parameter 分层未完前新增大型子系统

---

## 7. Core Architecture Map / 核心架构图

```
Player command / NPC autonomous action
        │
        ▼
   ActionIntent  ─────────────────────────────┐
   (semantic dimensions, not fixed enum)       │
        │                                      │
        ├── Signal ──→ propagation /           │
        │    distortion / block / leak          │
        │                                      │
        ├── Disturbance ──→ propagation /      │
        │    decay / superposition              │
        │                                      │
        ├── WorldObject change ──→ Task /      │
        │    Resource / Position / Building     │
        │                                      │
        └── Expectation ◄──────────────────────┘
               │
               ▼
         pending → fulfilled / partial /
         delayed / broken / ignored
               │
               ▼
           Memory  ──→ ActionTendency
           (deposit)    (score modifier)
               │              │
               ▼              ▼
        SocialNode param    Next ActionIntent
        SocialEdge param         │
               │                ▼
               └──────→ 新一轮循环

Player sees: Cognitive Projection (report / knowledge)
Developer sees: debug_true (full hidden state)
```

核心原则：

> **AI can throw stones. The simulation generates ripples.**

---

## 8. Test Status / 测试状态

| 指标 | 值 |
|------|-----|
| Latest pytest | `126 passed, 0 failed` |
| Python version | 3.13.5 |
| 测试文件数 | 26 |
| 测试框架 | pytest 8.3.4 |
| Warning 状态 | PytestCacheWarning (不影响结论) |
| CI/CD | 无（纯本地） |

测试文件清单：

```
tests/test_auto_run.py
tests/test_regressions.py
tests/test_scenarios.py
tests/test_threaded.py
tests/test_v22.py
tests/test_v221.py
tests/test_v222.py
tests/test_v223.py
tests/test_v23_actor_promotion.py
tests/test_v231_promoted_actor_lifecycle.py
tests/test_v24_action_tendency.py
tests/test_v241_action_intent.py
tests/test_v241_action_longterm.py
tests/test_v242_expectation_unification.py
tests/test_v243_expectation_action_feedback.py
tests/test_v244_parameter_dynamics.py
tests/test_v245_parameter_dynamics_integration.py
... (另有 v1 prototype 测试)
```

---

## 9. Open Risks / 当前风险

1. **Parameter Dynamics 尚未统一** — 快/中/慢变量没有总闸门，不同引擎各自改参数
2. **ActionIntent 虽开放，但尚未接 LLM** — natural_logic 目前由规则模板生成
3. **Normative Objects 尚未实现** — 法律/制度/动态职位还只是设计
4. **UI 尚未实现** — 当前仍是 CLI/report/debug
5. **背景居民规模还小** — 20 人，未做百人级压力测试
6. **report 可解释性** — clue dedup 和自然语言摘要需要长期打磨
7. **系统复杂度** — 15 步 tick 管线、13 个引擎模块，每阶段需要全量回归
8. **随机种子敏感性** — 部分测试依赖固定 seed，未做 seed 稳定性扫描

---

## 10. Future Backlog / 未来想法池

以下想法暂不列入当前主线，但值得后续考虑：

**机制层：**
- Dynamic Position / Emergent Role — 职位可被创建、合并、架空
- NormativeObject — Law / Rule / Policy / Institution / Decree
- MeetingObject — 正式会议作为世界对象
- Dual-use facilities — 同一建筑的正反两面用途
- Declared intent vs hidden intent — NPC 公开说和私下想的分离
- Public narrative vs true purpose — 系统叙事层 vs 真实目的层
- Resource agency / informal resource access — 非正式资源获取渠道
- Multi-scale time system — 小时/日/周/季多时间尺度

**AI 层（v2.5+）：**
- LLM natural_logic generator — AI 为 ActionIntent 生成自然语言解释
- LLM action interpreter — AI 解析玩家自然语言命令
- Semantic Action Layer — AI 生成新 ActionIntent 维度组合

**UI 层（v3.0+）：**
- 2D Pokémon-like 地图 UI
- Player presence interrupting secret conversations
- Cognitive Projection API — 只暴露玩家能知道的信息
- Social network visualization — 玩家已知关系图

**场景层（v4.0+）：**
- 末日避难所场景包
- 公司权斗场景包
- 学校治理场景包
- 空间站场景包
- 王国/城邦场景包

---

## 11. Decision Log / 决策记录

| 日期/版本 | 决策 | 原因 |
|-----------|------|------|
| v2.0 | 采用 SocialNetwork + WorldObject + EvidenceSignal 三层架构 | 旧 TaskEngine 中心架构容易写成"任务列表+事件列表" |
| v2.0 | 不刻画 CHIEF 对他人的 trust/preference | 玩家判断由玩家自己完成 |
| v2.3 | BackgroundResident → SocialNode 升格 | 实现"边缘人物进入核心圈" |
| v2.4 | 10 种 action_type 只是 ActionTemplate，不是系统边界 | 为未来 AI 生成行为留接口 |
| v2.4.1 | ActionIntent 作为开放语义维度 | AI 未来可填充 natural_logic 和新方法 |
| v2.4.2 | promise / request / appointment 统一为 Expectation | 避免三种分散实现各自维护 |
| v2.4.3 | Expectation 结果必须反馈到 ActionTendency | 完成 expectation→action 闭环保留 |
| v2.4.4 | 引入 ParameterDynamics 统一快/中/慢变量更新 | 在接 LLM 前建立参数物理规则 |
| v2.4.5 | centrality/lifecycle/evidence 全面接入 ParameterDynamics | 消除绕过统一闸门的参数更新 |
| 持续 | AI 只负责扔石头，社会引擎负责生成波纹 | 核心架构原则 |
| 持续 | UI 只能读取 Cognitive Projection，不能读取后台真相 | 玩家非全知 |
| 当前 | 在接 LLM 前，先统一 Parameter Dynamics | 确保底层参数规则先于 AI 引入 |

---

## 12. Glossary / 术语表

| 术语 | 含义 |
|------|------|
| **Social Network Layer** | 社会网络层：人和组织节点 + 多维关系边 |
| **World Object Layer** | 世界对象层：建筑、资源、任务、职位、文档 |
| **Evidence-Signal Layer** | 证据-信号层：连接前两层的信号/痕迹/线索/记忆/扰动 |
| **Signal** | 信号：可传播、变形、阻断、泄露的信息单位 |
| **Trace** | 痕迹：事件留在世界对象上的客观迹象 |
| **Clue** | 线索：玩家通过渠道发现的带置信度信息 |
| **Disturbance** | 扰动：沿社会网络传播的影响脉冲 |
| **Memory** | 记忆：信号/期望结算后沉积的长期影响 |
| **Expectation** | 期望：未来指向的参数束，统一 promise/request/appointment |
| **ActionIntent** | 行动意图：开放语义维度，非固定枚举 |
| **ActionTemplate** | 行动模板：当前 10 种固定 action_type，是测试用实现 |
| **BackgroundResident** | 背景居民：低分辨率居民池，可升格为 SocialNode |
| **Actor Promotion** | 演员升格：背景居民→社会节点的过程 |
| **Promoted Actor Lifecycle** | 升格后生命周期：core→active→fading→marginalized |
| **Cognitive Projection** | 认知投影：玩家可见的信息，不等于真相 |
| **Parameter Dynamics** | 参数动力学：快/中/慢变量的统一更新规则 |
| **NormativeObject** | 制度对象：法律、规则、政策等持续性制度 |
| **AI throws stones / simulation generates ripples** | 核心设计哲学：AI 提供输入和表达，规则引擎负责结算 |

---

## 13. Update Protocol / 更新规则

每完成一个版本号必须更新本文件：

1. 更新 **Current Status**（版本号、测试数、核心成就）
2. 勾选 **Version Timeline** 对应条目
3. 更新 **Test Status**（pytest 结果）
4. 更新 **Active Stage** 为本阶段内容
5. 更新 **Next Recommended Stage** 为下一推荐
6. 将新想法放入 **Future Backlog**，不直接插入当前主线
7. 将重要架构决定写入 **Decision Log**
8. 如果下一阶段变化，在 Decision Log 中写清原因
9. 提交 git 时引用本文件
