# Dynamic Influence–Signal Implementation Spec v0.1
# 动态影响-信号三层架构实现规格

> 本文档是给 coding agent / CC 使用的 v2 施工说明书。  
> 它不是世界观文档，也不是玩法宣传文档，而是把 `dynamic_influence_signal_architecture_v0_3.md` 中的三层架构落成可实现的数据结构、引擎流程、tick 顺序、传播规则、测试剧本与验收标准。  
>
> 当前目标：实现一个文本原型 / Rule Mode v2。  
> 暂时不做 2D 图形，不接 LLM API，不做完整开放造物。  
> 重点验证：动态影响-信号网络能否支撑“随时介入、并发扰动、影响传播、隐藏信号、玩家局部认知、边缘节点中心性跃迁”。

---

# 1. 核心目标

实现一个 Python 文本原型，核心不是任务系统，而是：

```text
Social Network Layer      社会网络层
World Object Layer        世界对象层
Evidence-Signal Layer     证据-信号层
World Clock               持续运行时钟
Influence Propagation     影响传播
Signal Propagation        信号传播
Cognitive Projection      玩家认知投影
```

必须验证以下链路：

```text
玩家或 NPC 行动
→ 生成 Signal / Disturbance / Task / WorldObject change
→ 行动可直接作用于人，也可作用于世界对象或信号层
→ 扰动沿社会网络传播
→ 信号沿信息边传播、衰减、变形、阻断、泄露
→ 世界对象留下 trace
→ trace 可能被审计、眼线、巡逻等发现为 clue
→ 玩家只看到到达玩家节点或被发现的认知投影
→ 社会网络边权和节点中心性更新
→ 下一轮行动倾向改变
```

---

# 2. 与旧原型的关系

如果已有旧版 Rule Mode 原型，旧模块不要完全删除，而是下沉。

## 2.1 旧 TaskEngine

旧定位：

```text
任务系统是主骨架
```

新定位：

```text
Task 是 World Object Layer 的一种对象。
任务状态变化会产生 Disturbance、Trace、Signal。
```

## 2.2 旧 EventEngine

旧定位：

```text
后台事件生成器
```

新定位：

```text
Event 是社会网络、世界对象、信号层共同演化后的结果。
事件可以直接影响社会网络，也可以改变世界对象，还可以生成信号或痕迹。
```

## 2.3 旧 EvidenceEngine

旧定位：

```text
隐藏事件 → clue
```

新定位：

```text
管理 Trace / Signal / Clue / Memory 之间的转换。
处理发现概率、置信度、误读、泄露、传播。
```

## 2.4 旧 ReportEngine

旧定位：

```text
生成文本报告
```

新定位：

```text
将高维真实世界投影成玩家可见的信息界面。
不得直接暴露真实后台。
```

---

# 3. 项目建议结构

```text
community_ai_sandbox_v2/
  main.py
  README.md
  data/
    initial_world_v2.json
  src/
    models.py
    world_state.py
    world_clock.py

    social_network.py
    world_objects.py
    signal_layer.py

    action_parser.py
    command_handlers.py

    influence_engine.py
    signal_engine.py
    task_engine.py
    event_engine.py
    evidence_engine.py
    cognition_engine.py
    report_engine.py
    centrality_engine.py
    simulation.py

    utils.py
  tests/
    test_clock.py
    test_direct_social_impact.py
    test_task_as_world_object.py
    test_signal_propagation.py
    test_hidden_signal_leakage.py
    test_centrality_shift.py
    test_wait_without_action.py
```

当前版本可以只使用 Python 标准库：

```text
dataclasses
enum
typing
random
math
json
uuid
```

不要引入复杂框架。

---

# 4. 数据模型总览

v2 至少需要以下核心对象：

```text
WorldState
WorldClock

SocialNode
SocialEdge
SocialNetwork

WorldObject
TaskObject
ResourcePool
PositionObject
DocumentObject

Signal
Trace
Clue
Memory
Disturbance

PlayerKnowledge
VisibleReport
```

