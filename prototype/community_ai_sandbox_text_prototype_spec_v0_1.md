# 《今日小区例会》文本原型 v0.1 规格说明

版本：v0.1  
定位：第一个可运行、可测试、可验收的后台模拟原型  
上游文档：
- 《AI 社会沙盘总纲 / Masterplan v0.4》
- 《核心系统设计文档 v0.2》

---

## 1. 原型目标

文本原型 v0.1 的目标不是做完整游戏，也不是做 2D 地图，而是验证本项目最核心的底层命题：

> 玩家命令不是结果。命令进入世界后，必须经过资源、权限、能力、心理、信息、环境和社会关系等现实条件检验，最终由系统自主推演出结果。

本阶段要证明以下链路可以运行：

```text
玩家输入命令
→ 系统解析为结构化 action
→ action 生成 task / policy / appointment / investigation 等对象
→ 系统检查资源、经费、权限、能力、关系和心理压力
→ 世界状态发生变化
→ 后台事件可能自主生成
→ 玩家不一定直接知道真实情况
→ 线索通过渠道、注意力、证据和置信度逐步浮出
→ 玩家据此继续决策
```

本阶段的判断标准不是“内容够多”，而是：

```text
1. 世界是否会自己运转
2. 事件是否由状态自然生成，而不是靠玩家点名
3. 玩家命令是否会受到现实约束
4. 信息系统是否不是简单 true/observed 二元
5. 玩家能否通过审计、眼线、会议等方式逐步接近真相
6. 系统是否能产生可解释的因果链
```

---

## 2. 原型边界

### 2.1 本阶段要做什么

文本原型 v0.1 应实现：

```text
1. 一个小规模社区世界状态
2. 玩家命令输入与结构化 action
3. 任务生成与执行系统
4. 经费审批与资源消耗系统
5. 职位、任命、权限与组织结构系统
6. 楼长、物业、保安等角色状态
7. 角色心理压力、忠诚、诚实、能力等变量
8. 后台事件自动生成
9. 线索、证据、置信度与玩家认知系统
10. 每日结算流程
11. 日报 / 会议 / 审计 / 眼线等信息渠道
12. 至少 3 个可运行测试剧本
```

### 2.2 本阶段不做什么

文本原型 v0.1 不做：

```text
1. 2D 地图
2. 像素美术
3. 居民个体级移动
4. A* 寻路
5. 复杂建筑自由拼装
6. 火箭、飞机等大型开放造物的完整实现
7. 大规模居民群体建模
8. 长期季节循环的完整版本
9. 完整起义战争系统
10. 商业化 UI
11. 多周目平衡
```

但是，本阶段的数据结构必须为后续 2D 地图和开放造物预留字段。

例如，即使文本原型不显示地图，也应允许 facility 拥有：

```json
{
  "location_hint": "near_B2",
  "footprint": [3, 2],
  "visual_tags": ["temporary", "storage", "dirty"]
}
```

---

## 3. 第一版世界规模

### 3.1 初始小区

文本原型 v0.1 使用一个极小但完整的小区：

```text
社区名称：临时自治小区 A
背景：crisis 下获得临时自治权
模拟周期：10 天
初始预算：10000
初始公共材料：100 单位
初始可用人力：20 单位
住宅楼：3 栋
核心角色：6 名
居民：按楼栋聚合，共 60 人
```

### 3.2 初始建筑 / 设施

```text
B1 住宅楼：20 人
B2 住宅楼：22 人
B3 住宅楼：18 人
物业中心：1 个
小区门口：1 个
公共仓库：无
垃圾点：1 个
临时空地：1 块
```

### 3.3 初始角色

```text
区长：玩家
B1 楼长：务实，能力较高，忠诚中等
B2 楼长：情绪敏感，居民影响力高，压力承受低
B3 楼长：保守，诚实较高，行动力一般
物业经理：预算优先，执行能力高，诚实中等
保安队长：秩序优先，忠诚较高，视野偏治安
临时财务员：账目管理，风险规避，容易被施压
```

### 3.4 初始社区状态

```json
{
  "day": 1,
  "budget": 10000,
  "materials": 100,
  "labor": 20,
  "legitimacy": 65,
  "public_order": 75,
  "trust_in_governance": 60,
  "information_distortion": 15,
  "general_anger": 15,
  "general_fear": 10,
  "rebellion_pressure": 0,
  "audit_strength": 20,
  "surveillance_strength": 5,
  "informant_network": 0
}
```

---

## 4. 核心数据对象

