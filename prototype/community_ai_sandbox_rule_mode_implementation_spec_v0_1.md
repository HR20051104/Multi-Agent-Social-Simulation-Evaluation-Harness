# 《AI 社区沙盘》Rule Mode 文本原型实现规格 v0.1

> 本文档用于指导 coding agent / Claude Code / Codex 实现第一版 **Rule Mode 文本原型**。  
> 当前阶段不接 LLM API，不做 2D 地图，不做复杂 UI，只实现后台逻辑与命令行交互。

---

## 1. 项目目标

项目名称暂定为：

```text
community_ai_sandbox_text_proto
```

这是一个 **AI 社会沙盘游戏的 Rule Mode 原型**。本阶段目标不是做完整游戏，而是验证核心后台链路是否成立：

```text
玩家命令
→ 解析为结构化 Action
→ 生成 Task / Policy / Investigation
→ 检查经费、资源、权限、执行者能力、心理压力
→ 推进每日结算
→ 自动生成后台事件
→ 后台事件不一定被玩家发现
→ 通过审计、眼线、举报、巡查等渠道生成 Clue
→ Clue 带来源、置信度、可靠性、误导风险
→ 玩家只能看到已发现信息，而不是全知 true_state
```

核心目标：实现一个可以运行、可以推进天数、可以暴露系统问题的命令行原型。

---

## 2. 核心设计原则

### 2.1 命令不是结果，执行才是结果

玩家说“让 2 栋楼长去建仓库”，不代表仓库立刻建成。

必须经过：

```text
任务创建
→ 执行者检查
→ 经费检查
→ 材料检查
→ 人力检查
→ 权限检查
→ 心理压力检查
→ 每日推进
→ 成功 / 拖延 / 失败 / 虚报 / 偷窃 / 崩溃 / 事故
```

### 2.2 规则引擎才是世界本体

当前版本不接 API。所有逻辑都用规则、概率、状态变量实现。

语言输出只是报告层。不要让报告直接决定世界结果。

### 2.3 不使用简单的 true/observed 二元模型

禁止把隐藏信息写成：

```json
{
  "content_true": "2栋楼长虚报材料价格。",
  "content_observed": "2栋项目材料价格偏高。"
}
```

这是错误设计。因为一旦 observed 里出现“材料价格偏高”，玩家就已经被系统提醒了。

正确模型是：

```text
TrueEvent 真实发生
→ Trace 客观迹象
→ DetectionChannel 发现渠道
→ Attention Check 注意力捕获
→ Clue 线索
→ Confidence 置信度
→ PlayerKnowledge 玩家认知
```

有些事件发生了，但玩家可能完全不知道。即使知道，也可能只是低置信度线索。

### 2.4 后台事件应自主推演

楼长偷钱、虚报进度、居民不满、私下串联，不应由玩家明确触发才出现。只要条件满足，就有概率生成。

例如：

```text
项目经费较大
审计强度低
楼长压力高
楼长忠诚低
玩家放权
施工缺资源
```

则可能生成：

```text
虚报进度
挪用资金
伪造材料账
向居民甩锅
私下抱怨
```

### 2.5 善治路线必须成立

不要把系统写成纯黑暗模拟器。玩家合理治理也应自然得到好结果：

```text
合理审批经费
透明审计
降低角色压力
修复设施
改善居民生活
提高信任
降低信息失真
减少后台恶性事件
```

---

## 3. 技术要求

### 3.1 语言与依赖

使用 Python 3.11+。

优先使用标准库：

```text
dataclasses
enum
json
random
typing
uuid
pathlib
```

不要引入复杂框架。

### 3.2 项目结构

建议结构：

```text
community_ai_sandbox_text_proto/
  main.py
  README.md
  data/
    initial_world.json
  src/
    models.py
    world.py
    command_parser.py
    rule_engine.py
    task_engine.py
    event_engine.py
    evidence_engine.py
    report_engine.py
    simulation.py
    utils.py
  tests/
    test_task_flow.py
    test_budget_flow.py
    test_hidden_event_flow.py
    test_evidence_flow.py
```

可以根据实现需要微调，但模块边界要清晰。

---

## 4. 核心数据模型

请用 `dataclass` 实现以下对象。

---

### 4.1 WorldState

表示世界真实状态。

字段至少包括：

