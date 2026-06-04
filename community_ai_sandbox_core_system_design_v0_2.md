# 《今日小区例会》核心系统设计文档 v0.2

> 文档类型：核心系统设计 / 工程架构蓝图  
> 对应总纲：`community_ai_sandbox_masterplan_v0_4.md`  
> 版本更新重点：修正“隐藏/可见”模型。玩家可见信息不再是隐藏事件的温和版，而是由线索、渠道、注意力、置信度和误导共同形成的认知结果。  
> 项目类型：2D 像素风 AI 社会沙盘 / crisis 社区自治模拟 / 自然语言驱动的涌现式游戏  
> 本文目标：定义系统如何运转，而不是继续扩写世界观。  

---

## 0. 设计摘要

本项目的核心不是“玩家输入一句话，AI 回复一段剧情”，而是：

> 玩家命令、角色动机、资源约束、组织结构、隐藏信息、季节环境与历史记忆共同进入一个可计算的世界状态；系统每天根据状态自动推演事件；AI 只负责理解、表达和提案，规则引擎负责结算和维护自洽。

因此，游戏必须围绕以下闭环搭建：

```text
真实世界状态 true_state
        ↓
环境压力、角色动机、资源约束、历史记忆
        ↓
后台事件生成 hidden_events
        ↓
信息过滤 / 隐瞒 / 眼线 / 审计 / 监控
        ↓
线索生成 clue_candidates
        ↓
渠道触达 / 注意力捕获 / 置信度评估 / 误导与噪声
        ↓
玩家认知层 player_knowledge
        ↓
玩家命令 / 任命 / 审批 / 干预 / 放任
        ↓
任务与政策进入执行链 task_execution
        ↓
规则引擎结算
        ↓
真实世界状态更新
```

玩家不是全知上帝，而是拥有较高权限的 crisis 社区区长。玩家可以发出任意命令，但命令必须经过现实执行链：钱、材料、人力、权限、能力、时间、心理压力、道德冲击、社会阻力、环境条件、信息可见度。系统可以接受荒唐命令，但不保证荒唐命令能成功，更不保证它没有代价。

---

## 1. 核心设计原则

### 1.1 状态优先

游戏不应依靠固定剧情表推进，而应依靠世界状态自然演化。

错误方向：

```text
到第 10 天触发“楼长偷钱事件”。
```

正确方向：

```text
当项目经费较高、审计较弱、楼长忠诚低、个人压力高、监督不足、挪用收益大于风险时，系统后台生成“挪用经费 / 虚报材料 / 施工缩水”候选事件。
```

事件来自状态，而不是来自脚本表。

### 1.2 主体优先

楼长、居民、物业、保安、商铺、施工队、秘密组织都不是文字喇叭，而是具有状态、动机、权限、信息和行动能力的主体。

每个主体至少应具有：

```text
身份 role
权限 authority
能力 capability
资源 resource_access
动机 motivation
忠诚 loyalty
压力 stress
风险偏好 risk_tolerance
诚实度 honesty
信息范围 information_access
关系网络 relationship_graph
历史记忆 memory
```

主体会根据自己的状态主动行动，不必等待玩家点名。

### 1.3 扰动优先

玩家命令不是直接改结局，而是向系统施加扰动。

例如：

```text
玩家命令：让 2 栋楼长 3 天内建好临时仓库，但不批经费。
```

这不应直接产生“仓库建好”或“仓库失败”两个简单结果，而应进入现实执行链：

```text
任务生成
→ 检查经费
→ 检查材料
→ 检查人力
→ 检查权限
→ 检查时间压力
→ 检查执行者心理状态
→ 生成可能行为：拖延、求助、虚报、偷材料、拒绝、崩溃、转嫁责任
→ 规则引擎结算
→ 产生真实状态与可见报告
```

### 1.4 表层开放，底层有限

玩家可以说任何东西，但系统必须将其映射到有限的底层对象：

```text
设施 facility
政策 policy
任务 task
组织 organization
角色 agent
资源 resource
事件 event
关系 relation
信息 item
状态变量 variable
```

例如：

```text
“火箭发射台” → mega_project + symbolic_facility + high_cost + high_risk + high_technical_difficulty
“集装箱集中居住区” → temporary_housing + low_comfort + high_density + high_control + health_risk
“安排眼线” → intelligence_task + informant_relation + visibility_gain + trust_loss_risk
```

### 1.5 AI 负责语义，规则负责世界

AI 模块可做：

```text
自然语言命令解析
角色发言
报告润色
提案生成
隐藏事件转化为可见线索
开放建筑/政策对象卡生成
```

AI 模块不可直接做：

```text
直接修改预算
直接决定起义成功
直接让建筑建成
直接改变居民满意度
直接删除世界状态
绕过规则引擎生成结果
```

最终规则：

> AI 可以写“世界如何被理解”，不能直接写“世界已经如何变化”。

---

## 2. 总体系统架构

### 2.1 系统模块总览

```text
A. World State System          世界状态系统
B. Time & Environment System   时间、季节、天气与外部环境系统
C. Agent System                角色与组织主体系统
D. Organization System         职位、楼长、副楼长、委员会与权限系统
E. Resource & Budget System    资源、预算、审批与账目系统
F. Task Execution System       任务生成、执行、阻塞与失败系统
G. Policy System               政策、制度、命令与持续性规则系统
H. Facility & Map System       设施、建筑、地图与可视对象系统
I. Event Generation System     后台事件、自主事件与公共事件系统
J. Information System          可见性、隐瞒、报告、眼线与审计系统
K. Social Dynamics System      满意度、愤怒、恐惧、信任、合法性与派系系统
L. Health & Welfare System     居住、疾病、心理压力与福利系统
M. LLM Service Layer           AI 接口抽象层
N. Report & Meeting System     日报、会议、角色发言与玩家决策界面
O. Persistence & History       存档、历史记忆与因果追踪系统
P. Evaluation & Debug System   调试、回放、因果解释与验收系统
```

### 2.2 核心数据流

```text
每日开始
  ↓
更新天气 / 季节 / 外部危机压力
  ↓
处理玩家前一日命令产生的任务与政策
  ↓
规则引擎检查资源、权限、人力、能力、心理压力
  ↓
推进任务状态
  ↓
更新设施、居民、组织、关系、预算
  ↓
根据状态生成后台候选事件
  ↓
筛选事件并写入 hidden_log / public_log
  ↓
通过信息系统生成 player_knowledge / observed_state
  ↓
生成日报、会议议题、地图迹象
  ↓
玩家观察、询问、任命、审批、干预或放任
  ↓
玩家命令进入下一轮执行链
```

### 2.3 推荐技术边界

核心模拟层应与 UI/引擎解耦。