本阶段应优先保持数据对象清晰。代码可以简单，但数据结构不能糊。

---

### 4.1 WorldState

`WorldState` 是整个模拟的真实世界状态。

```json
{
  "day": 1,
  "community": {
    "budget": 10000,
    "materials": 100,
    "labor": 20,
    "legitimacy": 65,
    "public_order": 75,
    "trust_in_governance": 60,
    "information_distortion": 15,
    "general_anger": 15,
    "general_fear": 10,
    "rebellion_pressure": 0
  },
  "buildings": {},
  "facilities": {},
  "agents": {},
  "positions": {},
  "tasks": {},
  "policies": {},
  "events": {},
  "traces": {},
  "clues": {},
  "player_knowledge": {},
  "history": []
}
```

原则：

```text
WorldState 记录真实状态。
玩家不应直接看到完整 WorldState。
玩家只能通过报告、会议、审计、眼线、观察等渠道获得 PlayerKnowledge。
```

---

### 4.2 Building

楼栋是居民聚合状态的主要载体。

```json
{
  "id": "B2",
  "name": "2栋",
  "population": 22,
  "leader_id": "agent_B2_leader",
  "deputy_leader_id": null,
  "resident_state": {
    "satisfaction": 58,
    "anger": 22,
    "fear": 8,
    "trust": 55,
    "health": 72,
    "organization": 10,
    "complaint_tendency": 35
  },
  "needs": {
    "storage": 50,
    "cleanliness": 60,
    "security": 50,
    "housing_quality": 70
  },
  "known_by_player": {
    "satisfaction_estimate": 60,
    "anger_estimate": 18,
    "confidence": 45
  }
}
```

---

### 4.3 Agent

Agent 包括楼长、物业经理、保安队长、财务员等。居民个体暂不细分。

```json
{
  "id": "agent_B2_leader",
  "name": "2栋楼长",
  "role": "building_leader",
  "assigned_building": "B2",
  "personality": {
    "pragmatism": 40,
    "emotionality": 75,
    "risk_tolerance": 35,
    "greed": 25,
    "moral_constraint": 55,
    "ambition": 30
  },
  "capability": {
    "construction": 25,
    "organization": 70,
    "finance": 30,
    "negotiation": 55,
    "security": 20
  },
  "state": {
    "loyalty_to_player": 45,
    "honesty": 60,
    "stress": 35,
    "fear": 15,
    "resentment": 20,
    "relationship_with_residents": 75
  },
  "permissions": ["report_building_status", "organize_residents"],
  "resources_controlled": [],
  "current_tasks": [],
  "private_memory": []
}
```

#### 4.3.1 角色变量解释

```text
loyalty_to_player：对区长的忠诚，不等于诚实。
honesty：报告真实情况的倾向。
stress：压力。过高会引发失误、拖延、崩溃、隐瞒、异常行为。
fear：恐惧。恐惧高会提高短期服从，但也提高信息失真。
resentment：怨气。高怨气会提高消极抵抗和背后串联概率。
greed：贪婪。不是单独触发贪污，必须结合机会和监督弱。
moral_constraint：道德约束。影响是否愿意执行伤害性命令或违法操作。
capability：能力。影响任务完成质量和失败风险。
```

---

### 4.4 Position

职位系统必须支持后续任命新楼长、副楼长、亲信、临时委员会等。

```json
{
  "id": "position_B2_deputy_leader",
  "title": "2栋副楼长",
  "holder_agent_id": null,
  "scope": "B2",
  "authority": [
    "assist_leader",
    "collect_resident_feedback",
    "supervise_small_tasks"
  ],
  "resource_access": [],
  "reporting_to": "agent_B2_leader",
  "appointed_by": "player",
  "legitimacy_source": "appointment",
  "is_active": false
}
```

职位任命不是单纯改称号，而会影响：

```text
1. 权限
2. 汇报渠道
3. 派系关系
4. 信息可见度
5. 居民信任
6. 楼长权力平衡
7. 任务执行能力
```

---

### 4.5 Task

Task 是玩家命令进入现实世界后的主要载体。

```json
{
  "id": "task_001",
  "type": "construct_facility",
  "title": "修建临时仓库",
  "created_day": 1,
  "assigned_to": "agent_B2_leader",
  "requested_by": "player",
  "target": {
    "facility_type": "temporary_storage",
    "location_hint": "near_B2"
  },
  "requirements": {
    "budget_required": 1800,
    "materials_required": 25,
    "labor_required": 5,
    "permission_required": ["construction_approval"],
    "capability_required": {
      "construction": 40,
      "organization": 30
    }
  },
  "approved_resources": {
    "budget": 0,
    "materials": 0,
    "labor": 0
  },
  "status": "blocked",
  "blockers": ["budget_not_approved", "materials_not_allocated"],
  "progress": 0,
  "quality": null,
  "pressure_level": 20,
  "risk_flags": ["assignee_under_resourced"],
  "history": []
}
```