---

# 5. WorldClock 世界时钟

## 5.1 定义

世界必须持续运行。玩家不输入命令时，世界仍然推进。

```python
@dataclass
class WorldClock:
    current_tick: int = 0
    current_day: int = 1
    time_of_day: str = "morning"
    tick_length: str = "half_day"
    paused: bool = False
    speed: float = 1.0
```

第一版建议：

```text
1 tick = 半天
2 tick = 1 天
time_of_day = morning / night
```

也可以简化为：

```text
1 tick = 1 day
```

但内部必须保留 tick 概念，后续方便细化。

## 5.2 Tick 推进原则

每个 tick 自动推进：

```text
1. 接收 pending actions
2. 生成 signals / disturbances / world object changes
3. 推进任务与世界对象状态
4. 传播 disturbances
5. 传播 signals
6. 更新 traces / clues / memories
7. 生成后台事件倾向
8. 更新社会网络边权
9. 更新中心性与核心圈状态
10. 更新玩家认知投影
11. 生成可见报告
```

玩家不操作时，也执行第 3 到第 11 步。

---

# 6. WorldState

```python
@dataclass
class WorldState:
    clock: WorldClock

    social_nodes: dict[str, SocialNode]
    social_edges: dict[str, SocialEdge]

    world_objects: dict[str, WorldObject]

    signals: dict[str, Signal]
    traces: dict[str, Trace]
    clues: dict[str, Clue]
    memories: dict[str, Memory]
    disturbances: dict[str, Disturbance]

    player_knowledge: dict[str, PlayerKnowledge]

    history_log: list[str]
    debug_log: list[str]
```

注意：

```text
social_nodes 只存人和组织
world_objects 存建筑、任务、资源、职位、文档等
signals/traces/clues 连接两层
```

---

# 7. Social Network Layer

## 7.1 SocialNode

社会节点只包含人、组织、群体、派系。

```python
@dataclass
class SocialNode:
    id: str
    name: str
    node_type: str          # chief / leader / deputy / resident_group / property / security / faction
    active: bool = True

    # role and identity
    roles: list[str] = field(default_factory=list)
    group_tags: list[str] = field(default_factory=list)

    # psychological state
    stress: float = 0.0
    fear: float = 0.0
    anger: float = 0.0
    hope: float = 50.0
    morale: float = 50.0

    # behavior tendency
    compliance_tendency: float = 50.0
    concealment_tendency: float = 20.0
    cooperation_tendency: float = 50.0
    sabotage_tendency: float = 0.0
    report_honesty: float = 60.0

    # competence and traits
    competence: float = 50.0
    honesty_trait: float = 50.0
    greed_trait: float = 20.0
    risk_tolerance: float = 40.0

    # high-dimensional centralities, updated by CentralityEngine
    authority_centrality: float = 0.0
    information_centrality: float = 0.0
    resource_centrality: float = 0.0
    access_to_chief: float = 0.0
    issue_relevance: float = 0.0
    overall_core_score: float = 0.0

    # memory references
    memory_ids: list[str] = field(default_factory=list)
    known_signal_ids: list[str] = field(default_factory=list)
```

## 7.2 Chief 节点特殊规则

玩家/区长可以作为社会网络中的影响源存在，但系统不要刻画：

```text
chief.trust_to_A
chief.preference_to_B
chief.inner_belief
```

系统可以刻画别人如何看待区长：

```text
A → chief trust
A → chief fear
A → chief obedience
A → chief concealment
```

也就是说：

> 系统刻画“别人怎么看玩家”，不刻画“玩家内心怎么看别人”。

玩家自己的判断由玩家通过报告、线索、会议发言和地图现象自行完成。

---

## 7.3 SocialEdge