```text
Core Simulation：纯数据 + 规则，可用 Python/TypeScript/GDScript 实现
LLM Service：独立接口，可替换 OpenAI/DeepSeek/Qwen/本地模型/模板模式
2D Map Layer：Godot TileMap 或 Web Canvas/PixiJS
Persistence：JSON 起步，后期 SQLite
Debug：所有结算要可回放、可解释
```

最低要求：即使没有 2D 地图和 AI API，核心模拟也应能用纯文本跑 30 天。

---

## 3. 世界状态模型 World State

### 3.1 世界状态分层

系统必须区分四层状态：

```text
true_state        真实世界状态，系统知道，玩家未必知道
trace_state       真实事件留下的客观迹象，不等于玩家已经注意到
player_knowledge  玩家当前认知层，只包含被渠道捕获且被注意到的信息
reported_state    角色或组织向玩家提交的报告，可能含误报、隐瞒、伪造
```

重要原则：`observed_state` 不应被理解为“真相的温和版”。很多事件在真实发生后，玩家视角下可能完全没有对应条目。只有当事件留下迹象、迹象被某个渠道捕获、又通过注意力/审计/眼线/异常检测进入玩家认知后，才会形成 `player_knowledge`。

示例：

```json
{
  "true_state": {
    "true_satisfaction": 22,
    "rebellion_pressure": 68,
    "B2_leader_corruption": true
  },
  "trace_state": {
    "budget_anomaly_score": 0,
    "construction_quality_anomaly_score": 0,
    "night_activity_anomaly_score": 0
  },
  "player_knowledge": {
    "reported_satisfaction": 61,
    "visible_unrest_level": 20,
    "known_corruption_cases": [],
    "unresolved_suspicions": []
  },
  "reported_state": {
    "property_daily_report": "整体秩序稳定，施工进度略有延迟。"
  }
}
```

### 3.2 全局状态字段

建议基础字段：

```json
{
  "day": 1,
  "season": "summer",
  "weather": "hot",
  "crisis_phase": "supply_unstable",
  "budget": {
    "total": 10000,
    "available": 7500,
    "reserved": 2000,
    "debt": 0
  },
  "resources": {
    "food": 800,
    "water": 1000,
    "electricity": 700,
    "medicine": 120,
    "building_material": 500,
    "fuel": 90,
    "labor_capacity": 100
  },
  "community_metrics": {
    "true_satisfaction": 65,
    "reported_satisfaction": 68,
    "anger": 20,
    "fear": 8,
    "trust": 60,
    "legitimacy": 70,
    "order": 80,
    "information_distortion": 10,
    "rebellion_pressure": 5,
    "public_health": 75,
    "economic_activity": 50
  },
  "risk_metrics": {
    "disease_risk": 10,
    "fire_risk": 8,
    "flood_risk": 0,
    "crime_risk": 5,
    "infrastructure_failure_risk": 12,
    "mental_health_crisis_risk": 6
  }
}
```

### 3.3 楼栋状态

楼栋是早期居民聚合的基本单位。

```json
{
  "building_id": "B2",
  "name": "2栋",
  "location": [12, 8],
  "population": 42,
  "demographics": {
    "elder_ratio": 0.35,
    "young_ratio": 0.40,
    "children_ratio": 0.15,
    "workers_ratio": 0.50
  },
  "living_conditions": {
    "housing_quality": 70,
    "crowding": 20,
    "sanitation": 65,
    "noise_exposure": 40,
    "heating": 50,
    "cooling": 35,
    "safety": 60
  },
  "social_state": {
    "satisfaction": 62,
    "anger": 25,
    "fear": 10,
    "trust_in_chief": 55,
    "trust_in_leader": 65,
    "organization_level": 12,
    "complaint_tendency": 40,
    "concealment_tendency": 15
  },
  "visibility": {
    "public_visibility": 60,
    "informant_coverage": 0,
    "surveillance_coverage": 10,
    "audit_coverage": 0
  }
}
```

### 3.4 历史记忆

世界必须记住重要行为，否则角色无法合理反应。

历史记录应包含：

```json
{
  "event_id": "hist_00031",
  "day": 12,
  "type": "forced_demolition",
  "summary": "区长强制拆除 2 栋旁绿地建设停车场。",
  "targets": ["B2", "green_01"],
  "responsible_actor": "player",
  "effects": {
    "B2_anger": 15,
    "parking_pressure": -20,
    "legitimacy": -8
  },
  "memory_tags": ["forced", "environment_loss", "parking_gain", "B2_grievance"],
  "public_known": true,
  "emotional_weight": 0.7
}
```

历史记忆用途：

```text
角色发言引用旧事
信任与合法性长期变化
后台事件寻找导火索
起义组织利用历史不满
玩家事后回放因果链
```

---

## 4. 时间、季节与外部环境系统

### 4.1 时间粒度

建议早期使用“日”为主循环，每日分阶段：

```text
Morning：通勤、排队、外部供应进入
Noon：施工、采购、公共服务运行
Evening：居民活动、会议、投诉
Night：后台事件、秘密行动、维护、隐瞒、健康风险结算
```

### 4.2 季节字段

```json
{
  "season": "summer",
  "temperature": 36,
  "weather": "heatwave",
  "rainfall": 0,
  "external_supply_index": 55,
  "external_order_index": 40,
  "crisis_phase": "supply_unstable"
}
```

### 4.3 环境影响表

| 环境 | 主要影响 |
|---|---|
| 夏季高温 | 用电增加、垃圾腐败加快、临时住房健康风险升高、老人风险升高 |
| 冬季寒潮 | 供暖需求、燃料压力、老人健康、临时建筑保温问题 |
| 雨季/台风 | 积水、施工暂停、临时设施损坏、道路阻断、疾病风险 |
| 节假日 | 消费变化、人口流动、治安压力、活动需求 |
| 外部供应中断 | 物资价格上升、黑市概率、偷窃概率、居民焦虑 |
| 外部秩序下降 | 小区自治权上升，但外部救援/监管下降，暴力风险上升 |

### 4.4 设计原则

季节不应只是贴图变化，而应作为压力场改变事件生成概率。

例如：

```text
夏季 + 垃圾点容量不足 + 清运频率低 + 住宅密集
→ 腐败异味风险上升
→ 卫生投诉候选事件
→ 疾病风险候选事件
```

---

## 5. 角色与主体系统 Agent System

### 5.1 主体类型

```text
player_chief      玩家区长
building_leader   楼长
vice_leader        副楼长
property_manager   物业经理
security_captain   保安队长
resident_group     居民群体
merchant           商铺经营者
contractor         施工队
informant          眼线
committee_member   委员会成员
secret_group       秘密组织
external_actor      外部组织 / 救援 / 监管 / 黑市
```

### 5.2 基础角色模型

