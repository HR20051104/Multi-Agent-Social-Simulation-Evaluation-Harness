# Community AI Sandbox v2 — Rule Mode Prototype

**Dynamic Influence–Signal Three-Layer Architecture**

## 架构概览

```
Social Network Layer  社会网络层 → 人、组织、派系
World Object Layer    世界对象层 → 建筑、资源、任务、职位
Evidence-Signal Layer 证据-信号层 → 命令、承诺、谣言、线索、记忆
```

核心原则：**玩家命令不是结果。** 每个命令生成 Signal + Disturbance + WorldObject 变化，沿网络传播、衰减、叠加。玩家只看到认知投影。

## 运行

```bash
cd prototype_v2/community_ai_sandbox_v2
python main.py
```

## 命令列表

```
help / status / report     查看状态
nodes / node <id>          社会节点
edges <id>                 社会边
objects / tasks / signals  世界对象/任务/信号
knowledge                  玩家认知
tick / wait <n>            推进时间

assign_task <agent> <type> <budget> <mat> <labor>
approve_task <id> <budget> <mat> <labor>
force_task <id>

appoint <node> <pos>       任命
appoint_deputy <node> <pos> 任命副职
promise <target> <topic> <deadline>
public_rebuke <node>       公开训斥
private_warning <node>     私下警告

audit <target>             审计
plant_informant <target>   安排眼线
meeting                    楼长会议
debug_true                 [调试] 完整状态
```

## 测试

```bash
cd tests
python run_scenarios.py
```

7 个测试剧本：
1. 行动直接作用于人（公开训斥 → stress↑ fear↑ trust↓）
2. 不给经费强制建造（任务 blocked，压力累积）
3. 正常审批顺利完工（预算流动，进度推进）
4. 承诺与信号传播
5. 边缘节点中心性跃迁（R1 任命 → core_score 5→25）
6. 隐藏信号泄露与眼线发现
7. 玩家不操作世界继续运行（8 ticks 不崩）

## 项目结构

```
greatest_creation/
├── src/                              ← 核心引擎（长期复用）
│   ├── models.py                     ← 全部 dataclass
│   ├── world.py                      ← 世界管理 + tick 编排
│   ├── world_clock.py                ← 持续时钟
│   ├── social_network.py             ← 社会节点/边管理
│   ├── influence_engine.py           ← 扰动传播
│   ├── signal_engine.py              ← 信号传播/变形/泄露
│   ├── task_engine.py                ← 任务作为 WorldObject
│   ├── event_engine.py               ← 自主事件生成
│   ├── evidence_engine.py            ← Trace/Clue/Memory
│   ├── centrality_engine.py          ← 中心性计算
│   ├── cognition_engine.py           ← 玩家认知投影
│   └── report_engine.py              ← 可见报告
│
├── prototype_v2/
│   └── community_ai_sandbox_v2/
│       ├── main.py                   ← CLI
│       ├── command_parser.py         ← 命令解析
│       └── tests/run_scenarios.py    ← 7 个测试
│
└── prototype/                        ← v1 旧原型（保留）
```

## 与 v1 的关键区别

| v1 | v2 |
|----|----|
| TaskEngine 是核心骨架 | 任务是 WorldObject 的一种 |
| Event 是随机后台事件 | Event 来自社会网络条件 |
| true_state / observed_state | 三层架构 + 信号传播 |
| next_day 回合制 | tick 持续时钟 |
| Agent 包含一切属性 | SocialNode + WorldObject 分离 |
| chief.trust_to_X 存在 | 不刻画玩家对他人信任 |
| 固定核心圈 | 中心性动态计算，支持跃迁 |

## 验收状态

- [x] python main.py 可启动
- [x] tick/wait 持续运行，玩家不操作世界也推进
- [x] 社会网络只包含人/组织节点
- [x] 世界对象不参与 trust/fear/loyalty
- [x] 行动可直接作用于社会网络（public_rebuke 不需要 trace）
- [x] 命令转为 Signal + Disturbance + WorldObject change
- [x] 扰动传播/衰减/叠加
- [x] 信号传播/衰减/变形/泄露
- [x] Trace → Clue 置信度管道
- [x] 玩家 report 不显示真实后台
- [x] 不刻画 CHIEF 对他人的 trust/preference
- [x] 任务作为 WorldObject 执行
- [x] 职位作为 WorldObject，任命改变中心性
- [x] 边缘节点中心性跃迁（R1: 5→25）
- [x] 7 个测试剧本全部通过