Task 状态枚举：

```text
proposed       已提出
approved       已批准
blocked        被现实条件卡住
in_progress    执行中
delayed        延误
completed      完成
failed         失败
abandoned      被放弃
faked          被虚报完成或虚报进度
corrupted      出现挪用、偷工减料、虚假采购等问题
```

---

### 4.6 Facility

文本原型不需要地图显示，但 facility 要为后续 2D 预留。

```json
{
  "id": "facility_storage_001",
  "name": "临时仓库",
  "category": "utility",
  "status": "under_construction",
  "condition": 100,
  "capacity": 80,
  "quality": null,
  "maintenance_cost": 20,
  "created_by_task": "task_001",
  "location_hint": "near_B2",
  "footprint": [3, 2],
  "visual_tags": ["temporary", "storage", "metal_roof"]
}
```

---

### 4.7 Event

Event 是真实发生的后台事件。它不等于玩家知道的事情。

```json
{
  "id": "event_017",
  "day": 4,
  "type": "minor_fund_misuse",
  "actors": ["agent_B2_leader"],
  "related_task": "task_001",
  "severity": 35,
  "truth_content": "2栋楼长私下截留部分材料预算，用于补偿此前垫付的人情开销。",
  "causes": [
    "underfunded_task",
    "high_stress",
    "low_audit_strength",
    "resource_pressure"
  ],
  "traces_generated": ["trace_021", "trace_022"],
  "is_known_to_player": false
}
```

关键原则：

```text
Event 是真实发生。
Event 不自动变成玩家可见信息。
Event 只能通过 Trace → Channel → Clue → Knowledge 链条进入玩家认知。
```

---

### 4.8 Trace

Trace 是事件留下的客观痕迹。痕迹也不一定被发现。

```json
{
  "id": "trace_021",
  "event_id": "event_017",
  "type": "accounting_irregularity",
  "location": "finance_records",
  "strength": 30,
  "persistence_days": 7,
  "discoverable_by": ["audit", "financial_review"],
  "misleading_possibility": 25
}
```

常见 Trace 类型：

```text
accounting_irregularity    账目痕迹
material_shortage          材料短缺痕迹
schedule_delay             工期延误痕迹
rumor_fragment             传闻碎片
witness_statement          目击证词
behavior_change            行为变化
quality_defect             工程质量问题
private_meeting_pattern    私下会面模式
```

---

### 4.9 Clue

Clue 是玩家通过某个渠道得到的信息。它可能是真的、半真、误导性、低置信度。

```json
{
  "id": "clue_008",
  "day_discovered": 5,
  "source_channel": "audit",
  "source_reliability": 70,
  "related_trace": "trace_021",
  "content": "审计发现仓库项目的材料记录存在一处小额不一致。",
  "confidence": 45,
  "possible_explanations": [
    "普通记账错误",
    "材料临时调拨未登记",
    "小额挪用或虚报"
  ],
  "is_confirmed": false
}
```

重要原则：

```text
线索不是结论。
线索必须带来源、置信度、可替代解释。
低置信度线索不能写成确定事实。
玩家需要进一步调查才能升级认知。
```

---

### 4.10 PlayerKnowledge

玩家认知不是事实，而是玩家当前相信或怀疑的状态。

```json
{
  "topic_id": "B2_storage_project_finance",
  "status": "suspected",
  "confidence": 45,
  "known_clues": ["clue_008"],
  "hypotheses": [
    {
      "claim": "仓库项目可能存在材料账异常",
      "confidence": 45
    },
    {
      "claim": "异常可能只是普通登记错误",
      "confidence": 35
    }
  ],
  "last_updated_day": 5
}
```

认知状态枚举：

```text
unknown       完全不知道
noticed       注意到异常，但无法判断
suspected     怀疑某类问题
probable      大概率认为存在问题
confirmed     已确认
misled        被误导
```

---

## 5. 玩家命令类型

文本原型 v0.1 支持以下命令。

---

### 5.1 任命 / 撤职类

示例：

```text
任命张三为2栋副楼长。
撤掉2栋楼长。
让物业经理兼任临时物资主管。
成立一个由1栋楼长和保安队长组成的应急小组。
```