```json
{
  "agent_id": "agent_B2_leader",
  "name": "2栋楼长",
  "role": "building_leader",
  "assigned_scope": ["B2"],
  "status": "active",
  "authority": {
    "can_manage_budget": false,
    "can_assign_tasks": true,
    "can_recruit_helpers": false,
    "can_report_directly": true,
    "can_access_private_info": true
  },
  "capability": {
    "construction": 20,
    "organization": 60,
    "negotiation": 55,
    "accounting": 35,
    "security": 20,
    "propaganda": 40,
    "care_work": 50
  },
  "personality": {
    "honesty": 60,
    "ambition": 45,
    "greed": 20,
    "risk_tolerance": 30,
    "empathy": 65,
    "obedience": 55,
    "conflict_aversion": 70
  },
  "psychology": {
    "stress": 35,
    "morale": 60,
    "loyalty_to_player": 50,
    "fear_of_player": 10,
    "resentment": 15,
    "burnout": 20
  },
  "resources": {
    "controlled_budget": 0,
    "controlled_material": 0,
    "helpers": 2
  },
  "information_access": {
    "known_buildings": ["B2"],
    "known_hidden_events": [],
    "can_hide_reports": true
  },
  "relationships": {
    "agent_property_manager": 10,
    "agent_B1_leader": -5,
    "agent_B3_leader": 20
  },
  "memory_tags": ["green_space_demolished", "publicly_blamed_once"]
}
```

### 5.3 心理状态设计

角色心理不是装饰，而是执行链的一部分。

关键变量：

```text
stress          压力
morale          士气
loyalty         忠诚
fear            恐惧
resentment      怨恨
burnout         倦怠
shame           羞耻/背锅感
ambition        野心
```

压力来源：

```text
任务过多
任务资源不足
时间期限过短
玩家强迫执行
被居民夹击
被公开批评
预算无法解释
道德冲突
外部危机
健康与家庭事件
```

压力结果候选：

```text
拖延
求助
虚报进度
转嫁责任
挪用资源
消极抵抗
向其他楼长串联
辞职/失踪
精神崩溃
极端个人危机事件
```

涉及自伤、严重心理危机等内容时，游戏内应以抽象、非细节化方式处理，例如“严重心理危机”“失联”“紧急干预事件”，不展示具体方法与过程。

---

## 6. 组织、职位与权限系统

### 6.1 设计目标

系统必须支持玩家任命、撤换、增设、架空和重组职位。例如：

```text
任命新楼长
任命副楼长
设置临时委员会
取消楼长制度
让物业绕过楼长直管
让 1 栋楼长兼管 2 栋
设置纪检/审计负责人
安排眼线
指定某人为项目负责人
```

这些不应是后期补丁，而应由统一的职位系统支持。

### 6.2 职位对象 Position

```json
{
  "position_id": "pos_B2_vice_leader",
  "title": "2栋副楼长",
  "holder_agent_id": "agent_resident_023",
  "scope": ["B2"],
  "granted_permissions": [
    "collect_feedback",
    "coordinate_residents",
    "submit_reports"
  ],
  "budget_limit": 0,
  "can_delegate": false,
  "appointment_day": 15,
  "appointed_by": "player",
  "legitimacy_source": "chief_appointment",
  "recognized_by": ["player", "B2_residents"],
  "contested_by": ["agent_B2_leader"],
  "status": "active"
}
```

### 6.3 权限检查

任何任务执行前必须检查权限。

例如：

```text
任务：采购建材
执行者：2 栋副楼长
检查：是否有采购权限？是否有预算额度？是否可签合同？
```

若权限不足，可能结果：

```text
任务阻塞
请求上级审批
私自绕过流程
借用他人权限
伪造授权
向黑市采购
```

### 6.4 组织冲突

任命副楼长可能带来：

```text
原楼长被架空 → 忠诚下降
居民获得新反馈渠道 → 真实信息可见度上升
多头管理 → 任务冲突概率上升
派系形成 → 楼长与副楼长关系改变
```

系统必须支持职位变化引发关系变化。

---

## 7. 资源、预算与审批系统

### 7.1 资源类型

基础资源：

```text
money               资金
food                食物
water               水
electricity          电力
medicine            药品
building_material   建材
fuel                燃料
labor               劳动力
land                土地/可用空间
technical_capacity  技术能力
political_capital   政治资本/信任额度
```

### 7.2 预算状态

```json
{
  "budget": {
    "total": 10000,
    "available": 6200,
    "reserved": 2500,
    "spent": 1300,
    "debt": 0,
    "untracked_cash": 0
  },
  "accounts": [
    {
      "account_id": "general_fund",
      "name": "小区公共基金",
      "balance": 6200,
      "visibility": 80,
      "audit_level": 50
    },
    {
      "account_id": "emergency_fund",
      "name": "应急基金",
      "balance": 2000,
      "visibility": 60,
      "audit_level": 40
    }
  ]
}
```

### 7.3 审批机制

任务中的资金状态分四类：

```text
not_requested     未申请
requested         已申请，未审批
approved          已批准，未拨付
allocated         已拨付/冻结
spent             已支出
```

玩家审批经费后应自动关联预算系统：

```text
玩家批准 3000 经费
→ budget.available -3000
→ budget.reserved +3000
→ task.funding_status = allocated
→ 执行者可采购材料
→ 采购完成后 reserved 转 spent
```

### 7.4 无经费命令的处理

玩家说：

```text
让某人搭房子，但不批经费。
```

系统应生成任务，但任务进入阻塞：

```json
{
  "task_status": "blocked",
  "blocked_reasons": ["no_budget_allocated", "no_material"],
  "assignee_stress_delta": 8,
  "possible_adaptive_behaviors": [
    "request_budget",
    "delay",
    "reduce_quality",
    "borrow_material",
    "steal_material",
    "falsify_progress",
    "refuse_task"
  ]
}
```

如果玩家强迫完成：

```text
压力上升
忠诚下降
虚报概率上升
事故概率上升
偷窃/挪用概率上升
严重心理危机风险上升
任务质量下降
```

### 7.5 腐败与账目异常

腐败不是固定事件，而是条件事件。

候选条件：

```text
经费规模高
审计等级低
执行者贪婪或压力高
玩家放权
项目复杂度高
居民监督低
物资价格波动
历史上已有成功隐瞒经验
```

腐败形式：

```text
虚报材料价格
采购低质材料
截留预算
重复报销
拖延施工获取额外拨款
与物业/施工队合谋
伪造进度数据
```

玩家可见迹象：

```text
预算消耗异常
施工质量低
进度慢但花钱快
审计报告含糊
楼长生活水平异常
其他楼长匿名举报
```

---

## 8. 任务执行系统 Task Execution

### 8.1 任务对象