```python
@dataclass
class SocialEdge:
    id: str
    source_id: str
    target_id: str

    # relation dimensions
    trust: float = 50.0
    authority: float = 0.0
    obedience: float = 50.0
    fear: float = 0.0
    hostility: float = 0.0
    empathy: float = 0.0
    dependency: float = 0.0
    interest_alignment: float = 0.0
    secrecy: float = 0.0
    competition: float = 0.0
    reputation_weight: float = 0.0

    # information channel dimensions
    information_flow: float = 20.0
    bandwidth: float = 20.0
    latency: int = 1
    distortion: float = 0.1
    visibility: float = 0.5     # public / semi_private / hidden 可映射为数值
    volatility: float = 0.2

    # meta
    tags: list[str] = field(default_factory=list)
    last_updated_tick: int = 0
```

边是有方向的。  
`A -> B` 和 `B -> A` 可以不同。

---

# 8. World Object Layer

## 8.1 WorldObject

世界对象不参与社会心理，不具备 trust/fear/loyalty。

```python
@dataclass
class WorldObject:
    id: str
    name: str
    object_type: str       # building / resource_pool / task / position / document / location / facility
    status: str = "active"

    location: str | None = None
    owner_node_id: str | None = None
    manager_node_id: str | None = None

    visibility: float = 0.5
    condition: float = 100.0
    importance: float = 50.0

    tags: list[str] = field(default_factory=list)
    linked_signal_ids: list[str] = field(default_factory=list)
    linked_trace_ids: list[str] = field(default_factory=list)
```

## 8.2 TaskObject

任务是世界对象的一种。

```python
@dataclass
class TaskObject(WorldObject):
    task_type: str = "generic"
    assignee_node_id: str | None = None
    requester_node_id: str | None = None

    progress_true: float = 0.0
    progress_reported: float = 0.0

    required_budget: int = 0
    reserved_budget: int = 0
    required_materials: int = 0
    reserved_materials: int = 0
    required_labor: int = 0
    reserved_labor: int = 0

    difficulty: float = 50.0
    risk: float = 20.0
    pressure_level: float = 0.0
    deadline_tick: int | None = None

    blocked_reason: str | None = None
    failure_risk: float = 0.0
    false_report_risk: float = 0.0
```

## 8.3 ResourcePool

```python
@dataclass
class ResourcePool(WorldObject):
    resource_type: str = "budget"   # budget / materials / labor / food / energy
    amount_available: float = 0.0
    amount_reserved: float = 0.0
```

## 8.4 PositionObject

职位也是世界对象，不是社会节点。  
担任职位的人是社会节点。

```python
@dataclass
class PositionObject(WorldObject):
    title: str = ""
    holder_node_id: str | None = None
    deputy_node_ids: list[str] = field(default_factory=list)

    permission_tags: list[str] = field(default_factory=list)
    scope: str = ""
    nominal_authority: float = 50.0
    actual_authority: float = 50.0
    accountability: float = 50.0
```

任命职位会：

```text
改变 PositionObject
生成 appointment signal
生成 authority/access/resource 相关 disturbance
更新社会网络中心性
可能引发原权力节点不满
```

---

# 9. Evidence-Signal Layer

## 9.1 Signal

```python
@dataclass
class Signal:
    id: str
    day_created: int
    tick_created: int

    signal_type: str        # order / promise / report / rumor / clue / audit_result / conspiracy ...
    source_node_id: str | None
    intended_receiver_ids: list[str]
    current_holder_ids: list[str]

    content_summary: str
    truth_status: str = "unknown"       # true / false / mixed / unknown
    confidence: float = 0.5

    intensity: float = 0.5
    secrecy_level: float = 0.0
    spread_rate: float = 0.5
    decay_rate: float = 0.1
    distortion_rate: float = 0.1
    memory_strength: float = 0.5

    blocked_by_node_ids: list[str] = field(default_factory=list)
    linked_world_object_ids: list[str] = field(default_factory=list)
    linked_trace_ids: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)
    active: bool = True
```

## 9.2 Trace

Trace 是世界对象或行动留下的客观痕迹。  
Trace 不等于玩家已知线索。

