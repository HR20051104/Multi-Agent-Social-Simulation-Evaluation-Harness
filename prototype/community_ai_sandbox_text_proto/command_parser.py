"""Command Parser for Rule Mode text prototype.

Parses simple structured commands (not natural language) in Rule Mode.
Each command maps to an action that the rule engine executes.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add root to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.models import WorldState
from src.task_engine import (
    create_task, approve_task_resources, force_task, deny_task,
)
from src.event_engine import generate_events
from src.evidence_engine import (
    run_audit, plant_informant, hold_meeting, process_all_channels,
    update_player_knowledge,
)
from src.world import daily_tick


def parse_and_execute(world: WorldState, command: str) -> str:
    """Parse a command string and execute it against the world.

    Returns a result message string.
    """
    parts = command.strip().split()
    if not parts:
        return ""

    cmd = parts[0].lower()

    # ── help ──
    if cmd == "help":
        return _help_text()

    # ── status ──
    elif cmd == "status":
        return _cmd_status(world)

    # ── agents ──
    elif cmd == "agents":
        return _cmd_agents(world)

    # ── positions ──
    elif cmd == "positions":
        return _cmd_positions(world)

    # ── tasks ──
    elif cmd == "tasks":
        return _cmd_tasks(world)

    # ── knowledge ──
    elif cmd == "knowledge":
        return _cmd_knowledge(world)

    # ── events_debug ──
    elif cmd == "events_debug":
        return _cmd_events_debug(world)

    # ── next_day ──
    elif cmd == "next_day":
        return _cmd_next_day(world)

    # ── appoint ──
    elif cmd == "appoint" and len(parts) >= 3:
        return _cmd_appoint(world, parts[1], parts[2])

    # ── appoint_deputy ──
    elif cmd == "appoint_deputy" and len(parts) >= 3:
        return _cmd_appoint_deputy(world, parts[1], parts[2])

    # ── remove_position ──
    elif cmd == "remove_position" and len(parts) >= 2:
        return _cmd_remove_position(world, parts[1])

    # ── assign_task ──
    elif cmd == "assign_task" and len(parts) >= 6:
        return _cmd_assign_task(world, parts[1], parts[2], parts[3], parts[4], parts[5])

    # ── approve_task ──
    elif cmd == "approve_task" and len(parts) >= 5:
        return _cmd_approve_task(world, parts[1], parts[2], parts[3], parts[4])

    # ── deny_task ──
    elif cmd == "deny_task" and len(parts) >= 2:
        return _cmd_deny_task(world, parts[1])

    # ── force_task ──
    elif cmd == "force_task" and len(parts) >= 2:
        return _cmd_force_task(world, parts[1])

    # ── audit ──
    elif cmd == "audit" and len(parts) >= 2:
        return _cmd_audit(world, parts[1])

    # ── plant_informant ──
    elif cmd == "plant_informant" and len(parts) >= 2:
        return _cmd_plant_informant(world, parts[1])

    # ── meeting ──
    elif cmd == "meeting":
        return _cmd_meeting(world)

    # ── quit ──
    elif cmd == "quit":
        return "__QUIT__"

    else:
        return f"未知命令: {command}\n输入 'help' 查看可用命令。"


# ── Command implementations ──────────────────────────────────────────

def _help_text() -> str:
    return """
可用命令:
  help                              显示帮助
  status                            查看当前世界状态
  agents                            查看所有角色
  positions                         查看所有职位
  tasks                             查看所有任务
  knowledge                         查看玩家认知
  next_day                          推进一天
  assign_task <agent_id> <type> <budget> <materials> <labor>
                                    分配任务 (type: build_storage, build_housing, repair, patrol, etc.)
  approve_task <task_id> <budget> <materials> <labor>
                                    审批任务资源
  deny_task <task_id>               取消任务
  force_task <task_id>              强制推进任务
  appoint <agent_id> <position_id>  任命
  appoint_deputy <agent_id> <position_id>
                                    任命副职
  remove_position <position_id>     撤职
  audit <target_id>                 审计（目标可以是任务/楼栋/角色）
  plant_informant <target_id>       安排眼线
  meeting                           召开楼长会议
  events_debug                      [调试] 查看所有隐藏事件
  quit                              退出