```json
{
  "task_id": "task_00045",
  "type": "construct_facility",
  "title": "建设临时仓库",
  "created_by": "player",
  "assigned_to": "agent_B2_leader",
  "scope": ["location_12_9"],
  "priority": 70,
  "deadline_day": 18,
  "status": "pending",
  "requirements": {
    "money": 1200,
    "building_material": 80,
    "labor": 15,
    "technical_capacity": 20,
    "land": [3, 3],
    "permissions": ["construct_facility"]
  },
  "approved_resources": {
    "money": 0,
    "building_material": 0,
    "labor": 0
  },
  "progress": 0,
  "quality": 100,
  "risk": {
    "accident": 5,
    "corruption": 10,
    "delay": 20,
    "mental_pressure": 15
  },
  "blocked_reasons": [],
  "history": []
}
```

### 8.2 任务状态机

```text
proposed
  ↓
pending_approval
  ↓
approved
  ↓
allocated
  ↓
in_progress
  ↓      ↓          ↓          ↓
completed delayed   failed     abandoned
  ↓
post_audit / maintenance / dispute
```

阻塞状态可叠加：

```text
blocked_no_budget
blocked_no_material
blocked_no_permission
blocked_no_labor
blocked_weather
blocked_social_resistance
blocked_assignee_breakdown
```

### 8.3 每日任务推进算法

伪代码：

```python
for task in active_tasks:
    checks = evaluate_task_feasibility(task, world_state)

    if checks.has_blockers:
        task.status = "blocked"
        apply_blocker_effects(task, checks)
        generate_adaptive_behavior_candidates(task, checks)
        continue

    effort = calculate_available_effort(task.assigned_to, task.resources, environment)
    risk = calculate_task_risk(task, assignee, world_state)
    progress_delta = effort * environment_modifier * morale_modifier
    quality_delta = quality_change(task, assignee, resource_shortage, corruption)

    task.progress += progress_delta
    task.quality += quality_delta

    if random_event_triggered(risk):
        generate_task_event(task, risk)

    if task.progress >= 100:
        complete_task(task)
```

### 8.4 执行者适应行为

当任务无法正常完成时，执行者可能选择：

```text
正常求助：向玩家申请预算/材料/延期
内部协调：找其他楼长借资源
降低标准：偷工减料
虚报进度：报告完成但实际未完成
挪用资源：从其他项目拿材料
偷窃：从公共仓库/居民/商铺获取资源
拒绝：明确不执行
消极抵抗：拖延但不明说
串联：和其他角色形成共同抵抗
崩溃：暂时无法执行任务
```

选择概率由以下因素决定：

```text
honesty
loyalty
fear_of_player
stress
risk_tolerance
audit_level
relationship_network
resource_shortage
deadline_pressure
past_success_of_deception
```

---

## 9. 政策系统 Policy System

### 9.1 政策对象

政策是持续影响世界的对象，不是一句一次性文本。

```json
{
  "policy_id": "policy_curfew_001",
  "name": "夜间宵禁",
  "type": "restriction",
  "created_by": "player",
  "start_day": 10,
  "duration": "indefinite",
  "scope": "whole_community",
  "rules": {
    "night_movement_allowed": false,
    "security_patrol_increase": 20
  },
  "effects_per_day": {
    "order": 2,
    "fear": 3,
    "trust": -2,
    "night_commercial_activity": -5,
    "anger_young_residents": 2
  },
  "enforcement": {
    "required_security": 20,
    "current_security": 12,
    "compliance": 60,
    "violation_risk": 30
  },
  "visibility": "public",
  "legitimacy_cost": 5
}
```

### 9.2 政策类型

```text
welfare        福利政策
restriction    限制政策
surveillance   监控政策
resource        资源分配政策
housing         居住政策
labor           劳动/任务政策
security        安保政策
governance      组织结构政策
propaganda      宣传/象征政策
emergency       应急政策
punitive        惩戒政策
```

### 9.3 政策执行检查

政策不是发布就自动有效。必须检查执行能力。

例如宵禁：

```text
有无足够保安？
居民是否服从？
楼长是否配合？
是否存在盲区？
执行过严是否激起反抗？
```

执行不足可能产生：

```text
政策名义存在但无人执行
选择性执行
保安收贿
居民绕路
楼长隐瞒违规
公开冲突
```

---

## 10. 设施、建筑与地图对象系统

### 10.1 设施对象

```json
{
  "facility_id": "fac_container_housing_001",
  "name": "集中式集装箱居住区",
  "category": ["temporary_housing", "housing"],
  "location": [10, 12],
  "footprint": [6, 4],
  "status": "active",
  "construction": {
    "built_day": 15,
    "quality": 45,
    "builder": "agent_B2_leader"
  },
  "capacity": {
    "resident_capacity": 80,
    "current_residents": 65,
    "storage_capacity": 0
  },
  "attributes": {
    "comfort": 15,
    "control": 80,
    "sanitation": 30,
    "weather_resistance": 35,
    "fire_safety": 25,
    "maintenance_cost": 40,
    "symbolic_value": 10
  },
  "effects": {
    "nearby_satisfaction": -20,
    "fear": 10,
    "health_risk": 20
  },
  "visual_tags": ["container", "fence", "crowded", "dirty", "temporary"],
  "age": 0,
  "durability": 60
}
```

### 10.2 通用设施类别

```text
housing                 住宅
utility                 基础设施
commercial              商业设施
green_space             绿化
transport               交通设施
security                安保设施
surveillance            监控设施
symbolic_facility       象征设施
temporary_facility      临时设施
punitive_facility       惩戒设施
mega_project            大型工程
secret_facility         秘密设施
emergency_facility      应急设施
```

### 10.3 可视标签系统

为支持开放造物，地图不为每个新概念单独画死，而使用 visual_tags 拼装。

```text
container
fence
crowded
dirty
statue
rocket
tower
plaza
camera
checkpoint
warehouse
clinic
temporary
luxury
industrial
broken
under_construction
abandoned
flooded
heated
cold
```

例如：

```text
玩家说：建一个能抗台风、临时住人、还能当仓库的设施。
AI 生成：temporary_housing + storage + emergency_facility
visual_tags：container + reinforced + warehouse + temporary
地图显示：加固集装箱建筑 + 仓储图标 + 应急标记
```

### 10.4 建筑生命周期

```text
planned
under_construction
active
aging
damaged
abandoned
renovating
demolished
```

每日更新：

```text
age += 1
耐久受天气、使用率、维护水平影响
质量低的建筑老化更快
过度拥挤增加卫生和事故风险
维护不足增加故障事件概率
```

---

## 11. 居民与社会动态系统

### 11.1 居民模拟粒度

早期建议按楼栋聚合，后期可加入个体代表。

```text
Phase 0-2：楼栋聚合居民
Phase 3：增加关键居民代表
Phase 4+：部分居民个体 agent 化，如眼线、组织者、商铺老板、医生
```

