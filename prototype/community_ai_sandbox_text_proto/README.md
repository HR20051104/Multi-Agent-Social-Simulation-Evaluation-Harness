# Community AI Sandbox — Rule Mode Text Prototype v0.1

《今日小区例会》· Rule Mode 文本原型

## 项目概述

这是一个 AI 社会沙盘游戏的 **Rule Mode 命令行原型**。当前阶段不接 LLM API，不做 2D 地图，不做复杂 UI，只实现后台逻辑与命令行交互。

核心验证命题：**玩家命令不是结果。命令进入世界后，必须经过资源、权限、能力、心理、信息、环境和社会关系等现实条件检验，最终由系统自主推演出结果。**

## 项目结构

```
greatest_creation/                        # 项目根目录
├── src/                                  # 长期核心引擎（跨阶段复用）
│   ├── models.py                         # 所有 dataclass 数据模型
│   ├── task_engine.py                    # 任务创建、审批、推进、完成
│   ├── event_engine.py                   # 后台事件自主生成
│   ├── evidence_engine.py                # 痕迹→渠道→线索→认知链路
│   └── world.py                          # 世界状态管理、每日结算
│
├── prototype/
│   └── community_ai_sandbox_text_proto/  # 当前阶段原型
│       ├── main.py                       # CLI 入口
│       ├── command_parser.py             # 命令解析与执行
│       ├── data/
│       │   └── initial_world.json        # 初始世界状态
│       └── tests/
│           └── run_all_scenarios.py      # 5 个测试剧本
│
├── community_ai_sandbox_masterplan_v0_4.md    # 项目总纲
└── community_ai_sandbox_core_system_design_v0_2.md  # 核心系统设计
```

## 如何运行

```bash
# 进入原型目录
cd prototype/community_ai_sandbox_text_proto

# 启动 CLI
python main.py

# 运行所有测试剧本
cd tests
python run_all_scenarios.py
```

## 可用命令

| 命令 | 说明 |
|------|------|
| `help` | 显示帮助 |
| `status` | 查看当前世界状态 |
| `agents` | 查看所有角色 |
| `positions` | 查看所有职位 |
| `tasks` | 查看所有任务 |
| `knowledge` | 查看玩家认知 |
| `next_day` | 推进一天 |
| `assign_task <agent_id> <type> <budget> <materials> <labor>` | 分配任务 |
| `approve_task <task_id> <budget> <materials> <labor>` | 审批任务资源 |
| `deny_task <task_id>` | 取消任务 |
| `force_task <task_id>` | 强制推进任务 |
| `appoint <agent_id> <position_id>` | 任命 |
| `appoint_deputy <agent_id> <position_id>` | 任命副职 |
| `remove_position <position_id>` | 撤职 |
| `audit <target_id>` | 审计 |
| `plant_informant <target_id>` | 安排眼线 |
| `meeting` | 召开楼长会议 |
| `events_debug` | [调试] 查看隐藏事件 |
| `quit` | 退出 |

## 初始角色

| ID | 名称 | 角色 | 特点 |
|----|------|------|------|
| A1 | 1栋楼长 | building_leader | 务实，honesty 70, loyalty 60 |
| A2 | 2栋楼长 | building_leader | 压力敏感，honesty 45, loyalty 45, greed 45 |
| A3 | 3栋楼长 | building_leader | 保守，honesty 65 |
| A4 | 物业经理 | property_manager | 预算优先，competence 70, greed 35 |
| A5 | 保安队长 | security_chief | 秩序优先，loyalty 65 |
| A6 | 临时财务员 | treasurer | 账目管理，honesty 70, greed 15 |

## 测试剧本

### 剧本 1：不给经费强制建造
```
assign_task A2 build_storage 1000 20 5
force_task T1
next_day (多次)
→ 任务 blocked，A2 stress 飙升，可能产生虚报/抱怨等隐藏事件
```

### 剧本 2：正常审批顺利完工
```
assign_task A1 build_storage 1000 20 5
approve_task T1 1000 20 5
next_day (多次)
→ 预算冻结，进度推进，约 6 天完成，A1 压力可控
```

### 剧本 3：隐藏挪用与审计发现
```
assign_task A2 build_storage 3000 40 6
approve_task T1 3000 40 6
force_task T1
next_day (多次)
audit T1
→ A2(greed 45) 可能挪用经费/材料，审计产生置信度线索
```

### 剧本 4：任命副楼长
```
appoint_deputy A3 leader_B2
positions
meeting
→ 副楼长职位创建，原楼长 trust -5，会议反映管理结构变化
```

## 核心闭环

```
玩家命令 → 结构化 Action → Task/Policy/Investigation
→ 资源/权限/能力/心理检查
→ 每日推进 → 后台事件自主生成
→ 痕迹 → 渠道 → 线索(置信度) → 玩家认知
→ 玩家再决策
```

## 验收状态

- [x] 可以 `python main.py` 启动
- [x] 连续 `next_day` 运行 10 天不崩
- [x] 任务创建、审批、强制
- [x] 缺资源时任务不会凭空完成
- [x] 审批资源自动扣除/冻结
- [x] 执行者压力会随任务状况变化
- [x] 后台事件基于条件自动生成
- [x] 后台事件不会自动暴露给玩家
- [x] 审计/眼线等渠道可以生成线索
- [x] 线索带置信度和来源
- [x] 玩家认知与真实事件分离
- [x] 支持任命楼长/副楼长/撤职
- [x] 5 个测试剧本跑通

## 已知限制

- 当前使用简单命令格式（非自然语言），LLM 接口已预留
- 居民为按楼栋聚合，非个体模拟
- 无 2D 地图（Phase 1 实现）
- 季节/天气系统简化
- 无完整起义系统（社会指标已预留）

## 下一步

1. 接入 LLM API → 自然语言命令解析
2. 接入 LLM API → 角色发言生成
3. 升级报告系统 → AI 润色
4. 进入 Phase 1：2D 小区地图原型
