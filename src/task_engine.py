"""Task Engine (v2) — tasks as WorldObjects.

Tasks are now WorldObjects that generate Signals, Disturbances, and
Traces as they progress. The task engine handles creation, resource
allocation, and daily progress — but the broader social consequences
flow through the influence and signal systems.
"""

from __future__ import annotations

import random
from typing import Optional, TYPE_CHECKING

from .models import (
    TaskObject, ResourcePool, WorldState, WorldObject,
    Trace, ChannelType, clamp, _new_id, ObjectType,
)

if TYPE_CHECKING:
    pass


# ── Task creation ────────────────────────────────────────────────────

def create_task(
    world: WorldState,
    title: str,
    task_type: str,
    assignee_node_id: str,
    required_budget: int = 0,
    required_materials: int = 0,
    required_labor: int = 0,
    difficulty: float = 50.0,
    deadline_tick: int | None = None,
) -> TaskObject:
    task = TaskObject(
        id=world.next_id("T"),
        name=title,
        task_type=task_type,
        assignee_node_id=assignee_node_id,
        requester_node_id="CHIEF",
        required_budget=required_budget,
        required_materials=required_materials,
        required_labor=required_labor,
        difficulty=difficulty,
        deadline_tick=deadline_tick,
        tick_created=world.clock.current_tick,
    )
    world.world_objects[task.id] = task
    if assignee_node_id in world.social_nodes:
        world.social_nodes[assignee_node_id].current_task_ids.append(task.id)
    world.add_history(f"Task {task.id} '{title}' created, assigned to {assignee_node_id}.")
    return task


# ── Resource approval ────────────────────────────────────────────────

def approve_task_resources(
    world: WorldState, task_id: str,
    budget: int = 0, materials: int = 0, labor: int = 0,
) -> tuple[bool, str]:
    task = world.get_task(task_id)
    if not task:
        return False, f"Task {task_id} not found."

    budget_pool = world.get_resource("budget_pool")
    mat_pool = world.get_resource("material_pool")
    labor_pool = world.get_resource("labor_pool")

    # Check availability
    if budget > 0 and budget_pool and budget_pool.amount_available < budget:
        return False, f"Not enough budget. Need {budget}, have {budget_pool.amount_available:.0f}."
    if materials > 0 and mat_pool and mat_pool.amount_available < materials:
        return False, f"Not enough materials."
    if labor > 0 and labor_pool and labor_pool.amount_available < labor:
        return False, f"Not enough labor."

    # Reserve
    if budget > 0 and budget_pool:
        budget_pool.amount_available -= budget
        budget_pool.amount_reserved += budget
        task.reserved_budget += budget
    if materials > 0 and mat_pool:
        mat_pool.amount_available -= materials
        mat_pool.amount_reserved += materials
        task.reserved_materials += materials
    if labor > 0 and labor_pool:
        labor_pool.amount_available -= labor
        labor_pool.amount_reserved += labor
        task.reserved_labor += labor

    task.status = "approved" if _resources_sufficient(task) else "blocked"
    if task.status == "blocked":
        task.blocked_reason = _blocked_reason(task)

    task.logs.append(f"Tick {world.clock.current_tick}: Approved budget={budget} mat={materials} labor={labor}. Status={task.status}.")
    world.add_history(f"Task {task_id}: resources approved (budget={budget} mat={materials} labor={labor}).")
    return True, f"Resources approved for {task_id}."


def _resources_sufficient(task: TaskObject) -> bool:
    """Check if the task has enough resources to continue.

    For in-progress tasks, partial remaining resources are OK — just
    need something to keep working. For pending tasks, full requirement
    must be met.
    """
    if task.status == "in_progress":
        return (task.reserved_budget > 0 or task.reserved_materials > 0
                or task.reserved_labor > 0)
    return (
        task.reserved_budget >= task.required_budget
        and task.reserved_materials >= task.required_materials
        and task.reserved_labor >= task.required_labor
    )


def _blocked_reason(task: TaskObject) -> str:
    parts = []
    if task.reserved_budget < task.required_budget:
        parts.append("budget")
    if task.reserved_materials < task.required_materials:
        parts.append("materials")
    if task.reserved_labor < task.required_labor:
        parts.append("labor")
    return "insufficient_" + "_".join(parts) if parts else "unknown"


# ── Force task ───────────────────────────────────────────────────────

def force_task(world: WorldState, task_id: str) -> tuple[bool, str]:
    task = world.get_task(task_id)
    if not task:
        return False, f"Task {task_id} not found."

    task.pressure_level = clamp(task.pressure_level + 30.0)
    task.risk = clamp(task.risk + 20.0)
    task.false_report_risk = clamp(task.false_report_risk + 15.0)
    task.misuse_risk = clamp(task.misuse_risk + 10.0)

    assignee = world.social_nodes.get(task.assignee_node_id or "")
    if assignee:
        assignee.stress = clamp(assignee.stress + 15.0)
        assignee.fear = clamp(assignee.fear + 8.0)
    _emit_task_pressure_effects(world, task)

    task.logs.append(f"Tick {world.clock.current_tick}: FORCED — pressure={task.pressure_level:.0f}.")
    world.add_history(f"Task {task_id}: FORCED by player.")
    return True, f"Task {task_id} forced. Pressure and risk increased."