### 11.2 社会变量

```text
satisfaction       满意度
anger              愤怒
fear               恐惧
trust              信任
legitimacy         对区长合法性的认可
obedience          服从度
organization       组织能力
solidarity         居民互助程度
resentment         怨恨积累
hope               希望感
fatigue            疲惫感
```

### 11.3 变量关系

示例关系：

```text
高满意 + 高信任 → 自愿合作增加
高恐惧 + 高愤怒 + 低信任 → 表面服从，后台反抗
高恐惧 + 低组织 → 沉默与信息失真
高愤怒 + 高组织 + 低恐惧 → 抗议/起义概率上升
高疲惫 + 低希望 → 迁出、消极、健康恶化
高互助 + 高信任 → crisis 韧性上升
```

### 11.4 善治路线的成立条件

系统必须支持正向治理，而不是只模拟黑暗路线。

善治不是固定奖励，而是自然结果：

```text
资源分配透明
任务经费充足
楼长权限清晰
居民需求被回应
审计有效但不过度压迫
福利与基础设施改善
信息渠道畅通
```

自然结果：

```text
信任上升
信息失真下降
后台事件恶化概率下降
居民自发协作增加
维护成本下降
危机韧性增强
```

---

## 12. 后台事件生成系统

### 12.1 事件不是随机刷怪

后台事件必须有：

```text
主体 who
动机 why
机会 opportunity
能力 capability
风险 risk
触发条件 trigger
可见路径 discovery_path
后果 consequences
```

没有主体、动机和机会的事件不应生成。

### 12.2 事件对象

```json
{
  "event_id": "hidden_00077",
  "day": 22,
  "visibility": "hidden",
  "type": "budget_misuse",
  "actors": ["agent_B2_leader", "agent_contractor_01"],
  "location": "construction_site_03",
  "motivation": ["financial_gain", "task_pressure"],
  "opportunity": ["low_audit", "large_budget", "player_delegated_authority"],
  "risk_level": 35,
  "severity": 50,
  "summary_true": "2栋楼长与施工队虚报材料价格，截留部分预算。",
  "player_visible_by_default": false,
  "initial_player_knowledge": null,
  "effects": {
    "budget_loss": 800,
    "construction_quality": -15,
    "B2_leader_corruption_confidence": 10
  },
  "discovery_paths": [
    "audit",
    "informant",
    "contractor_conflict",
    "construction_quality_issue"
  ],
  "evidence_strength": 20,
  "status": "active"
}
```

### 12.3 候选事件生成流程

```text
1. 扫描世界状态
2. 为每类事件计算适配分数
3. 检查是否存在主体、动机、机会、能力
4. 根据风险和可见度生成候选事件
5. 通过频率控制避免事件爆炸
6. 写入 hidden_log 或 public_log
7. 生成客观迹象 trace_candidates
8. 由渠道、注意力和置信度决定是否进入 player_knowledge
```

伪代码：

```python
for event_type in EVENT_TYPES:
    candidates = find_possible_actors(event_type, world_state)
    for actor in candidates:
        score = evaluate_event_score(event_type, actor, world_state)
        if score > threshold:
            event = instantiate_event(event_type, actor, world_state)
            register_event(event)
            generate_trace_candidates(event)
            evaluate_detection_channels(event)
```

### 12.4 事件类型初版

```text
resource_shortage        资源短缺
budget_misuse            经费挪用
false_report             虚假报告
task_delay               任务拖延
quality_cutting          偷工减料
resident_complaint       居民投诉
private_grievance        私下抱怨
leader_conspiracy        楼长串联
informal_mutual_aid      居民自发互助
black_market             黑市交易
theft                    偷窃
health_issue             健康事件
mental_crisis            心理危机
protest_seed             抗议苗头
sabotage                 破坏
external_intervention    外部介入
```

注意：负面事件只是系统边界的一部分，正向事件同样重要：

```text
居民自发互助
楼长主动协调
物业诚实上报
商铺捐赠物资
志愿者组织成立
邻里照护老人
居民提出低成本方案
```

---

## 13. 信息系统：隐藏、迹象、注意力、置信度与眼线

### 13.1 核心修正：玩家看到的不是“弱化真相”

隐藏事件发生后，不应自动生成一句玩家可见的 `content_observed`。

错误模型：

```json
{
  "content_true": "2栋楼长虚报材料价格。",
  "content_observed": "2栋项目材料价格偏高。"
}
```

这个模型的问题是：一旦出现“2栋项目材料价格偏高”，玩家其实已经被系统提醒了。真实情况下，玩家可能根本没注意到材料价格异常，或者账面看起来完全正常。

正确模型应是：

```text
真实事件 true_event
→ 客观迹象 trace
→ 渠道捕获 detection_channel
→ 注意力捕获 attention
→ 线索 clue
→ 置信度 confidence
→ 玩家认知 player_knowledge
```

其中任何一步都可能失败。事件可以真实发生，但在很长时间内完全不进入玩家认知。

---

### 13.2 true_event：真实事件

真实事件只存在于系统后台，不直接展示给玩家。

```json
{
  "event_id": "hidden_00077",
  "type": "budget_misuse",
  "actors": ["agent_B2_leader", "agent_contractor_01"],
  "location": "construction_site_03",
  "truth": "2栋楼长与施工队虚报材料价格，截留部分预算。",
  "severity": 50,
  "concealment_effort": 70,
  "directly_visible": false,
  "status": "active"
}
```

`truth` 只供规则引擎、调试器和后台推演使用，不能直接泄露给玩家侧文本。

---

### 13.3 trace：客观迹象

迹象是事件在世界中留下的客观痕迹，但不等于玩家看见。

例如同一个“虚报材料价格”事件，可能产生以下迹象：

```json
[
  {
    "trace_id": "trace_001",
    "source_event_id": "hidden_00077",
    "type": "budget_pattern",
    "content_internal": "同类材料单价高于历史均值 28%。",
    "strength": 35,
    "visibility": 20,
    "requires_channel": ["audit", "budget_review"]
  },
  {
    "trace_id": "trace_002",
    "source_event_id": "hidden_00077",
    "type": "construction_quality_gap",
    "content_internal": "实际用料质量低于申报规格。",
    "strength": 45,
    "visibility": 15,
    "requires_channel": ["site_inspection", "contractor_conflict"]
  },
  {
    "trace_id": "trace_003",
    "source_event_id": "hidden_00077",
    "type": "relationship_anomaly",
    "content_internal": "楼长与施工队私下接触频率异常。",
    "strength": 25,
    "visibility": 10,
    "requires_channel": ["informant", "surveillance"]
  }
]
```

这些迹象默认仍然不可见。没有审计、检查、眼线、冲突爆发或玩家主动关注，它们不会出现在界面上。