```python
@dataclass
class Trace:
    id: str
    tick_created: int
    trace_type: str        # ledger_anomaly / stock_mismatch / delay / witness / damage / meeting_record
    source_event_id: str | None
    linked_world_object_id: str | None
    location: str | None

    strength: float = 0.5
    decay_rate: float = 0.05
    detectable_by: list[str] = field(default_factory=list)  # audit / patrol / informant / inspection
    discovered: bool = False
```

## 9.3 Clue

Clue 是玩家或某个节点通过渠道获得的线索。

```python
@dataclass
class Clue:
    id: str
    tick_created: int
    source_channel: str       # audit / informant / patrol / meeting / report
    holder_node_id: str       # usually chief if player knows
    related_trace_id: str | None
    related_signal_id: str | None

    content: str
    confidence: float
    source_reliability: float
    misleading_risk: float
    status: str = "unverified"   # unverified / suspected / confirmed / false
```

Clue 文本不得低置信度直接暴露真相。

低置信度：

```text
有匿名信息称材料使用情况可能和进度不匹配，但暂时无法确认。
```

中置信度：

```text
审计发现材料记录与实际盘点存在不一致，需要进一步核查。
```

高置信度：

```text
审计确认该项目有 300 单位材料去向不明，相关签字人为 A2。
```

## 9.4 Memory

Memory 是信号沉积后的长期影响。

```python
@dataclass
class Memory:
    id: str
    holder_node_id: str
    source_signal_id: str
    topic: str
    sentiment: float          # negative to positive, e.g. -1 to 1
    strength: float
    decay_rate: float
    created_tick: int
    last_reinforced_tick: int
```

承诺、失信、公开训斥、救助、背叛，都可以沉积为 memory。

---

# 10. Disturbance 扰动

扰动是作用于社会网络、世界对象或信号层的影响源。

```python
@dataclass
class Disturbance:
    id: str
    tick_created: int

    disturbance_type: str      # coercion / funding / appointment / audit / rumor_burst / resource_shortage
    source_node_id: str | None

    entry_social_node_ids: list[str] = field(default_factory=list)
    entry_world_object_ids: list[str] = field(default_factory=list)
    entry_signal_ids: list[str] = field(default_factory=list)

    intensity: float = 0.5
    duration_ticks: int = 3
    age_ticks: int = 0
    decay_rate: float = 0.2

    propagation_channels: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    active: bool = True
```

扰动不是直接结果。  
例如“强压 A2 建仓库”不是只做 `A2.stress += 20`，而是：

```text
生成 coercion disturbance
入口：A2、task_T1
传播：authority / fear / information_flow / empathy
持续：若干 tick
影响：A2、旁观楼长、相关居民、报告诚实度、任务虚报风险
```

---

# 11. 玩家命令如何进入系统

当前 Rule Mode v2 不接 LLM，使用结构化 CLI 命令。

## 11.1 命令示例

```text
help
status
tick
wait 3
nodes
edges A2
objects
signals
knowledge

assign_task A2 build_storage 1000 20 5
approve_task T1 1000 20 5
force_task T1

appoint A6 position_supply_coordinator
appoint_deputy A3 leader_B2

promise B2 build_garbage_point 4
public_rebuke A2
private_warning A2

audit T1
plant_informant B2

debug_true
quit
```

## 11.2 命令处理原则

玩家命令通常生成：

```text
Signal
Disturbance
WorldObject change
```

例如：

### assign_task

```text
生成 TaskObject
生成 order Signal
生成 responsibility Disturbance
改变 assignee 与 chief 的 authority/obedience 通道
```

### approve_task

```text
改变 ResourcePool
改变 TaskObject reserved resources
生成 funding Disturbance
生成 approval Signal
```

### force_task

```text
生成 coercion Disturbance
生成 pressure Signal
提高任务 pressure_level
```

### appoint

```text
改变 PositionObject
生成 appointment Signal
生成 authority/access Disturbance
更新中心性
```