```python
day: int
budget: int
materials: int
labor: int
legitimacy: float
public_order: float
information_distortion: float
true_satisfaction: float
reported_satisfaction: float
rebellion_pressure: float
agents: dict[str, Agent]
positions: dict[str, Position]
buildings: dict[str, Building]
tasks: dict[str, Task]
events: list[TrueEvent]
traces: list[Trace]
clues: list[Clue]
player_knowledge: list[PlayerKnowledge]
history_log: list[str]
```

说明：

- `true_satisfaction` 是真实满意度。
- `reported_satisfaction` 是通过报告呈现给玩家的满意度，可能受信息失真影响。
- `information_distortion` 越高，公开报告越不可信。
- `events` 是真实后台事件，不默认展示。
- `clues` 是玩家已经通过渠道发现的线索。

---

### 4.2 Agent

表示楼长、物业、保安等行动主体。

字段至少包括：

```python
id: str
name: str
role: str
position_id: str | None
loyalty: float
honesty: float
stress: float
competence: float
greed: float
fear: float
trust_in_player: float
health: float
alive: bool
available: bool
known_secrets: list[str]
```

字段含义：

| 字段 | 含义 |
|---|---|
| loyalty | 对玩家/区长的忠诚 |
| honesty | 诚实程度，影响虚报概率 |
| stress | 心理压力，影响拖延、虚报、崩溃 |
| competence | 执行能力，影响任务推进 |
| greed | 贪婪程度，影响挪用资源概率 |
| fear | 恐惧程度，影响表面服从和真实隐瞒 |
| trust_in_player | 对玩家的信任 |
| health | 健康状态 |

---

### 4.3 Position

职位系统必须支持楼长、副楼长、临时负责人、物业经理等。

字段至少包括：

```python
id: str
title: str
scope: str
holder_id: str | None
deputy_ids: list[str]
permissions: list[str]
authority_level: float
```

必须支持操作：

```text
任命楼长
任命副楼长
撤职
临时授权
多人共管
```

注意：职位不是纯文本标签，而应影响权限、执行任务、压力分担、报告渠道和信息失真。

---

### 4.4 Building

字段至少包括：

```python
id: str
name: str
category: str
condition: float
capacity: int
occupants: int
comfort: float
control_level: float
maintenance_cost: int
status: str
```

`status` 可选：

```text
normal
under_construction
damaged
abandoned
closed
```

---

### 4.5 Task

字段至少包括：

```python
id: str
title: str
type: str
assignee_id: str
status: str
progress: float
required_budget: int
approved_budget: int
reserved_budget: int
required_materials: int
reserved_materials: int
required_labor: int
reserved_labor: int
difficulty: float
risk: float
deadline: int | None
pressure_level: float
created_day: int
logs: list[str]
```

任务状态建议：

```text
pending
blocked
in_progress
delayed
completed
failed
falsely_reported
cancelled
```

说明：

- `required_*` 是任务实际需要。
- `approved_budget` 是玩家批准的经费额度。
- `reserved_*` 是已经从公共池冻结给任务的资源。
- 缺资源时任务不得凭空完成。

---

### 4.6 TrueEvent

真实事件。玩家不一定知道。

字段至少包括：

```python
id: str
day: int
type: str
severity: float
actor_ids: list[str]
target_ids: list[str]
content_true: str
visibility_base: float
trace_ids: list[str]
discovered: bool
```

注意：

- `content_true` 只存在后台。
- 普通报告系统不得直接展示 `content_true`。
- `discovered=True` 不代表玩家完全理解真相，只代表至少已有线索关联到它。

---

### 4.7 Trace

事件留下的客观迹象。

字段至少包括：

```python
id: str
event_id: str
day: int
type: str
location: str | None
strength: float
decay: float
detectable_by: list[str]
```

Trace 示例：

```text
材料库存异常
施工进度异常
居民传闻
账目数字不一致
夜间活动异常
楼长情绪异常
```

Trace 不等于 Clue。Trace 可以一直存在，但玩家未必发现。

---

### 4.8 Clue

玩家通过渠道发现的线索。

字段至少包括：

```python
id: str
day: int
source: str
related_event_id: str | None
related_trace_id: str | None
content: str
confidence: float
source_reliability: float
misleading_risk: float
status: str
```

`status` 可选：

```text
unverified
suspected
confirmed
false
```

Clue 文本必须避免直接写死真相，除非置信度极高。

低置信度例子：

```text
有居民匿名反映，2栋项目的材料使用情况似乎和施工进度对不上，但目前没有账目证据。
```