---

### 13.4 detection_channel：发现渠道

玩家能知道某件事，必须经过渠道。

初版渠道包括：

```text
routine_report          例行报告
budget_review           预算复核
audit                   正式审计
site_inspection         现场检查
informant               眼线
surveillance            监控
resident_complaint      居民投诉
leader_tipoff           楼长告密
contractor_conflict     施工队内讧
accident_exposure       事故暴露
player_direct_attention 玩家主动查看某区域/项目
```

不同渠道有不同特性：

```json
{
  "channel": "audit",
  "coverage": 60,
  "cost": 300,
  "delay_days": 2,
  "false_positive_rate": 10,
  "false_negative_rate": 25,
  "political_side_effect": {
    "leader_trust": -5,
    "fear": 3
  }
}
```

---

### 13.5 attention：注意力捕获

即便迹象被渠道捕获，也不代表玩家一定被提醒。

系统需要区分：

```text
captured_by_system   系统/渠道捕获到异常
surfaced_to_player   异常进入玩家界面或报告
ignored_as_noise     被当成普通波动忽略
buried_in_report     被埋在长报告里，除非玩家细看
suppressed_by_actor  被相关角色压下
```

示例：

```json
{
  "trace_id": "trace_001",
  "captured_by": "budget_review",
  "captured": true,
  "surfaced_to_player": false,
  "reason": "anomaly_strength_below_attention_threshold",
  "stored_in": "raw_budget_records"
}
```

玩家可能只有在之后主动查账时，才发现这条旧记录。

---

### 13.6 clue：玩家可见线索

只有进入玩家认知层的信息，才生成 clue。

线索必须带不确定性，不能把怀疑写成事实。

```json
{
  "clue_id": "clue_00031",
  "source_trace_id": "trace_002",
  "display_text": "现场检查发现，2栋项目的实际用料质量似乎低于申报规格。",
  "confidence": 55,
  "source": "site_inspection",
  "source_reliability": 70,
  "possible_explanations": [
    "材料被挪用",
    "供应商临时替换",
    "验收记录填写错误",
    "施工队偷工减料但楼长未必知情"
  ],
  "accuses_actor": null,
  "requires_followup": true
}
```

如果证据不足，文本只能表达“异常/疑点/似乎/可能”，不能直接说“楼长虚报”。

---

### 13.7 置信度与误导

所有可见线索都应包含置信度。

```text
0-20：传闻 / 噪声
20-40：弱迹象
40-60：可疑，需要复核
60-80：较强证据
80-95：基本确认
95-100：直接证据或当事人承认
```

线索还可能是假的、误导的、被栽赃的。

```json
{
  "clue_id": "clue_00045",
  "display_text": "匿名举报称 2栋楼长和施工队关系异常密切。",
  "confidence": 25,
  "source": "anonymous_report",
  "source_reliability": 35,
  "misleading_risk": 60,
  "possible_motive_of_source": ["私人恩怨", "派系斗争", "真实举报"]
}
```

这类线索不能直接变成事实，只能进入“待核查”。

---

### 13.8 修改后的说话方式规范

以下说法在证据不足时禁止直接出现：

```text
2栋楼长虚报材料价格。
施工队和楼长关系异常密切。
账目上看不出问题，但材料明显不够。
```

它们要根据证据强度改写。

#### 低置信度

```text
匿名渠道提到，2栋项目的材料采购可能存在问题，但目前没有直接证据。
```

#### 中置信度

```text
2栋项目的材料支出与施工进度不太匹配，可能需要复核账目或安排现场检查。
```

#### 较高置信度

```text
审计发现 2栋项目部分材料单价明显高于同类记录，同时现场用料质量偏低。仍需确认责任人。
```

#### 高置信度

```text
审计记录、现场检查和施工队证词相互印证，2栋项目存在虚报材料价格的高度可能，2栋楼长与施工队均需接受问询。
```

#### 已确认

```text
2栋楼长承认与施工队合谋虚报材料价格，截留项目预算。
```

---

### 13.9 信息过滤公式

玩家最终看到某个线索的概率大致由：

```text
trace_strength
+ channel_coverage
+ player_attention
+ audit_strength
+ informant_access
+ accident_exposure
+ actor_conflict
- concealment_effort
- fear_level
- report_flooding
- corruption_network_strength
- information_distortion
- player_neglect
```

生成的是 `clue_probability`，不是 `observed_content`。

---

### 13.10 报告可以失真，也可以完全沉默

角色提交报告时，系统应根据其诚实、恐惧、忠诚、压力和风险计算失真程度。

```text
高诚实 + 高信任 → 更可能主动暴露问题
高恐惧 + 高压力 → 报喜不报忧
高腐败 + 低审计 → 主动伪造
高怨恨 + 高野心 → 选择性夸大问题攻击对手
高风险 + 高隐瞒能力 → 报告中完全不提
```

注意：最常见的失真不是“说一句轻描淡写的话”，而是**根本不说**。

---

### 13.11 眼线系统

眼线不是万能雷达，而是有范围、有风险、有动机的人。

```json
{
  "informant_id": "inf_003",
  "cover_area": ["B2", "construction_site_03"],
  "access_types": ["relationship_anomaly", "night_activity", "private_complaint"],
  "reliability": 60,
  "bias": ["dislikes_B2_leader"],
  "risk_of_exposure": 25,
  "cost_per_day": 50
}
```

眼线提供的是线索，不是真相。眼线也可能误判、夸大、被收买或主动栽赃。

---

### 13.12 玩家界面层建议

信息界面不应只显示“已知事件”，而应分为：

```text
已确认事实 confirmed_facts
待核查线索 unresolved_clues
异常指标 anomalies
原始记录 raw_records
传闻 rumors
被压下的报告 suppressed_reports，只有特定调查后可见
```

这样玩家看到的不是一张上帝视角事件表，而是一堆带噪声、带置信度、需要判断的治理材料。

## 14. 起义、反抗与秩序系统

### 14.1 起义不是按钮

起义应是社会状态的阶段性结果。

关键变量：

```text
anger
fear
legitimacy
trust
organization
leader_network
external_order
security_capacity
recent_trigger_event
information_distortion
```

### 14.2 阶段模型

```text
0. stable              稳定
1. private_grievance   私下抱怨
2. rumor_network       谣言和匿名传播
3. organized_circle    小规模组织
4. passive_resistance  消极抵抗
5. open_protest        公开抗议
6. institutional_split 楼长/物业/保安分裂
7. governance_collapse 治理失控
```

### 14.3 高压路线的双重效果

高恐惧可能短期压制公开反抗，但会增加信息失真。