### promise

```text
生成 promise Signal
不一定立刻改变 WorldObject
相关节点形成期待
```

### public_rebuke

```text
直接作用于社会网络
生成 public_gesture Signal
生成 humiliation/fear Disturbance
旁观节点可能接收信号
```

---

# 12. Tick 推进详细流程

每个 tick 按以下顺序执行。

## Step 0: increment clock

```text
current_tick += 1
更新 current_day / time_of_day
```

## Step 1: process queued player actions

把玩家输入转换为：

```text
Signal
Disturbance
WorldObject changes
```

## Step 2: update world objects

推进任务、资源、建筑、职位等。

### Task update

对每个 TaskObject：

```text
检查资源是否足够
检查 assignee 状态
检查 pressure_level
更新 progress_true
更新 progress_reported
生成 delay trace / progress report signal / false report risk
```

资源不足：

```text
task.blocked_reason = "insufficient_resources"
生成 resource_shortage disturbance
assignee stress 上升
```

压力过高：

```text
false_report_risk 上升
sabotage / breakdown / misuse 倾向上升
```

## Step 3: propagate disturbances

对每个 active Disturbance：

```text
根据 entry points 找到初始节点
沿指定 propagation_channels 传播
按 SocialEdge 强度、latency、decay 计算影响
叠加到节点临时影响缓存
age_ticks += 1
超过 duration 或强度过低则 inactive
```

示例伪代码：

```python
for disturbance in active_disturbances:
    frontier = disturbance.entry_social_node_ids
    for depth in range(max_depth):
        next_frontier = []
        for node in frontier:
            apply_disturbance_effect(node, disturbance, depth)
            for edge in outgoing_edges(node):
                if edge_supports_channel(edge, disturbance.propagation_channels):
                    transmitted = disturbance.intensity * edge_weight(edge) * decay(depth)
                    if transmitted > threshold:
                        queue_effect(edge.target_id, transmitted)
                        next_frontier.append(edge.target_id)
        frontier = next_frontier
```

## Step 4: apply accumulated social effects

将临时影响缓存落到 SocialNode 和 SocialEdge：

```text
stress / fear / anger / morale / concealment_tendency / report_honesty
edge trust / fear / information_flow / secrecy / empathy / hostility
```

注意：

```text
chief 对 others 的 trust 不更新
others 对 chief 的 trust/fear/obedience 可以更新
```

## Step 5: propagate signals

对每个 active Signal：

```text
从 current_holder_ids 出发
沿 information_flow 边传播
受 secrecy_level、blocked_by、edge bandwidth、distortion、latency 影响
更新新 holders
可能产生 distorted signal
可能产生 leak signal
decay signal intensity
```

传播规则建议：

```text
传播概率 =
signal.spread_rate
× edge.information_flow
× edge.bandwidth
× (1 - signal.secrecy_level)
× (1 - edge.distortion)
```

如果 secrecy 高但节点压力高，可能泄露：

```text
leak_probability =
signal.secrecy_level
× holder.stress
× edge.empathy
× random_factor
```

## Step 6: generate traces and clues

Trace 由世界对象异常、任务延迟、账目不一致、公开行为、会议记录等生成。

EvidenceEngine 根据渠道生成 Clue：

```text
audit → ledger_anomaly / stock_mismatch / document trace
informant → private_complaint / conspiracy / rumor
patrol → location anomaly / night activity
meeting → attitude anomaly / silence / contradiction
```

不是所有 trace 都会被发现。  
不是所有 clue 都是真的。  
低置信 clue 必须模糊表达。

## Step 7: generate autonomous events

根据当前网络状态生成后台事件倾向。

不要写成纯随机事件。  
必须来自条件组合。

例子：

### private_complaint

条件：

```text
node.stress 高
node trust_to_chief 低
edge empathy with another node 高
```

### false_report

条件：