输出 action 示例：

```json
{
  "action_type": "appoint_position",
  "target_agent": "agent_ZhangSan",
  "position": "B2_deputy_leader",
  "scope": "B2"
}
```

系统检查：

```text
1. 玩家是否有任命权
2. 被任命者是否存在
3. 职位是否存在，不存在则是否可创建
4. 被任命者是否愿意接受
5. 原职位持有者是否受影响
6. 居民是否承认该任命
7. 组织关系是否改变
```

---

### 5.2 分配任务类

示例：

```text
让2栋楼长去修一个临时仓库。
让保安队长组织夜间巡逻。
让物业经理负责清点物资。
```

输出 action 示例：

```json
{
  "action_type": "assign_task",
  "assignee": "agent_B2_leader",
  "task_type": "construct_facility",
  "task_detail": {
    "facility_name": "临时仓库",
    "location_hint": "near_B2"
  }
}
```

系统检查：

```text
1. 任务需要什么资源
2. 是否审批经费
3. 是否分配材料
4. 是否有人力
5. 执行者能力是否足够
6. 执行者压力是否过高
7. 执行者是否有权限调动相关资源
8. 如果缺资源，任务应 blocked，而不是直接完成
```

---

### 5.3 经费 / 资源审批类

示例：

```text
批准仓库项目1800经费。
给2栋楼长20单位材料。
不给钱，但要求三天内必须完工。
冻结物业经理的采购权限。
```

输出 action 示例：

```json
{
  "action_type": "approve_resources",
  "target_task": "task_001",
  "resources": {
    "budget": 1800,
    "materials": 25,
    "labor": 5
  }
}
```

自动关联：

```text
批准经费 → 预算冻结或扣款
分配材料 → 公共材料池减少
分配人力 → 可用人力减少
撤回经费 → 任务停滞或违约
强制要求完成但不给资源 → 压力和异常行为风险上升
```

---

### 5.4 调查 / 审计 / 眼线类

示例：

```text
审计2栋仓库项目账目。
安排眼线关注2栋楼长。
让保安队长调查夜间异常活动。
开启匿名举报箱。
```

输出 action 示例：

```json
{
  "action_type": "investigate",
  "method": "audit",
  "target": "task_001",
  "intensity": 50
}
```

系统检查：

```text
1. 调查方式能发现哪些 trace
2. 调查强度是否足够
3. 调查是否消耗预算/人力
4. 被调查者是否察觉
5. 调查本身是否提高恐惧或不信任
6. 是否产生线索 clue
7. 线索置信度是多少
```

---

### 5.5 会议 / 询问类

示例：

```text
召开楼长会议。
询问2栋楼长仓库进度。
让物业经理汇报预算。
要求所有楼长说明居民情绪。
```

会议不是直接读取真相，而是生成角色视角的报告。

报告受以下变量影响：

```text
1. 角色知道什么
2. 角色愿不愿说
3. 角色敢不敢说
4. 角色是否有私心
5. 角色是否被恐惧压制
6. 玩家是否有证据追问
7. 会议气氛和权力关系
```

---

### 5.6 推进时间类

示例：

```text
进入下一天。
推进三天。
```

每推进一天，应执行：

```text
1. 任务执行结算
2. 资源消耗结算
3. 角色心理变化
4. 居民状态变化
5. 后台事件生成
6. trace 生成和衰减
7. clue 发现判定
8. 玩家日报生成
9. 历史日志写入
```

---

## 6. 任务执行流程

任务执行必须是本原型的核心。

### 6.1 标准流程

```text
Step 1：玩家提出命令
Step 2：生成 action
Step 3：action 生成 task
Step 4：系统计算 requirements
Step 5：检查 approved_resources
Step 6：检查 assignee capability / permission / stress
Step 7：判断任务状态
Step 8：每日推进 progress 或生成 blocker
Step 9：完成、失败、拖延、虚报或腐化
Step 10：生成事件、trace、报告或线索
```

### 6.2 任务可行性检查

任务是否可推进由以下因素决定：

```text
资源：预算、材料、人力、时间
权限：执行者是否有权调动资源
能力：执行者能力是否满足任务门槛
心理：压力、恐惧、怨气是否过高
关系：居民是否配合，其他角色是否阻挠
环境：天气、crisis 阶段，本阶段可简化
监督：审计强度、透明度
```

### 6.3 缺资源时的行为

如果任务缺资源，不应该自动失败，而是进入压力演化：