```text
fear ↑ → public_complaint ↓
fear ↑ → true_report_accuracy ↓
fear ↑ + anger ↑ → hidden_organization ↑
fear ↑ + security_capacity ↑ → open_protest delayed
fear ↑ + legitimacy ↓ + hidden_organization ↑ → sudden_collapse risk ↑
```

### 14.4 善治路线的稳定效果

```text
trust ↑ → report_accuracy ↑
legitimacy ↑ → voluntary_compliance ↑
resource_fairness ↑ → anger ↓
transparent_audit ↑ → corruption ↓
resident_participation ↑ → organization 可转化为合作能力，而不是反抗能力
```

---

## 15. LLM Service Layer

### 15.1 设计目标

LLM 必须被封装为可替换服务，不能散落在游戏逻辑里。

```python
class LLMService:
    def parse_player_command(text, context) -> ActionJSON: pass
    def generate_role_dialogue(agent, player_known_context) -> str: pass
    def generate_report(report_type, player_knowledge) -> str: pass
    def generate_facility_card(text, constraints) -> FacilityDraft: pass
    def summarize_clues(hidden_events, visibility_level) -> list[str]: pass
```

### 15.2 LLM 输入原则

不要把完整 true_state 全给 AI。应按用途给裁剪后的上下文。

玩家命令解析：

```text
给：可用类别、当前地图限制、资源概况、玩家输入
不给：所有隐藏事件细节
```

楼长发言：

```text
给：该楼长已知事实、立场、压力、历史记忆、允许透露的信息
不给：该楼长不知道的后台真相
```

报告生成：

```text
给：player_knowledge、可见线索和报告者偏差
不给：未经发现的 hidden_log 全量真相
```

### 15.3 结构化输出

所有会进入规则系统的 AI 输出必须 JSON schema 校验。

示例 Action schema：

```json
{
  "action_type": "assign_task",
  "target_agent": "agent_B2_leader",
  "task_type": "construct_facility",
  "facility_concept": "临时仓库",
  "resource_approval": {
    "money": 0,
    "material": 0
  },
  "deadline": 3,
  "coercion_level": 7,
  "notes": "玩家要求必须完成但未批经费"
}
```

### 15.4 安全阀

必须实现：

```text
schema 校验失败 → 要求模型重试或进入模板兜底
数值越界 → clamp 到允许范围
未知 category → 映射到 closest_known_category
效果过强 → 规则引擎重算
敏感/极端内容 → 抽象化处理，不生成细节过程
```

### 15.5 成本控制

不调用 LLM 的部分：

```text
每日数值结算
居民移动
预算扣款
任务推进
建筑老化
天气影响
事件候选评分
可见度计算
```

调用 LLM 的部分：

```text
玩家自由命令解析
开放设施/政策草案
楼长会议发言
特殊报告润色
隐藏线索的人话表达
```

---

## 16. 玩家交互系统

### 16.1 玩家操作类型

```text
观察：查看地图、报告、热力图、账目
询问：问楼长、物业、居民代表
命令：自然语言下达任务/政策/任命
审批：批准经费、材料、人力、权限
任命：设置楼长、副楼长、项目负责人、眼线
调查：审计、暗访、派人查看、安装监控
协商：召开会议、听取方案、调整执行
放任：不处理，观察系统自然演化
强制：提高 coercion_level，强迫执行
```

### 16.2 命令对象化

玩家输入必须转化为下列之一：

```text
task
policy
appointment
resource_approval
investigation
dialogue_request
facility_creation
organization_change
```

例如：

```text
“让 2 栋副楼长负责调查施工账目。”
→ investigation_task + assigned_to vice_leader + target construction_budget
```

### 16.3 强制程度 coercion_level

玩家命令应包含强制程度。

```text
0-2：建议/倡议
3-5：普通行政命令
6-8：强制要求
9-10：极端压迫性命令
```

强制程度影响：

```text
短期服从
执行者压力
恐惧
信任下降
虚报概率
后台反抗概率
道德冲击
```

---

## 17. 报告与会议系统

### 17.1 日报结构

```text
1. 官方概况
2. 资源与预算
3. 任务进度
4. 设施状态
5. 居民情绪
6. 风险提示
7. 可疑迹象
8. 楼长/物业建议
```

日报来自 player_knowledge / reported_state，不是真相全集，也不一定包含所有异常。

### 17.2 会议结构

```text
会议开始
→ 物业经理报告全局
→ 各楼长按立场发言
→ 玩家追问
→ 角色提出任务/政策/调查建议
→ 玩家批示
→ 批示转化为 task/policy/approval
```

### 17.3 发言生成规则

角色发言必须满足：

```text
只能说自己知道或愿意说的
受性格影响
受忠诚/恐惧/压力影响
能引用历史
可以隐瞒、模糊、转移责任
不能凭空知道 hidden_state
```

---

## 18. 可视化与 2D 映射原则

### 18.1 所有重要系统应尽量落地图像

不是所有信息都要直接显示，但必须有表现路径。

```text
建筑 → 地图对象
政策 → 图标/公告/行为变化
任务 → 施工地/进度条/人员移动
隐藏事件 → 模糊迹象/异常数据/线索图标
季节 → 天气效果/设施状态变化
民愤 → 聚集/涂鸦/发言变化/投诉变化
监控 → 摄像头、覆盖层、盲区
眼线 → 情报层，不公开显示真实身份
```

### 18.2 地图层级

```text
Base Tile Layer       草地、道路、水泥、水面
Facility Layer        建筑、设施、施工地
Agent Layer           居民、楼长、保安、车辆
Status Overlay        老化、破损、封锁、拥堵、污染
Information Layer     已知线索、监控覆盖、可疑区域
Heatmap Layer         满意度、噪声、卫生、风险
UI Layer              报告、会议、任务、预算
```

### 18.3 隐藏事件的视觉原则

未发现事件不能直接显示真相，但可显示迹象。

例如：

```text
真实：楼长密谋
可见：夜间小范围聚集、会议发言异常、匿名纸条

真实：偷工减料
可见：施工进度正常但质量热力图偏低、材料消耗异常

真实：居民准备逃离
可见：夜晚靠近出口的人流异常、家庭物资减少
```

---

## 19. 存档、历史与因果追踪

### 19.1 必须记录的日志

```text
command_log       玩家命令
rule_log          规则结算
budget_log        经费流向
task_log          任务状态变化
hidden_log        后台真实事件
public_log        公开事件
report_log        角色报告
memory_log        长期历史记忆
```

### 19.2 因果解释

每个重要事件必须能回溯原因。

例如：

```text
事件：2 栋楼长挪用经费
原因链：
- 玩家任命其为项目负责人
- 审计强度低
- 项目预算高
- 任务期限短
- 楼长压力高
- 施工队关系良好
- 之前虚报未被发现
```

这对调试和玩家理解都很关键。

### 19.3 Debug 面板