```text
task pressure 高
task progress_true 低
assignee report_honesty 低
assignee fear 高
audit risk 低
```

### conspiracy_signal

条件：

```text
A 和 B 对 chief trust 低
A-B secrecy/empathy 高
共同压力源存在
information_flow 高
```

### misuse_resource

条件：

```text
task 有 reserved resources
assignee greed 高
honesty 低
audit visibility 低
pressure 高
```

事件生成后，通常创建：

```text
Signal
Trace
Disturbance
Memory
```

之一或多个。

## Step 8: update memories

信号被节点持有一段时间后，根据 `memory_strength` 沉积为 Memory。

例如：

```text
promise 未兑现 → broken_expectation memory
public_rebuke → humiliation memory
successful_support → reliable_support memory
```

Memory 会影响后续节点反应。

## Step 9: update centralities

计算或近似更新：

```text
authority_centrality
information_centrality
resource_centrality
access_to_chief
issue_relevance
overall_core_score
```

第一版可不用复杂图算法，使用启发式：

```text
authority_centrality = 相关职位权力 + authority 出边总量
information_centrality = information_flow 入出边 + 持有重要 signal 数
resource_centrality = 管理 resource/task/object 的重要度
access_to_chief = 与 chief 的直接 authority/information 边 + 最近收到 chief signal
issue_relevance = 与当前高风险任务/资源/事件关联度
overall_core_score = 加权和
```

边缘节点中心性跃迁的核心测试：

```text
普通居民 R1 被任命为物资协调员
→ PositionObject 变化
→ R1 resource_centrality 上升
→ R1 access_to_chief 上升
→ 其他节点对 R1 的 information_flow 增强
→ R1 进入当前议题核心圈
```

## Step 10: update player knowledge

玩家不是全知节点。

玩家知道的信息来源：

```text
chief 当前持有的 signal
clue holder = chief
公开 report
直接观察到的 object 状态
会议中听到的发言
```

生成 PlayerKnowledge：

```python
@dataclass
class PlayerKnowledge:
    id: str
    topic: str
    confidence: float
    summary: str
    source_ids: list[str]
    status: str   # unknown / weak_suspicion / suspected / probable / confirmed / misled
    last_updated_tick: int
```

注意：  
这不是“玩家信任谁”的系统。  
它只是玩家当前有哪些信息。

## Step 11: generate visible report

ReportEngine 输出：

```text
当前时间
资源摘要
任务摘要
可见社会变化
已知线索
重要信号
核心圈变化提示
可疑但不确定的信息
```

不得输出 debug 真相，除非玩家输入 `debug_true`。

---

# 13. 传播算法简化版

第一版不要追求复杂图神经网络。  
先实现可解释规则。

## 13.1 边权归一化

所有边属性范围建议：

```text
0.0 ~ 100.0
```

计算时归一化到：

```text
0.0 ~ 1.0
```

## 13.2 Disturbance 传播

传播强度：

```text
transmitted =
base_intensity
× channel_match_weight
× edge_channel_strength
× (1 - depth_decay)
× random_noise
```

不同 disturbance_type 默认影响：

```text
coercion:
    direct target: stress +, fear +, trust_to_chief -, concealment_tendency +
    observers: fear + small, report_honesty - small

funding:
    target: morale +, cooperation +, trust_to_chief +
    non-target observers: fairness perception may change

appointment:
    target: authority/resource/access centrality +
    displaced nodes: competition/hostility may +

audit:
    target task/object: clue discovery chance +
    involved nodes: fear/stress + if guilty, report_honesty may change

public_support:
    target: morale +, reputation +
    observers: trust_to_chief + if perceived fair

broken_promise:
    affected nodes: trust_to_chief -, rumor +, memory negative
```

## 13.3 Signal 传播

传播概率：

```text
p =
signal.spread_rate
× edge.information_flow
× edge.bandwidth
× receiver_interest
× (1 - signal.secrecy_level)
```

变形概率：