```text
Day 1：任务 blocked
Day 2：执行者压力上升
Day 3：执行者可能申请资源、拖延、虚报进度
Day 4+：若继续强压，可能出现异常行为
```

异常行为包括：

```text
拖延
推责
虚报进度
向其他角色私下求助
挪用其他项目资源
偷工减料
小额偷窃
伪造报告
辞职/罢工/崩溃
```

这些异常行为不是随机惩罚，而是由条件触发。

---

## 7. 经费与资源系统

### 7.1 资源类型

文本原型 v0.1 至少有：

```text
budget      经费
materials   材料
labor       人力
attention   管理注意力，可选
trust       信任，不是硬资源但影响执行
```

### 7.2 经费状态

经费不只有“扣款”，还应有状态：

```text
available     可用
frozen        已冻结给某任务
spent         已实际支出
misused       被挪用
recovered     被追回
unaccounted   去向不明
```

示例：

```json
{
  "budget_pool": {
    "available": 8200,
    "frozen": 1800,
    "spent": 0,
    "misused": 0,
    "unaccounted": 0
  }
}
```

### 7.3 审批规则

```text
玩家批准预算后，预算应先 frozen。
任务推进时，frozen 逐步转为 spent。
如果存在贪污/虚报，则部分 frozen 可能转为 misused 或 unaccounted。
如果任务取消，未使用 frozen 应释放。
```

### 7.4 自动关联原则

玩家说：

```text
批准仓库项目1800经费。
```

系统应自动：

```text
1. 找到仓库任务
2. 检查预算是否足够
3. 将 1800 从 available 移到 frozen
4. 更新 task.approved_resources.budget
5. 降低任务 blocker
6. 记录历史
```

玩家说：

```text
不给经费，但要求必须三天内完工。
```

系统应自动：

```text
1. 任务保持 blocked 或低速推进
2. assignee 压力上升
3. 恐惧或怨气上升
4. 异常行为风险上升
5. 可能产生 hidden_event
```

---

## 8. 角色心理与异常行为系统

### 8.1 压力来源

角色压力来源包括：

```text
任务缺资源
任务期限过短
任务超过能力
被公开批评
被要求执行违背道德的命令
居民压力
上级压力
审计压力
长期无休息
失败历史
```

### 8.2 压力后果

压力不是直接“自杀/崩溃”。必须分阶段。

```text
0-30：正常
31-50：抱怨、效率下降
51-70：拖延、隐瞒、推责、关系恶化
71-85：虚报、违规操作、消极抵抗、情绪爆发
86-95：严重崩溃、辞职、失踪、极端行为风险
96-100：重大心理危机或不可逆事件风险
```

涉及自伤等极端结果时，系统不应轻率生成。需要同时满足：

```text
1. 压力极高
2. 支持网络极弱
3. 恐惧或绝望极高
4. 长期被强迫且无出口
5. 近期有强导火索
6. 没有干预或缓冲机制
```

并且应优先生成较温和但仍严重的替代结果：

```text
请假
辞职
崩溃哭诉
公开反抗
逃避任务
找人顶包
向居民倾诉
向其他楼长求助
```

### 8.3 异常行为生成条件

#### 8.3.1 虚报进度

触发条件：

```text
任务被强压
任务进度低
执行者害怕惩罚
审计弱
诚实较低或压力较高
```

#### 8.3.2 挪用资源

触发条件：

```text
任务缺资源
执行者有资源接触机会
审计弱
压力或贪婪较高
道德约束不足
```

#### 8.3.3 偷工减料

触发条件：

```text
任务期限紧
材料不足
质量检查弱
执行者想完成表面进度
```

#### 8.3.4 公开反抗

触发条件：

```text
怨气高
恐惧不足以压制
居民支持执行者
玩家合法性低
近期不公事件
```

---

## 9. 后台事件生成系统

后台事件不是玩家点名产生，而是系统每天扫描状态生成。

### 9.1 后台事件生成流程

```text
每日结算开始
→ 扫描任务状态
→ 扫描角色心理
→ 扫描资源异常
→ 扫描居民状态
→ 扫描组织关系
→ 生成候选事件
→ 计算事件概率
→ 根据阈值与随机扰动决定是否发生
→ 生成 true_event
→ 生成 trace
→ 写入 hidden_log
```

### 9.2 候选事件结构

```json
{
  "candidate_type": "false_progress_report",
  "preconditions": [
    "task_progress_low",
    "deadline_pressure_high",
    "assignee_fear_high",
    "audit_strength_low"
  ],
  "base_probability": 25,
  "modifiers": {
    "honesty_low": 15,
    "stress_high": 20,
    "loyalty_high": -5
  }
}
```