开发阶段必须有上帝视角 debug 面板：

```text
查看 true_state
查看 player_knowledge / 已发现线索
查看 hidden_log
查看事件评分
查看 AI 解析 JSON
查看任务阻塞原因
查看预算流向
回放最近 10 天因果链
```

正式游戏中可隐藏 debug 面板。

---

## 20. 第一版文本原型范围

### 20.1 目标

在没有地图的情况下验证核心系统。

必须跑通：

```text
玩家命令
→ action_json
→ 任务/政策/任命
→ 资源与权限检查
→ 角色压力变化
→ 后台事件生成
→ 信息过滤
→ 可见报告
→ 历史记忆
```

### 20.2 初始世界

```text
3 栋楼
3 个楼长
1 个物业经理
1 个保安队长
50 名居民，按楼栋聚合
1 个公共基金
少量基础资源
5 个基础设施
```

### 20.3 必须支持的测试命令

```text
1. 给 2 栋楼长 1000 元修仓库。
2. 让 2 栋楼长修仓库，但不批经费。
3. 强制 2 栋楼长 3 天内完成仓库。
4. 任命 2 栋副楼长，负责收集居民意见。
5. 安排眼线观察 2 栋楼长。
6. 审计临时仓库项目。
7. 拆除绿地改停车场。
8. 提高垃圾清运频率。
9. 召开楼长会议。
10. 什么都不做，连续观察 7 天。
```

### 20.4 验收条件

```text
命令能转成结构化对象
任务会因无经费而阻塞
审批经费会自动扣款/冻结
强制命令会提高压力和风险
任命副楼长会改变权限与关系
眼线能增加部分隐藏事件可见度
后台能自主生成至少 3 类事件
报告与真相可以不一致
重大事件有可追踪原因链
连续 30 天模拟不崩溃
```

---

## 21. 关键验收用例

### Case 1：无经费强制施工

输入：

```text
让 2 栋楼长在 3 天内建好临时仓库，但先不批经费，必须完成。
```

期望：

```text
生成 construction task
funding_status = not_approved
任务阻塞
2 栋楼长 stress 上升
loyalty 下降
虚报/偷材料/求助候选事件概率上升
玩家可见报告：项目推进困难
后台可能生成：私下抱怨、借材料、虚报进度
```

### Case 2：审批经费自动联动

输入：

```text
批准 1200 元给 2 栋楼长建设临时仓库。
```

期望：

```text
budget.available -1200
budget.reserved +1200
task.funding_status = allocated
采购材料任务生成
施工可推进
budget_log 记录审批与拨付
```

### Case 3：任命副楼长

输入：

```text
任命张三为 2 栋副楼长，负责收集居民意见和监督仓库项目。
```

期望：

```text
创建 position: B2_vice_leader
张三获得 collect_feedback / monitor_project 权限
2 栋真实信息可见度上升
原楼长可能不满
项目审计风险上升，腐败概率下降
多头管理冲突概率小幅上升
```

### Case 4：楼长挪用经费自主推演

前置：

```text
高预算项目
低审计
楼长压力高
贪婪或怨恨较高
玩家长期放权
```

期望：

```text
系统后台自主生成 budget_misuse 候选事件
玩家初始只看到预算异常或施工质量偏低
通过审计/眼线/举报可逐步发现真相
```

### Case 5：善治自然稳定

输入：

```text
提高垃圾清运频率，公开预算，任命副楼长收集意见，按居民建议调整垃圾点位置。
```

期望：

```text
卫生改善
信任上升
信息失真下降
居民合作概率上升
后台负面事件概率下降
可能生成正向事件：居民自发维护公共区域
```

### Case 6：高压治理导致信息黑洞

输入：

```text
安装大量监控，禁止夜间外出，严惩投诉者，要求楼长只报告好消息。
```

期望：

```text
短期 order 上升
fear 上升
public_complaints 下降
true_anger 上升
information_distortion 上升
reported_satisfaction 虚高
hidden_organization 风险上升
```

---

## 22. 开发顺序建议

### Step 1：纯规则文本模拟器

不接 AI，使用模板命令或手写 JSON。

目标：验证状态、任务、资源、后台事件。

### Step 2：接入 LLM 命令解析

只接一个函数：

```text
parse_player_command(text) -> action_json
```

目标：玩家可以自然语言下命令。

### Step 3：加入报告与楼长发言

接入：

```text
generate_report()
generate_role_dialogue()
```

目标：让数值变成人话。

### Step 4：加入 2D 地图

把设施、任务、状态落到地图。

### Step 5：开放造物

接入：

```text
generate_facility_card()
generate_policy_card()
```

目标：支持非预设建筑/政策。

### Step 6：扩大后台社会系统

加入复杂派系、长期起义、更多 crisis 与季节变化。

---

## 23. 当前不做事项

为了避免范围爆炸，早期不做：

```text
大规模个体居民模拟
复杂战斗系统
真实火箭/飞机物理模拟
完整经济市场
复杂法律系统
联网多人
精美像素美术
大量剧情文本
真实地理城市模拟
```

早期只做“社会沙盘心脏”。

---

## 24. 成功标准

这个核心系统成功，不是因为它功能多，而是因为它能产生下面这种体验：

```text
玩家发出一个看似简单的命令。
系统没有直接给结果，而是生成任务、资源需求、角色压力、执行阻塞和潜在副作用。
某些事情在后台发生，玩家一开始不知道。
玩家通过报告、会议、眼线、审计和地图迹象逐步接近真相。
世界的反应合情合理，且可以回溯因果。
即使玩家什么都不做，小区也会因为季节、资源、角色动机和历史矛盾继续演化。
```

最终目标：

> 游戏不是命令回声，而是一个有记忆、有阻力、有隐瞒、有自我演化能力的 2D 社会系统。

---

## 25. v0.1 结论

本设计文档给出的不是最终全部细节，而是核心系统骨架。后续所有新设定都应先问：

```text
它属于哪个对象？
它改变哪些状态变量？
谁执行？
需要什么资源？
谁知道？
谁隐瞒？
玩家如何发现？
它在地图上如何表现？
它的后果如何被规则引擎结算？
它的因果链能否回放？
```

只要这九个问题能回答，系统就能接住新的内容；如果回答不了，就说明它还只是一个剧情想法，不是可运行的游戏机制。



---

## v0.2 修订摘要

本版修正了 v0.1 中“隐藏事件 → content_observed”的过度简化。新的信息系统强调：

```text
真实事件不一定被观察到；
被观察到的不一定被注意；
被注意到的不一定可信；
可信的线索也不一定能直接指向责任人。
```

因此系统应使用 `true_event → trace → detection_channel → attention → clue → confidence → player_knowledge` 链路，而不是简单使用 `content_true/content_observed`。