```text
distort_p =
signal.distortion_rate
+ edge.distortion
+ receiver_anger_modifier
+ low_confidence_modifier
```

泄露概率：

```text
leak_p =
signal.secrecy_level
× holder.stress
× max(edge.empathy, edge.hostility_as_leak_to_enemy)
× leak_context_modifier
```

## 13.4 Trace → Clue

发现概率：

```text
p =
trace.strength
× channel_power
× source_reliability
× object_visibility
× (1 - information_distortion)
```

不同渠道：

```text
audit:
    high reliability, low misleading risk
informant:
    medium reliability, high misleading risk
patrol:
    medium reliability
meeting:
    low reliability for facts, useful for attitude changes
routine_report:
    affected heavily by report_honesty and information_distortion
```

---

# 14. CLI 命令要求

必须支持：

```text
help
status
tick
wait <n>
nodes
node <node_id>
edges <node_id>
objects
object <object_id>
tasks
signals
knowledge
report

assign_task <assignee_id> <task_type> <budget> <materials> <labor>
approve_task <task_id> <budget> <materials> <labor>
force_task <task_id>

appoint <node_id> <position_id>
appoint_deputy <node_id> <position_id>

promise <target_id> <topic> <deadline_ticks>
public_rebuke <node_id>
private_warning <node_id>

audit <object_id>
plant_informant <target_id>

debug_true
quit
```

`debug_true` 只用于开发，显示：

```text
真实 signals
隐藏 traces
真实社会边
后台事件
```

正常 report 不得显示这些。

---

# 15. 初始世界建议

## 15.1 社会节点

```text
CHIEF: 玩家区长
A1: 1栋楼长，务实
A2: 2栋楼长，压力敏感，较容易隐瞒
A3: 3栋楼长，保守
A4: 物业经理，资源/预算相关
A5: 保安队长，秩序相关
R1: 普通居民，可用于测试边缘节点跃迁
G1: 1栋居民群
G2: 2栋居民群
G3: 3栋居民群
```

## 15.2 初始职位对象

```text
leader_B1 -> A1
leader_B2 -> A2
leader_B3 -> A3
property_manager -> A4
security_chief -> A5
```

## 15.3 初始资源对象

```text
budget_pool: 10000
material_pool: 100
labor_pool: 20
```

## 15.4 初始社会边

```text
CHIEF -> A1/A2/A3/A4/A5:
    authority high

A1/A2/A3/A4/A5 -> CHIEF:
    trust medium
    fear low
    information_flow medium

A1 <-> A2:
    information_flow medium
    empathy low-medium

A2 <-> A3:
    information_flow medium
    empathy medium

A4 <-> A2:
    resource dependency medium
```

注意不要设置：

```text
CHIEF trust to A*
```

---

# 16. 测试剧本

## 16.1 剧本一：行动直接作用于人

命令：

```text
public_rebuke A2
tick
report
edges A2
signals
```

预期：

```text
A2 stress 上升
A2 对 CHIEF 的 trust 下降或 fear 上升
A1/A3 可能通过 information_flow 收到公开训斥信号
不需要先生成世界对象 trace
玩家报告可见公开训斥的后果
```

## 16.2 剧本二：强压任务但不给资源

命令：

```text
assign_task A2 build_storage 1000 20 5
force_task T1
wait 3
report
debug_true
```

预期：

```text
T1 blocked 或进展很慢
coercion disturbance 持续传播
A2 stress/fear 上升
A2 report_honesty 下降
A1/A3 形成弱信号或记忆
后台可能生成 private_complaint / false_report signal
玩家正常 report 不直接显示全部真相
```

## 16.3 剧本三：审批资源后正常推进

命令：

```text
assign_task A1 build_storage 1000 20 5
approve_task T1 1000 20 5
wait 3
tasks
report
```

预期：

```text
资源池减少或冻结
T1 progress_true 上升
A1 stress 控制在较低水平
funding disturbance 改善 A1 对 CHIEF 的评价
```