### 9.3 第一版后台事件类型

v0.1 至少支持：

```text
task_delay                  任务拖延
private_complaint            私下抱怨
false_progress_report        虚报进度
minor_fund_misuse            小额挪用
material_misallocation       材料私下调拨
quality_cutting              偷工减料
resident_discontent_growth   居民不满积累
rumor_spread                 谣言传播
informal_alliance            私下结盟
whistleblowing_attempt       举报尝试
```

### 9.4 事件不得无因生成

每个事件必须记录 causes。

错误示例：

```json
{
  "type": "fund_misuse",
  "causes": []
}
```

正确示例：

```json
{
  "type": "fund_misuse",
  "causes": [
    "approved_budget_exists",
    "audit_strength_low",
    "assignee_stress_high",
    "material_pressure_high"
  ]
}
```

---

## 10. 线索、证据与置信度系统

这是 v0.1 必须修正和验证的核心。

### 10.1 不能使用简单 observed 文本

禁止把真实事件直接改写成“玩家可见版”。

错误设计：

```json
{
  "content_true": "2栋楼长虚报材料价格。",
  "content_observed": "2栋项目材料价格偏高。"
}
```

问题：

```text
只要玩家看到“材料价格偏高”，就已经被系统强提醒。
真实情况下玩家可能完全注意不到。
```

正确设计：

```text
真实事件存在
→ 留下若干 trace
→ trace 可能被某个渠道发现
→ 发现后生成 clue
→ clue 带置信度、来源和替代解释
→ 玩家认知逐步更新
```

### 10.2 线索生成条件

线索出现必须经过渠道，例如：

```text
audit             审计
informant         眼线
complaint         居民投诉
meeting           会议发言
inspection        现场检查
accident          事故暴露
rumor             传闻
data_check        数据异常检测
```

没有渠道时：

```text
事件可以发生，但玩家完全不知道。
```

### 10.3 线索写法规范

低置信度线索不能写成确定事实。

#### 低置信度

```text
审计记录里有一处小额材料登记不一致，但目前无法判断是记账错误还是实际异常。
```

#### 中置信度

```text
仓库项目的材料消耗和施工进度不太匹配，可能存在调拨未登记、浪费或虚报。
```

#### 高置信度

```text
审计和仓库盘点相互印证，确认有 12 单位材料未进入施工现场。
```

#### 已确认

```text
经财务记录、仓库盘点和目击证词交叉确认，2栋楼长参与了材料挪用。
```

### 10.4 可误导性

线索可以误导玩家。

例如：

```text
账目异常可能是贪污，也可能是混乱时期的登记延迟。
施工队和楼长频繁接触可能是合谋，也可能是正常协调。
材料明显不够可能是挪用，也可能是需求估算错误。
```

系统必须保留替代解释，直到证据足够。

---

## 11. 玩家报告系统

### 11.1 日报

每天给玩家的日报不应展示全部事实，而应展示：

```text
1. 公开发生的事情
2. 玩家已有渠道能知道的事情
3. 明显的任务状态
4. 已发现线索
5. 需要玩家注意但未必指向真相的异常
```

日报示例：

```text
第 4 天日报：
- 临时仓库项目仍未开工，主要原因是经费和材料尚未审批。
- 2栋楼长提交了延期申请，称目前“缺少必要条件”。
- 2栋居民满意度估计略有下降，但置信度较低。
- 未发现重大治安问题。
```

如果没有审计/眼线，不应写：

```text
2栋楼长可能虚报材料。
```

### 11.2 会议报告

会议发言是角色主动表达，不等于真相。

会议发言应受：

```text
honesty
fear
loyalty
stress
self_interest
known_facts
player_evidence
```

影响。

### 11.3 审计报告

审计报告更接近证据，但也有成本和局限。

审计可能输出：

```text
未发现异常
发现低置信度异常
发现中置信度异常
确认异常
审计受阻
审计数据不足
```

---

## 12. 每日结算流程

每日推进应按固定顺序执行，避免因果混乱。

```text
1. 接收玩家当日命令
2. 将命令解析为 action
3. 生成 / 修改 task、policy、position、investigation
4. 立即处理资源审批与权限变更
5. 执行任务推进
6. 结算资源消耗
7. 更新角色心理
8. 更新居民楼栋状态
9. 扫描并生成后台事件
10. 为后台事件生成 trace
11. 根据渠道尝试发现 trace
12. 生成 clue
13. 更新 player_knowledge
14. 生成玩家日报
15. 写入历史日志
16. day + 1
```