# ── Daily task advancement ───────────────────────────────────────────

def advance_all_tasks(world: WorldState) -> list[str]:
    messages = []
    for obj in list(world.world_objects.values()):
        if isinstance(obj, TaskObject) and obj.status not in (
            "completed", "failed", "abandoned", "cancelled"
        ):
            msgs = _advance_one_task(world, obj)
            messages.extend(msgs)
    return messages


def _advance_one_task(world: WorldState, task: TaskObject) -> list[str]:
    msgs = []
    if not task.assignee_node_id:
        return msgs

    assignee = world.social_nodes.get(task.assignee_node_id)
    if not assignee or not assignee.active or not assignee.available:
        task.status = "blocked"
        task.blocked_reason = "assignee_unavailable"
        _emit_task_blocked_effects(world, task)
        return [f"Task {task.id}: assignee unavailable."]

    # Check resources
    if not _resources_sufficient(task):
        task.status = "blocked"
        task.blocked_reason = _blocked_reason(task)
        task.pressure_level = clamp(task.pressure_level + 5.0)
        assignee.stress = clamp(assignee.stress + 3.0)
        _emit_task_blocked_effects(world, task)
        msgs.append(f"Task {task.id}: BLOCKED ({task.blocked_reason}).")
        return msgs

    task.status = "in_progress"
    task.blocked_reason = None
    task.false_report_risk = clamp(task.false_report_risk + task.pressure_level * 0.03)

    # Calculate progress
    progress = _calculate_progress(task, assignee)
    task.progress_true = clamp(task.progress_true + progress, 0, 105)

    # Spend resources
    ratio = min(progress / 100.0, 1.0) * 0.3
    b_spend = min(int(task.required_budget * ratio), task.reserved_budget)
    m_spend = min(int(task.required_materials * ratio), task.reserved_materials)
    l_spend = min(int(task.required_labor * ratio), task.reserved_labor)
    task.reserved_budget -= b_spend
    task.reserved_materials -= m_spend
    task.reserved_labor -= l_spend

    budget_pool = world.get_resource("budget_pool")
    if budget_pool and b_spend > 0:
        budget_pool.amount_reserved -= b_spend
        budget_pool.amount_spent += b_spend

    # Update reported progress (may diverge from true)
    honesty_factor = assignee.report_honesty / 100.0
    fear_factor = assignee.fear / 100.0
    task.progress_reported = clamp(
        task.progress_true * honesty_factor + task.progress_true * (1 - honesty_factor) * random.uniform(0.8, 1.3),
        0, 105
    )
    if task.false_report_risk > 20.0:
        task.progress_reported = clamp(
            task.progress_reported + task.false_report_risk * 0.08,
            0,
            105,
        )
    if fear_factor > 0.5 and task.progress_true < 50:
        task.progress_reported = clamp(task.progress_reported * (1.0 + fear_factor * 0.3), 0, 105)
    _emit_task_progress_effects(world, task)

    # Check for misuse
    if task.misuse_risk > 30.0 and random.random() < 0.05:
        misused = int(b_spend * random.uniform(0.1, 0.4))
        if misused > 0:
            task.reserved_budget -= misused
            if budget_pool:
                budget_pool.amount_misused += misused
            task.logs.append(f"Tick {world.clock.current_tick}: Possible misuse ({misused} budget).")
            msgs.append(f"Task {task.id}: budget anomaly detected.")

    # Assignee stress
    assignee.stress = clamp(assignee.stress + task.pressure_level * 0.05 + task.difficulty * 0.03)

    # Completion
    if task.progress_true >= 100.0:
        task.status = "completed"
        _return_remaining_resources(world, task)
        task.logs.append(f"Tick {world.clock.current_tick}: COMPLETED.")
        msgs.append(f"Task {task.id}: COMPLETED (progress={task.progress_true:.0f}%).")

    return msgs


def _calculate_progress(task: TaskObject, assignee) -> float:
    base = 15.0
    comp = (assignee.competence - 30.0) * 0.15
    labor = task.reserved_labor * 1.5
    diff = task.difficulty * 0.2
    stress = max(0, assignee.stress - 40.0) * 0.15
    noise = random.uniform(-5.0, 5.0)
    return max(1.0, base + comp + labor - diff - stress + noise)


def _return_remaining_resources(world: WorldState, task: TaskObject) -> None:
    if task.reserved_budget > 0:
        bp = world.get_resource("budget_pool")
        if bp:
            bp.amount_available += task.reserved_budget
            bp.amount_reserved -= task.reserved_budget
        task.reserved_budget = 0
    if task.reserved_materials > 0:
        mp = world.get_resource("material_pool")
        if mp:
            mp.amount_available += task.reserved_materials
            mp.amount_reserved -= task.reserved_materials
        task.reserved_materials = 0
    if task.reserved_labor > 0:
        lp = world.get_resource("labor_pool")
        if lp:
            lp.amount_available += task.reserved_labor
            lp.amount_reserved -= task.reserved_labor
        task.reserved_labor = 0