## 16.4 剧本四：承诺与失信

命令：

```text
promise G2 build_garbage_point 4
wait 5
report
signals
debug_true
```

预期：

```text
生成 promise signal
G2 或 A2 对 CHIEF 形成期待
超过 deadline 未兑现后，promise 变质为 broken_expectation
相关节点 trust_to_chief 下降
可能产生 rumor 或 complaint signal
```

## 16.5 剧本五：边缘节点进入核心圈

命令：

```text
appoint R1 position_supply_coordinator
tick
node R1
report
```

预期：

```text
R1 authority/resource/access centrality 上升
R1 从边缘节点进入物资议题核心圈
A4 可能产生竞争或不满扰动
其他节点向 R1 的 information_flow 增强
```

## 16.6 剧本六：隐藏信号泄露

命令：

```text
assign_task A2 build_storage 3000 40 6
approve_task T1 3000 40 6
force_task T1
wait 3
plant_informant A2
wait 2
knowledge
debug_true
```

预期：

```text
若 A2 产生 false_report / misuse / private_complaint 等隐藏信号
informant 增加该类信号泄露或 clue 发现概率
knowledge 中可能出现低/中置信度线索
不得直接无条件暴露真相
```

## 16.7 剧本七：玩家不操作，世界继续运行

命令：

```text
assign_task A2 build_storage 1000 20 5
wait 5
report
debug_true
```

预期：

```text
即使玩家只 wait，任务、信号、扰动、心理、后台事件仍继续推进
世界不是输入一句动一下
```

---

# 17. 验收标准

完成后必须满足：

```text
1. python main.py 可启动
2. 支持 tick/wait，玩家不操作世界也推进
3. 社会网络只包含人/组织节点
4. 世界对象不参与 trust/fear/loyalty 等社会心理
5. 行动可以直接作用于社会网络，不必经过 trace
6. 玩家命令转为 Signal + Disturbance + WorldObject change
7. 支持多个扰动并发传播和叠加
8. 支持 signal 传播、衰减、变形、阻断、泄露
9. 支持 trace → clue，且 clue 有置信度
10. 玩家 report 不显示真实后台，只显示认知投影
11. 不刻画 CHIEF 对他人的 trust/preference
12. 支持任务作为 WorldObject 执行
13. 支持职位作为 WorldObject，任命改变社会中心性
14. 支持边缘节点中心性跃迁测试
15. README 包含运行方式、命令表、测试剧本
```

---

# 18. 已知限制

当前 v2 文本原型暂不要求：

```text
1. 不接 LLM API
2. 不做自然语言开放解析
3. 不做 2D 地图
4. 不做复杂 UI
5. 不做完整 GNN 或真实网络科学算法
6. 不做大型居民个体模拟
7. 不做无限造物
```

当前目标是验证底层心脏：

```text
三层架构
持续时钟
社会影响传播
信号传播
隐藏与泄露
玩家认知投影
中心性跃迁
```

---

# 19. 推荐实现顺序

建议 CC 按此顺序实现：

```text
1. models.py 中定义核心 dataclass
2. initial_world_v2.json / 初始化函数
3. CLI 框架与基本命令
4. WorldClock tick/wait
5. SocialNetwork 基础边查询与更新
6. WorldObject / TaskObject 基础逻辑
7. DisturbanceEngine
8. SignalEngine
9. EvidenceEngine
10. CentralityEngine
11. ReportEngine
12. 测试剧本与 README
```

不要一开始就追求很聪明的事件生成。  
先让水波能传播，再让水波变复杂。

---

# 20. 一句话总结

> v2 原型的核心不是任务管理，而是一个持续运行的动态影响-信号网络。玩家每个命令都是向系统投下扰动；扰动可直接影响人，也可改变世界对象或产生信号；信号会传播、衰减、变形、阻断、泄露并沉积为记忆；玩家只能通过认知投影理解局部世界。任务、事件、证据和职位都只是这个三层系统中的对象与信号表现。