---

## 13. AI 接口预留

文本原型 v0.1 应支持两种模式。

### 13.1 Rule Mode

不用 API。

特点：

```text
1. 玩家命令用固定菜单或简化指令
2. 报告用模板生成
3. 适合调试规则引擎
4. 成本低，稳定
```

### 13.2 LLM Mode

接 API。

AI 负责：

```text
1. 玩家自然语言 → action_json
2. 角色发言生成
3. 日报润色
4. 线索文本生成
```

AI 不负责：

```text
1. 直接修改世界状态
2. 直接决定任务是否成功
3. 直接决定谁贪污
4. 直接决定起义是否发生
5. 直接跳过证据系统告诉玩家真相
```

### 13.3 LLMService 接口

建议抽象为：

```python
class LLMService:
    def parse_player_command(text, context) -> ActionJSON:
        pass

    def generate_daily_report(observed_context, player_knowledge) -> str:
        pass

    def generate_agent_statement(agent_context, meeting_context) -> str:
        pass

    def generate_clue_text(clue_data) -> str:
        pass
```

所有 LLM 输出必须经过 schema 校验。

---

## 14. 文本原型推荐文件结构

建议项目结构：

```text
community_ai_sandbox_text_proto/
  main.py
  data/
    initial_world.json
    schemas/
      action.schema.json
      task.schema.json
      event.schema.json
      clue.schema.json
  engine/
    world_state.py
    command_parser.py
    action_handler.py
    task_engine.py
    resource_engine.py
    agent_engine.py
    event_engine.py
    trace_engine.py
    knowledge_engine.py
    report_engine.py
    daily_tick.py
  llm/
    llm_service.py
    mock_llm.py
    openai_llm.py
  tests/
    scenario_underfunded_task.py
    scenario_audit_discovery.py
    scenario_appointment_conflict.py
  logs/
    visible_log.txt
    hidden_log.txt
    debug_state.json
```

---

## 15. 测试剧本

文本原型 v0.1 至少要跑通以下剧本。

---

### 15.1 剧本 A：不给钱却强制修仓库

#### 初始命令

```text
让2栋楼长修一个临时仓库，但暂时不批经费。三天内必须完成。
```

#### 预期系统行为

```text
Day 1：生成任务，任务 blocked，原因是经费和材料未审批。
Day 2：2栋楼长压力上升，可能提交延期或求助。
Day 3：若玩家继续强压，虚报、抱怨、私下求助风险上升。
Day 4+：可能生成后台事件，如虚报进度或私下挪用材料。
```

#### 验收点

```text
1. 任务不能凭空完成
2. 缺资源会形成 blocker
3. 角色压力上升
4. 后台事件可能自主出现
5. 玩家不一定知道真实异常
6. 通过审计或眼线可以获得线索
```

---

### 15.2 剧本 B：正常审批并顺利完成

#### 初始命令

```text
让物业经理修一个临时仓库，批准1800经费、25材料、5人力。
```

#### 预期系统行为

```text
Day 1：任务 approved，预算冻结。
Day 2-4：任务推进，资源逐步消耗。
Day 5：仓库完成，生成 facility。
居民仓储需求缓解。
```

#### 验收点

```text
1. 经费自动冻结/支出
2. 材料自动扣减
3. 任务进度推进
4. 设施进入世界状态
5. 正向治理也能成立
```

---

### 15.3 剧本 C：任命副楼长导致权力变化

#### 初始命令

```text
任命一名亲信为2栋副楼长，让他协助监督2栋事务。
```

#### 预期系统行为

```text
1. 创建或激活副楼长职位
2. 更新组织结构
3. 2栋楼长可能感到被削权
4. 信息可见度可能提高
5. 2栋内部信任可能下降
6. 副楼长可能成为眼线或新的派系节点
```

#### 验收点

```text
1. 职位不是称号，而是权限和关系变化
2. 任命会影响信息渠道
3. 原楼长会产生心理/关系反应
4. 后续事件可引用这次任命
```

---

### 15.4 剧本 D：审计发现线索但不能直接定罪

#### 前置条件

后台已发生小额挪用事件，并生成账目 trace。

#### 玩家命令

```text
审计2栋仓库项目账目。
```

#### 预期系统行为

```text
1. 审计消耗一定人力或预算
2. 审计扫描相关 trace
3. 根据 audit_strength 和 trace_strength 生成 clue
4. clue 带置信度和替代解释
5. player_knowledge 从 unknown 变成 noticed 或 suspected
```