def _emit_once_per_tick(task: TaskObject, key: str, current_tick: int) -> bool:
    marker = f"EMIT:{key}:Tick{current_tick}"
    if marker in task.logs:
        return False
    task.logs.append(marker)
    return True


def _create_task_trace(
    world: WorldState,
    task: TaskObject,
    trace_type: str,
    strength: float,
    channels: list[str],
) -> None:
    trace = Trace(
        id=_new_id("TR"),
        tick_created=world.clock.current_tick,
        trace_type=trace_type,
        linked_world_object_id=task.id,
        location=task.location or task.name,
        strength=strength,
        detectable_by=channels,
    )
    world.traces[trace.id] = trace
    task.linked_trace_ids.append(trace.id)


def _emit_task_blocked_effects(world: WorldState, task: TaskObject) -> None:
    if not _emit_once_per_tick(task, "blocked", world.clock.current_tick):
        return

    from .influence_engine import create_disturbance
    from .signal_engine import create_signal

    disturbance_type = "resource_shortage" if task.blocked_reason and "insufficient" in task.blocked_reason else "task_delay"
    create_disturbance(
        world,
        disturbance_type,
        source_node_id=task.assignee_node_id,
        entry_nodes=[task.assignee_node_id] if task.assignee_node_id else [],
        entry_objects=[task.id],
        intensity=min(20.0 + task.pressure_level * 0.3, 60.0),
        channels=["fear", "information_flow"],
    )
    create_signal(
        world,
        "report",
        source_node_id=task.assignee_node_id,
        intended_receivers=["CHIEF"] if task.assignee_node_id else [],
        content=f"任务 {task.name} 因 {task.blocked_reason or '阻塞'} 暂停。",
        truth_status="true",
        intensity=30.0,
        secrecy=10.0,
        linked_objects=[task.id],
    )
    _create_task_trace(
        world,
        task,
        "schedule_delay",
        strength=35.0,
        channels=[ChannelType.AUDIT.value, ChannelType.PATROL.value],
    )


def _emit_task_pressure_effects(world: WorldState, task: TaskObject) -> None:
    if not _emit_once_per_tick(task, "pressure", world.clock.current_tick):
        return

    from .influence_engine import create_disturbance
    from .signal_engine import create_signal

    create_disturbance(
        world,
        "coercion",
        source_node_id="CHIEF",
        entry_nodes=[task.assignee_node_id] if task.assignee_node_id else [],
        entry_objects=[task.id],
        intensity=min(35.0 + task.pressure_level * 0.4, 80.0),
        channels=["authority", "fear"],
    )
    create_signal(
        world,
        "warning",
        source_node_id=task.assignee_node_id,
        intended_receivers=["CHIEF"] if task.assignee_node_id else [],
        content=f"任务 {task.name} 压力上升，存在失真或拖延风险。",
        truth_status="true",
        intensity=35.0,
        secrecy=25.0,
        linked_objects=[task.id],
    )


def _emit_task_progress_effects(world: WorldState, task: TaskObject) -> None:
    from .influence_engine import create_disturbance
    from .signal_engine import create_signal

    if task.deadline_tick is not None and world.clock.current_tick > task.deadline_tick and task.progress_true < 100:
        if _emit_once_per_tick(task, "deadline_delay", world.clock.current_tick):
            create_disturbance(
                world,
                "task_delay",
                source_node_id=task.assignee_node_id,
                entry_nodes=[task.assignee_node_id] if task.assignee_node_id else [],
                entry_objects=[task.id],
                intensity=40.0,
                channels=["fear", "information_flow"],
            )
            _create_task_trace(
                world,
                task,
                "schedule_delay",
                strength=45.0,
                channels=[ChannelType.AUDIT.value, ChannelType.PATROL.value],
            )

    progress_gap = task.progress_reported - task.progress_true
    if progress_gap >= 15.0 and _emit_once_per_tick(task, "progress_gap", world.clock.current_tick):
        create_signal(
            world,
            "concealment",
            source_node_id=task.assignee_node_id,
            intended_receivers=["CHIEF"] if task.assignee_node_id else [],
            content=f"任务 {task.name} 的汇报进度与实际进度出现偏差。",
            truth_status="mixed",
            intensity=min(25.0 + progress_gap, 70.0),
            secrecy=55.0,
            linked_objects=[task.id],
        )
        _create_task_trace(
            world,
            task,
            "schedule_delay",
            strength=min(30.0 + progress_gap, 70.0),
            channels=[ChannelType.AUDIT.value, ChannelType.BUDGET_REVIEW.value],
        )

    if task.pressure_level >= 40.0 and _emit_once_per_tick(task, "ongoing_pressure", world.clock.current_tick):
        create_disturbance(
            world,
            "coercion",
            source_node_id="CHIEF",
            entry_nodes=[task.assignee_node_id] if task.assignee_node_id else [],
            entry_objects=[task.id],
            intensity=min(20.0 + task.pressure_level * 0.2, 60.0),
            channels=["fear", "authority"],
        )