"""


def _cmd_status(world: WorldState) -> str:
    lines = [
        f"=== Day {world.day} 状态 ===",
        f"预算: 可用 {world.budget_available} | 冻结 {world.budget_frozen} | 已支出 {world.budget_spent}",
        f"资源: 材料 {world.materials} | 人力 {world.labor}",
        f"--- 社会指标 ---",
        f"合法性: {world.legitimacy:.0f}  公共秩序: {world.public_order:.0f}",
        f"真实满意度: {world.true_satisfaction:.0f}  报告满意度: {world.reported_satisfaction:.0f}",
        f"愤怒: {world.general_anger:.0f}  恐惧: {world.general_fear:.0f}",
        f"信息失真: {world.information_distortion:.0f}  反抗压力: {world.rebellion_pressure:.0f}",
        f"治理信任: {world.trust_in_governance:.0f}",
        f"审计强度: {world.audit_strength:.0f}  监控强度: {world.surveillance_strength:.0f}  眼线网络: {world.informant_network:.0f}",
        f"---",
        f"活跃任务: {len([t for t in world.tasks.values() if t.status not in ('completed','failed','abandoned','cancelled')])}",
        f"隐藏事件: {len(world.events)}  已知线索: {len(world.clues)}",
    ]
    return "\n".join(lines)


def _cmd_agents(world: WorldState) -> str:
    lines = ["=== 角色 ==="]
    for agent in world.agents.values():
        pos_name = ""
        if agent.position_id and agent.position_id in world.positions:
            pos_name = world.positions[agent.position_id].title
        lines.append(
            f"  {agent.id}: {agent.name} ({agent.role}) [{pos_name}] "
            f"忠{agent.loyalty:.0f} 诚{agent.honesty:.0f} 压{agent.stress:.0f} "
            f"能{agent.competence:.0f} 贪{agent.greed:.0f} 惧{agent.fear:.0f} "
            f"健{agent.health:.0f} {'[OK]' if agent.available else '[X]'}"
        )
    return "\n".join(lines)


def _cmd_positions(world: WorldState) -> str:
    lines = ["=== 职位 ==="]
    for pos in world.positions.values():
        holder_name = ""
        if pos.holder_id and pos.holder_id in world.agents:
            holder_name = world.agents[pos.holder_id].name
        deputies = ", ".join(pos.deputy_ids) if pos.deputy_ids else "无"
        lines.append(
            f"  {pos.id}: {pos.title} | 任职: {holder_name} | "
            f"副职: {deputies} | 权限: {pos.authority_level:.0f} | "
            f"管辖: {pos.scope}"
        )
    return "\n".join(lines)


def _cmd_tasks(world: WorldState) -> str:
    if not world.tasks:
        return "当前没有任务。"

    lines = ["=== 任务 ==="]
    for task in world.tasks.values():
        assignee_name = world.agents[task.assignee_id].name if task.assignee_id in world.agents else "?"
        lines.append(
            f"  {task.id}: {task.title} [{task.status}] "
            f"负责人: {assignee_name} "
            f"进度: {task.progress:.0f}% "
            f"预算: {task.reserved_budget}/{task.required_budget} "
            f"材料: {task.reserved_materials}/{task.required_materials} "
            f"人力: {task.reserved_labor}/{task.required_labor}"
        )
        if task.blockers:
            lines.append(f"    阻塞原因: {', '.join(task.blockers)}")
        if task.risk_flags:
            lines.append(f"    风险标记: {', '.join(task.risk_flags)}")
    return "\n".join(lines)


def _cmd_knowledge(world: WorldState) -> str:
    if not world.player_knowledge:
        return "暂无特别认知。"

    lines = ["=== 玩家认知 ==="]
    for pk in world.player_knowledge:
        lines.append(f"  [{pk.status}] {pk.topic}: {pk.summary}")
    if world.clues:
        lines.append("--- 已发现线索 ---")
        for clue in world.clues[-5:]:  # last 5
            lines.append(f"  [{clue.source}] 置信度{clue.confidence:.0f}%: {clue.content}")
    return "\n".join(lines)


def _cmd_events_debug(world: WorldState) -> str:
    if not world.events:
        return "[DEBUG] 没有隐藏事件。"

    lines = ["=== [DEBUG] 所有隐藏事件 ==="]
    for ev in world.events:
        discovered = "[D]" if ev.discovered else "[?]"
        lines.append(
            f"  Day{ev.day} [{ev.type}] [{discovered}] {ev.content_true}"
        )
        if ev.causes:
            lines.append(f"    原因: {', '.join(ev.causes)}")
    return "\n".join(lines)


def _cmd_next_day(world: WorldState) -> str:
    prev_day = world.day
    summary = daily_tick(world)
    lines = [
        f"=== 第 {prev_day} 天 → 第 {world.day} 天 ===",
        f"预算: {summary['budget_available']} | 材料: {summary['materials']} | 人力: {summary['labor']}",
        f"报告满意度: {summary['reported_satisfaction']:.0f} | 公共秩序: {summary['public_order']:.0f}",
        f"新隐藏事件: {summary['new_events']} | 新线索: {summary['new_clues']}",
    ]
    if summary['tick_log']:
        lines.append("--- 日志 ---")
        for msg in summary['tick_log'][:10]:
            lines.append(f"  {msg}")
    return "\n".join(lines)


def _cmd_appoint(world: WorldState, agent_id: str, position_id: str) -> str:
    if agent_id not in world.agents:
        return f"角色 {agent_id} 不存在。"
    if position_id not in world.positions:
        return f"职位 {position_id} 不存在。"

    pos = world.positions[position_id]
    old_holder = pos.holder_id

    pos.holder_id = agent_id
    world.agents[agent_id].position_id = position_id
    pos.appointment_day = world.day

    msg = f"任命 {world.agents[agent_id].name} 为 {pos.title}。"
    if old_holder and old_holder in world.agents:
        world.agents[old_holder].position_id = None
        world.agents[old_holder].loyalty = clamp_import(world.agents[old_holder].loyalty - 10.0)
        world.agents[old_holder].resentment = clamp_import(world.agents[old_holder].resentment + 15.0)
        msg += f"（原任职者 {world.agents[old_holder].name} 已被撤换）"

    world.add_history(f"Day {world.day}: Appointed {agent_id} as {position_id}.")
    return msg


def _cmd_appoint_deputy(world: WorldState, agent_id: str, position_id: str) -> str:
    if agent_id not in world.agents:
        return f"角色 {agent_id} 不存在。"
    if position_id not in world.positions:
        return f"职位 {position_id} 不存在。"

    pos = world.positions[position_id]
    if agent_id not in pos.deputy_ids:
        pos.deputy_ids.append(agent_id)

    # The deputy also gets a position-like association
    # Create a deputy position if it doesn't exist
    deputy_pos_id = f"deputy_{position_id}"
    if deputy_pos_id not in world.positions:
        from src.models import Position
        deputy_pos = Position(
            id=deputy_pos_id,
            title=f"{pos.title}副职",
            scope=pos.scope,
            holder_id=agent_id,
            permissions=["assist_leader", "collect_feedback", "supervise_small_tasks"],
            authority_level=pos.authority_level * 0.6,
            appointed_by="player",
            appointment_day=world.day,
        )
        world.positions[deputy_pos_id] = deputy_pos
        world.agents[agent_id].position_id = deputy_pos_id

    # Effects on original leader
    if pos.holder_id and pos.holder_id in world.agents:
        leader = world.agents[pos.holder_id]
        leader.trust_in_player = clamp_import(leader.trust_in_player - 5.0)
        leader.resentment = clamp_import(leader.resentment + 8.0)

    world.add_history(f"Day {world.day}: Appointed {agent_id} as deputy of {position_id}.")
    return f"任命 {world.agents[agent_id].name} 为 {pos.title}的副职。注意：原楼长可能会感到被削权。"


def _cmd_remove_position(world: WorldState, position_id: str) -> str:
    if position_id not in world.positions:
        return f"职位 {position_id} 不存在。"

    pos = world.positions[position_id]
    pos.is_active = False

    if pos.holder_id and pos.holder_id in world.agents:
        world.agents[pos.holder_id].position_id = None
        world.agents[pos.holder_id].loyalty = clamp_import(world.agents[pos.holder_id].loyalty - 20.0)
        world.agents[pos.holder_id].resentment = clamp_import(world.agents[pos.holder_id].resentment + 25.0)

    world.add_history(f"Day {world.day}: Position {position_id} removed.")
    return f"已撤销 {pos.title} 职位。"


def _cmd_assign_task(world: WorldState, agent_id: str, task_type: str,
                     budget: str, materials: str, labor: str) -> str:
    if agent_id not in world.agents:
        return f"角色 {agent_id} 不存在。"

    try:
        b = int(budget)
        m = int(materials)
        l = int(labor)
    except ValueError:
        return "参数必须是数字。"

    type_names = {
        "build_storage": "修建临时仓库",
        "build_housing": "修建临时住房",
        "build_facility": "修建公共设施",
        "repair": "修缮设施",
        "patrol": "组织巡逻",
        "investigate": "调查任务",
        "clean": "清洁任务",
        "distribute_supplies": "分配物资",
        "organize_residents": "组织居民",
        "other": "其他任务",
    }
    title = type_names.get(task_type, task_type)

    task = create_task(
        world,
        title=title,
        task_type=task_type,
        assignee_id=agent_id,
        required_budget=b,
        required_materials=m,
        required_labor=l,
    )

    # If no resources requested, task can start immediately
    if b == 0 and m == 0 and l == 0:
        task.status = "approved"
        task.blockers = []

    return f"任务 {task.id} 已创建: {title}，分配给 {world.agents[agent_id].name}。需要 预算:{b} 材料:{m} 人力:{l}。"


def _cmd_approve_task(world: WorldState, task_id: str, budget: str, materials: str, labor: str) -> str:
    try:
        b = int(budget)
        m = int(materials)
        l = int(labor)
    except ValueError:
        return "参数必须是数字。"

    success, msg = approve_task_resources(world, task_id, b, m, l)
    return msg


def _cmd_deny_task(world: WorldState, task_id: str) -> str:
    success, msg = deny_task(world, task_id)
    return msg


def _cmd_force_task(world: WorldState, task_id: str) -> str:
    success, msg = force_task(world, task_id)
    return msg


def _cmd_audit(world: WorldState, target_id: str) -> str:
    clues = run_audit(world, target_id)
    if not clues:
        return f"审计 {target_id} 未发现明显异常。（消耗100预算）"
    lines = [f"=== 审计 {target_id} 结果 ==="]
    for clue in clues:
        lines.append(f"  [{clue.source}] 置信度{clue.confidence:.0f}%: {clue.content}")
    return "\n".join(lines)


def _cmd_plant_informant(world: WorldState, target_id: str) -> str:
    success, msg = plant_informant(world, target_id)
    return msg


def _cmd_meeting(world: WorldState) -> str:
    statements = hold_meeting(world)
    return "\n".join(statements)


# ── Utility ──────────────────────────────────────────────────────────

def clamp_import(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, float(value)))