中置信度例子：

```text
审计发现 2栋项目的材料库存记录与实际盘点存在差异，需要进一步核查。
```

高置信度例子：

```text
审计确认 2栋项目存在 300 单位材料去向不明，相关签字人为 2栋楼长。
```

---

### 4.9 PlayerKnowledge

玩家认知，不等于真实世界。

字段至少包括：

```python
id: str
topic: str
confidence: float
summary: str
related_clue_ids: list[str]
last_updated_day: int
```

PlayerKnowledge 应由 Clue 聚合而来，而不是直接由 TrueEvent 生成。

---

## 5. 玩家命令系统

当前 Rule Mode 不需要自然语言智能解析。可以使用简单命令格式。

必须支持：

```text
help
status
next_day
agents
positions
tasks
events_debug
knowledge
appoint <agent_id> <position_id>
appoint_deputy <agent_id> <position_id>
remove_position <position_id>
assign_task <agent_id> <task_type> <required_budget> <required_materials> <required_labor>
approve_task <task_id> <budget> <materials> <labor>
deny_task <task_id>
force_task <task_id>
audit <target_id>
plant_informant <target_id>
meeting
quit
```

说明：

- `events_debug` 仅用于开发调试，正常玩家不应使用。
- `audit` 可针对任务、楼栋、角色或项目。
- `plant_informant` 可以提高特定目标相关 Trace 的发现概率，但应增加信任损耗或信息失真风险。

---

## 6. 任务执行系统

实现 `TaskEngine`。

---

### 6.1 创建任务

命令：

```text
assign_task A2 build_storage 1000 20 5
```

应生成 Task：

```text
assignee_id = A2
type = build_storage
required_budget = 1000
required_materials = 20
required_labor = 5
status = pending
progress = 0
```

创建任务本身不扣款、不消耗材料、不推进施工。

---

### 6.2 审批资源

命令：

```text
approve_task T1 1000 20 5
```

逻辑：

```text
检查 world.budget/materials/labor 是否足够
足够则从公共池冻结到任务池
更新 task.approved_budget / reserved_budget / reserved_materials / reserved_labor
若不足则审批失败，给出提示
```

建议采用“冻结”概念，即资源从公共池转入任务池。

---

### 6.3 每日推进任务

每日推进时，检查：

```text
reserved_budget >= required_budget
reserved_materials >= required_materials
reserved_labor >= required_labor
```

如果不足：

```text
status = blocked
assignee.stress += 若干
assignee.loyalty -= 若干
生成 task log
```

如果足够：

```text
status = in_progress
progress += daily_progress
```

建议公式：

```python
daily_progress = base + competence_factor + labor_factor - difficulty_factor - stress_penalty + random_noise
```

应保证不会出现资源不足但任务高速完成的情况。

---

### 6.4 强制推进

命令：

```text
force_task T1
```

效果：

```text
task.pressure_level 增加
assignee.stress 增加
assignee.loyalty 下降
assignee.fear 上升
```

如果资源不足还强制推进，则提高风险：

```text
虚报进度
偷窃材料
挪用资金
施工事故
任务失败
角色心理崩溃
```

---

### 6.5 任务完成

当 `progress >= 100`：

```text
status = completed
写入 history_log
更新建筑或世界状态
降低相关投诉或压力
释放未用资源，或记录消耗
```

---

## 7. 角色心理与异常行为系统

---

### 7.1 压力来源

每日结算时，根据以下因素更新 Agent stress：

```text
被强制推进任务
任务缺资源
任务逾期
居民不满
玩家责罚
预算不足但要求完成
职位责任过高
审计压力
```

---

### 7.2 压力后果

当 `stress > 70`：

```text
拖延概率上升
虚报概率上升
忠诚下降
健康下降
```

当 `stress > 85`：

```text
崩溃事件概率上升
辞职/逃避/严重心理危机风险上升
```

关于极端行为：

实现为抽象事件即可：

```text
severe_breakdown
self_harm_risk
disappearance
```

不要写血腥细节。只需要模拟严重心理崩溃和治理后果。

---

### 7.3 异常行为生成条件

#### 虚报进度

条件：

```text
任务压力高
资源不足
执行者 honesty 低或 stress 高
玩家要求强制完成
审计弱
```

#### 挪用资金/材料

条件：

```text
项目有资源池
greed 高
honesty 低
审计弱
压力高或忠诚低
```