#### 验收点

```text
1. 不直接告诉玩家“谁贪污了”
2. 线索有置信度
3. 线索有替代解释
4. 后续调查可以提高置信度
```

---

### 15.5 剧本 E：高压治理导致报告失真

#### 初始命令

```text
连续三天公开批评所有楼长，要求所有问题必须当天解决，否则撤职。
```

#### 预期系统行为

```text
1. 楼长恐惧上升
2. 短期服从上升
3. 真实问题未必减少
4. 报告失真增加
5. 私下抱怨和串联风险上升
6. 玩家日报看起来可能更稳定
```

#### 验收点

```text
1. 高压不是立刻失败，也不是纯惩罚
2. 恐惧能带来短期服从
3. 信息质量下降
4. 后台风险累积
5. 玩家可见世界和真实世界开始分离
```

---

## 16. 验收标准

文本原型 v0.1 通过标准：

### 16.1 功能验收

```text
1. 可以初始化世界
2. 可以输入或选择玩家命令
3. 命令能生成 action
4. action 能生成 task / appointment / investigation 等对象
5. 任务会检查资源和权限
6. 经费审批会自动扣款或冻结
7. 缺资源任务不会凭空完成
8. 角色心理会随事件变化
9. 后台事件能自主生成
10. 事件能生成 trace
11. trace 不一定被发现
12. 发现后生成 clue
13. clue 带置信度和来源
14. 玩家日报不会全知
15. 至少 3 个测试剧本跑通
```

### 16.2 设计验收

```text
1. 玩家能感到“世界在自己运转”
2. 玩家命令有现实阻力
3. 玩家不总是知道真相
4. 信息不是简单 true/observed
5. 善治路线能产生正反馈
6. 高压路线能产生短期收益和长期风险
7. 后台事件有因果，不是随机吓人
8. 事件能被事后解释
```

### 16.3 工程验收

```text
1. 数据结构清晰
2. 模块边界清晰
3. LLM 可插拔
4. Rule Mode 可独立运行
5. 所有重要状态可导出 debug_state.json
6. visible_log 与 hidden_log 分离
7. 每日结算顺序固定
```

---

## 17. 进入下一阶段的条件

只有当文本原型 v0.1 满足以下条件，才进入 2D 地图原型：

```text
1. 连续模拟 10 天不崩
2. 至少 5 类玩家命令可用
3. 至少 5 类后台事件可生成
4. 至少 3 条线索链路可跑通
5. 至少一个剧本出现“玩家最初不知道，后来通过调查发现”的过程
6. 至少一个剧本出现“善治顺利完成任务”的过程
7. 至少一个剧本出现“命令因现实条件被卡住”的过程
8. 日报不会泄露未发现真相
```

进入 2D 阶段时，优先可视化：

```text
1. 建筑和设施状态
2. 任务进度
3. 施工中 / 停滞 / 完成
4. 已发现线索的位置
5. 楼栋居民状态估计
6. 玩家已知信息，而不是真实后台全貌
```

---

## 18. 文本原型 v0.1 的核心原则

最后再次明确，本原型必须遵守以下原则：

### 18.1 命令不是结果

玩家可以命令任何事，但事情能不能做成，由资源、权限、能力、心理和社会关系决定。

### 18.2 事件来自状态

后台事件不是固定剧本，而是从任务压力、角色动机、资源机会、监督强弱、居民状态中自然生成。

### 18.3 玩家不是全知

真实事件不自动进入玩家视野。玩家只能通过渠道、线索和证据逐步认知。

### 18.4 AI 不是规则引擎

AI 可以解析、表达、润色、生成提案，但不能绕过规则直接决定世界结果。

### 18.5 善治和恶治都要成立

系统不是为了惩罚玩家，而是根据现实逻辑反馈后果。合理审批、透明监督、缓解压力应带来稳定；强压、失信、资源不足、信息扭曲应积累风险。

### 18.6 先验证心脏，再做皮肤

文本原型的意义是验证世界是否会自己跳动。只有心脏能跳，2D 像素地图才有意义。

---

## 19. 文档结论

文本原型 v0.1 是整个项目从设想到工程的第一道门。

它不追求完整内容，而追求一个可运行的核心闭环：

```text
玩家命令
→ 现实约束
→ 任务执行
→ 后台演化
→ 信息不完全
→ 玩家再决策
```

如果这个闭环成立，后续的 2D 地图、AI 楼长会议、自由造物、季节系统、起义系统和长期社区演化才有真实基础。