#### 私下抱怨

条件：

```text
stress 高
loyalty 低
trust_in_player 低
```

---

## 8. 后台事件生成系统

实现 `EventEngine`。

每日自动检查世界状态、任务状态、角色状态，生成 TrueEvent。

第一版至少支持事件类型：

```text
private_complaint
false_progress_report
budget_misuse
material_misuse
task_delay
resident_dissatisfaction
rumor_spread
audit_anomaly
informant_tip
psychological_breakdown
```

事件生成要求：

```text
写入 world.events
生成 0~多个 Trace
不直接加入 player_knowledge
不自动展示给玩家
```

示例：楼长挪用材料。

```python
TrueEvent(
  type="material_misuse",
  actor_ids=["A2"],
  target_ids=["T1"],
  content_true="2栋楼长私下挪用了仓库项目的一部分材料。",
  visibility_base=0.2
)
```

同时生成 traces：

```text
材料库存异常
施工进度异常
低强度居民传闻
```

---

## 9. 证据、线索与置信度系统

实现 `EvidenceEngine`。

---

### 9.1 发现渠道

第一版支持：

```text
audit
informant
patrol
meeting
routine_report
accident_exposure
```

不同渠道能发现不同 Trace。

| 渠道 | 可发现内容 | 特点 |
|---|---|---|
| audit | 账目异常、材料异常 | 可靠性高，误导低 |
| informant | 私下抱怨、密谋、传闻 | 可靠性中低，误导中高 |
| patrol | 夜间活动、施工异常 | 可靠性中等 |
| meeting | 态度异常、发言矛盾 | 可靠性低，主观性高 |
| routine_report | 公开进度、公开满意度 | 容易受信息失真影响 |
| accident_exposure | 事故暴露的问题 | 可靠性较高，但被动发生 |

---

### 9.2 发现流程

```text
Trace 存在
→ 渠道覆盖
→ 根据 trace.strength、channel_power、information_distortion、source_reliability 计算发现概率
→ 成功则生成 Clue
→ 更新 PlayerKnowledge
```

推荐发现概率：

```python
p = trace.strength * channel_power * source_reliability
p *= (1 - world.information_distortion / 150)
p = clamp(p, 0.02, 0.95)
```

---

### 9.3 置信度

Clue 必须有：

```text
confidence
source_reliability
misleading_risk
```

渠道默认值建议：

```text
audit: reliability 0.85, misleading_risk 0.10
informant: reliability 0.55, misleading_risk 0.35
meeting: reliability 0.40, misleading_risk 0.40
patrol: reliability 0.65, misleading_risk 0.20
routine_report: reliability 0.50, misleading_risk depends on information_distortion
accident_exposure: reliability 0.80, misleading_risk 0.15
```

---

### 9.4 Clue 文本生成规则

不要直接暴露真相。根据 confidence 分级。

#### 低置信度 `< 0.4`

使用：

```text
有人反映……
似乎……
暂时无法确认……
可能存在……
```

#### 中置信度 `0.4~0.75`

使用：

```text
检查发现……
存在不一致……
需要进一步核查……
有较明显异常……
```

#### 高置信度 `> 0.75`

使用：

```text
已确认……
证据显示……
账目与实物核查一致指向……
```

---

## 10. 报告系统

实现 `ReportEngine`。

玩家可见内容包括：

```text
今日公开摘要
任务状态摘要
资源状态
角色会议发言
已发现线索
玩家认知更新
```

不要默认显示真实后台事件。

示例日报：

```text
Day 4 Report
预算：8500
材料：80
人力：12

任务：
- T1 临时仓库：blocked，原因：经费未完全审批。

公开情况：
- 2栋居民满意度略有下降。
- 物业称施工计划仍在等待资源协调。

已知线索：
- 暂无新线索。
```

如果有审计发现：

```text
已知线索：
- 审计发现 T1 项目的材料记录与实际进度存在不一致，置信度 0.68，建议继续核查。
```

---

## 11. 初始世界

`data/initial_world.json` 中设置以下内容。

### 11.1 角色

```text
A1: 1栋楼长，务实，honesty 70, loyalty 60, competence 65, greed 20
A2: 2栋楼长，压力敏感，honesty 45, loyalty 45, competence 55, greed 45
A3: 3栋楼长，保守，honesty 65, loyalty 50, competence 50, greed 25
A4: 物业经理，预算优先，honesty 50, loyalty 55, competence 70, greed 35
A5: 保安队长，秩序优先，honesty 60, loyalty 65, competence 60, greed 20
```

### 11.2 职位

```text
leader_B1 -> A1
leader_B2 -> A2
leader_B3 -> A3
property_manager -> A4
security_chief -> A5
```

### 11.3 世界资源

```text
budget: 10000
materials: 100
labor: 20
legitimacy: 70
public_order: 80
information_distortion: 10
true_satisfaction: 65
reported_satisfaction: 67
rebellion_pressure: 5
```

### 11.4 建筑

```text
B1 住宅楼
B2 住宅楼
B3 住宅楼
F1 绿地
F2 垃圾点
F3 停车场
F4 物业中心
```

---

## 12. CLI 交互要求

运行：

```bash
python main.py
```

显示：

```text
Community AI Sandbox Text Prototype v0.1
Type help for commands.
Day 1 >
```

支持命令：

```text
help
status
agents
positions
tasks
knowledge
next_day
appoint <agent_id> <position_id>
appoint_deputy <agent_id> <position_id>
remove_position <position_id>
assign_task <agent_id> <task_type> <required_budget> <required_materials> <required_labor>
approve_task <task_id> <budget> <materials> <labor>
deny_task <task_id>
force_task <task_id>
audit <target_id>
plant_informant <target_id>
meeting
events_debug
quit
```

`events_debug` 输出后台真实事件，仅用于开发调试。

---

## 13. 测试剧本

请在 README 中写入以下测试剧本，并保证可以跑通。

---

### 13.1 剧本 1：不给经费强制建造

```text
assign_task A2 build_storage 1000 20 5
force_task T1
next_day
next_day
next_day
status
agents
events_debug
knowledge
```

预期：

```text
任务卡住或进展很慢
A2 stress 上升
A2 loyalty 下降
后台可能出现 private_complaint 或 false_progress_report
玩家默认不一定知道后台事件
```

---

### 13.2 剧本 2：审批经费后正常推进

```text
assign_task A1 build_storage 1000 20 5
approve_task T1 1000 20 5
next_day
next_day
tasks
```

预期：

```text
预算/材料/人力冻结或扣除
任务进入 in_progress
进度正常增长
A1 stress 变化较小
```

---

### 13.3 剧本 3：隐藏挪用事件与审计发现

```text
assign_task A2 build_storage 3000 40 6
approve_task T1 3000 40 6
force_task T1
next_day
next_day
next_day
audit T1
knowledge
events_debug
```

预期：

```text
在条件满足时，可能生成 material_misuse 或 budget_misuse
玩家未审计前不一定知道
审计后可能获得 clue
clue 带 confidence，不一定直接确认真相
```

---

### 13.4 剧本 4：任命副楼长

```text
appoint_deputy A3 leader_B2
positions
meeting
```

预期：

```text
leader_B2 中 deputy_ids 包含 A3
会议中可以体现 B2 管理结构变化
后续任务可以考虑副楼长分担压力
```

---

## 14. 验收标准

完成后必须满足：

```text
1. 可以通过 python main.py 启动
2. 可以连续 next_day 运行 10 天不崩
3. 玩家可以创建任务、审批经费、强制任务
4. 缺资源时任务不会凭空完成
5. 审批资源会自动扣除或冻结
6. 执行者压力会随任务状况变化
7. 后台事件会基于条件自动生成
8. 后台事件不会自动暴露给玩家
9. 审计/眼线等渠道可以生成线索
10. 线索带置信度和来源
11. 玩家认知与真实事件分离
12. 支持任命楼长/副楼长/撤职
13. README 包含运行方法和测试剧本
14. 代码结构清晰，模块边界明确
```

---

## 15. 明确不做的内容

当前版本不要做：

```text
2D 图形地图
LLM API 接入
自然语言智能解析
复杂居民个体模拟
复杂季节系统
火箭/飞机等开放造物
完整起义系统
复杂 UI
联网功能
存档编辑器
```

本阶段只验证后台机制。

---

## 16. 完成后输出要求

完成实现后，请输出：

```text
1. 项目结构
2. 如何运行
3. 支持的命令
4. 已实现功能
5. 已知限制
6. 推荐下一步
```

不要只写伪代码。  
不要做 2D 图形。  
不要接 LLM API。  
不要把隐藏事件默认展示给玩家。  
不要让玩家命令直接变成结果。
