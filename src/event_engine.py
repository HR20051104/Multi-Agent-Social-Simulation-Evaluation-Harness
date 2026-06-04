"""Event Engine (v2).

Autonomous events emerge from tasks, signals, and social conditions.
"""

from __future__ import annotations

import random

from .models import (
    ChannelType,
    Disturbance,
    DisturbanceType,
    Memory,
    SignalType,
    Trace,
    TruthStatus,
    WorldState,
    _new_id,
    clamp,
)


def scan_and_generate(world: WorldState) -> dict:
    counts = {"signals": 0, "traces": 0, "disturbances": 0}

    s, t, d = _scan_promises(world)
    counts["signals"] += s
    counts["traces"] += t
    counts["disturbances"] += d

    for obj in list(world.world_objects.values()):
        if hasattr(obj, "task_type") and obj.status in ("in_progress", "blocked", "approved"):
            s, t, d = _scan_task(world, obj)
            counts["signals"] += s
            counts["traces"] += t
            counts["disturbances"] += d

    for node in list(world.social_nodes.values()):
        if node.active:
            s, t, d = _scan_node(world, node)
            counts["signals"] += s
            counts["traces"] += t
            counts["disturbances"] += d

    s, t, d = _scan_positions(world)
    counts["signals"] += s
    counts["traces"] += t
    counts["disturbances"] += d

    s, t, d = _scan_conspiracies(world)
    counts["signals"] += s
    counts["traces"] += t
    counts["disturbances"] += d
    return counts


def _scan_promises(world: WorldState) -> tuple[int, int, int]:
    signal_count = trace_count = disturbance_count = 0
    for signal in list(world.signals.values()):
        if signal.signal_type != SignalType.PROMISE.value:
            continue
        if signal.promise_status in {"fulfilled", "broken"}:
            continue

        progress = _promise_fulfillment_progress(world, signal)
        signal.fulfillment_progress = progress
        if progress >= 1.0:
            signal.promise_status = "fulfilled"
            signal.fulfilled = True
            _deposit_promise_memory(world, signal.intended_receiver_ids, signal.id, "promise_fulfilled", 0.45, signal)
            _adjust_chief_trust(world, signal.intended_receiver_ids, signal, -4.0)
            continue

        if signal.deadline_tick is None or world.clock.current_tick <= signal.deadline_tick:
            if progress > 0:
                signal.promise_status = "partial"
            continue

        affected_nodes = [
            node_id
            for node_id in dict.fromkeys(signal.intended_receiver_ids + signal.current_holder_ids)
            if node_id and node_id != "CHIEF" and node_id in world.social_nodes
        ] or ["A2"]

        if progress >= 0.4:
            disappointment = _create_promise_outcome(
                world,
                signal,
                affected_nodes,
                SignalType.DISAPPOINTMENT.value,
                min(55.0, signal.intensity * 0.6),
                "partial",
            )
            signal_count += 1
            _deposit_promise_memory(world, affected_nodes, disappointment.id, disappointment.signal_type, -0.35, signal)
            _adjust_chief_trust(world, affected_nodes, signal, 3.0)
            signal.promise_status = "delayed"
            signal.fulfilled = True
            signal.active = False
            continue

        broken = _create_promise_outcome(
            world,
            signal,
            affected_nodes,
            SignalType.BROKEN_EXPECTATION.value,
            min(90.0, signal.intensity * 0.9),
            "broken",
        )
        signal_count += 1
        _deposit_promise_memory(world, affected_nodes, broken.id, broken.signal_type, -0.7, signal)
        _adjust_chief_trust(world, affected_nodes, signal, max(6.0, signal.intensity * 0.08))
        disturbance_id = _new_id("D")
        world.disturbances[disturbance_id] = Disturbance(
            id=disturbance_id,
            tick_created=world.clock.current_tick,
            disturbance_type=DisturbanceType.BROKEN_PROMISE.value,
            source_node_id="CHIEF",
            entry_social_node_ids=affected_nodes,
            entry_signal_ids=[signal.id, broken.id],
            intensity=min(signal.intensity * 0.8, 80.0),
            duration_ticks=3,
            propagation_channels=["trust", "information_flow", "fear"],
            active=True,
        )
        disturbance_count += 1
        signal.promise_status = "broken"
        signal.fulfilled = True
        signal.active = False

    return signal_count, trace_count, disturbance_count


def _promise_fulfillment_progress(world: WorldState, signal) -> float:
    if signal.linked_fulfillment_targets:
        matched = sum(1 for target in signal.linked_fulfillment_targets if _target_is_fulfilled(world, target))
        if signal.linked_fulfillment_targets:
            return matched / len(signal.linked_fulfillment_targets)

    conditions = signal.fulfillment_conditions or []
    if conditions:
        matched = sum(1 for condition in conditions if _condition_is_fulfilled(world, condition))
        return matched / len(conditions)

    if signal.linked_world_object_ids:
        matched = sum(1 for target in signal.linked_world_object_ids if _target_is_fulfilled(world, target))
        if signal.linked_world_object_ids:
            return matched / len(signal.linked_world_object_ids)

    topic = (signal.promise_topic or "").strip().lower()
    if not topic:
        return 0.0

    for obj in world.world_objects.values():
        name = getattr(obj, "name", "").lower()
        task_type = getattr(obj, "task_type", "").lower()
        if topic in name or topic == task_type:
            status = getattr(obj, "status", "")
            if status == "completed":
                return 1.0
            if status in {"approved", "in_progress"}:
                return 0.5
    return 0.0


def _target_is_fulfilled(world: WorldState, target_id: str) -> bool:
    obj = world.world_objects.get(target_id)
    if obj is not None:
        return getattr(obj, "status", "") == "completed"
    signal = world.signals.get(target_id)
    if signal is not None:
        return signal.signal_type in {"report", "appointment", "coordination"} and signal.active
    return False


def _condition_is_fulfilled(world: WorldState, condition: str) -> bool:
    if condition.startswith("task_completed:"):
        return _target_is_fulfilled(world, condition.split(":", 1)[1])
    if condition.startswith("object_completed:"):
        return _target_is_fulfilled(world, condition.split(":", 1)[1])
    if condition.startswith("signal_exists:"):
        signal_type = condition.split(":", 1)[1]
        return any(signal.signal_type == signal_type for signal in world.signals.values())
    return False


def _create_promise_outcome(world: WorldState, signal, affected_nodes: list[str], signal_type: str, intensity: float, status: str):
    from .signal_engine import create_signal

    outcome = create_signal(
        world,
        signal_type,
        source_node_id="CHIEF",
        intended_receivers=affected_nodes,
        content=f"{signal_type.replace('_', ' ')}: {signal.promise_topic or signal.content_summary}",
        truth_status=TruthStatus.TRUE.value,
        intensity=intensity,
        secrecy=10.0,
        spread=min(signal.spread_rate + 10.0, 90.0),
        decay=signal.decay_rate,
        memory_strength=min(signal.memory_strength + 10.0, 95.0),
        related_signal_id=signal.id,
        promise_status=status,
        tags=["promise_outcome"],
    )
    outcome.current_holder_ids = ["CHIEF", *affected_nodes]
    return outcome


def _deposit_promise_memory(world: WorldState, affected_nodes: list[str], source_signal_id: str, topic: str, sentiment: float, signal) -> None:
    for node_id in affected_nodes:
        memory = Memory(
            id=_new_id("M"),
            holder_node_id=node_id,
            source_signal_id=source_signal_id,
            topic=topic,
            sentiment=sentiment,
            strength=min(signal.memory_strength + 15.0, 95.0),
            created_tick=world.clock.current_tick,
            last_reinforced_tick=world.clock.current_tick,
        )
        world.memories[memory.id] = memory
        if node_id in world.social_nodes:
            world.social_nodes[node_id].memory_ids.append(memory.id)


def _adjust_chief_trust(world: WorldState, affected_nodes: list[str], signal, trust_drop: float) -> None:
    for node_id in affected_nodes:
        edge = world.social_edges.get(f"{node_id}->CHIEF")
        if edge:
            edge.trust = clamp(edge.trust - trust_drop)
            if trust_drop > 0:
                edge.fear = clamp(edge.fear + 2.0)
            elif trust_drop < 0:
                edge.fear = clamp(edge.fear - 1.0)


def _scan_positions(world: WorldState) -> tuple[int, int, int]:
    for obj in world.world_objects.values():
        if not hasattr(obj, "holder_node_id") or not obj.holder_node_id:
            continue
        holder_id = obj.holder_node_id
        chief_edge = world.get_edge("CHIEF", holder_id)
        back_edge = world.get_edge(holder_id, "CHIEF")
        managed_resources = sum(
            1 for resource in world.world_objects.values()
            if getattr(resource, "manager_node_id", None) == holder_id
        )
        known_signals = len(world.social_nodes.get(holder_id).known_signal_ids) if holder_id in world.social_nodes else 0

        if managed_resources > 0 or known_signals > 0:
            if chief_edge:
                chief_edge.information_flow = clamp(chief_edge.information_flow + 1.0)
            if back_edge:
                back_edge.information_flow = clamp(back_edge.information_flow + 1.0)
            if obj.id == "position_supply_coordinator":
                a4_edge = world.get_edge("A4", holder_id)
                if a4_edge:
                    a4_edge.competition = clamp(a4_edge.competition + 1.0)
                    a4_edge.dependency = clamp(a4_edge.dependency + 1.5)
                    a4_edge.information_flow = clamp(a4_edge.information_flow + 1.0)
        else:
            if chief_edge:
                chief_edge.authority = clamp(chief_edge.authority - 2.0)
                chief_edge.information_flow = clamp(chief_edge.information_flow - 1.5)
            if back_edge:
                back_edge.information_flow = clamp(back_edge.information_flow - 1.0)
    return 0, 0, 0


def _scan_task(world: WorldState, task) -> tuple[int, int, int]:
    signal_count = trace_count = disturbance_count = 0
    assignee = world.social_nodes.get(task.assignee_node_id or "")

    if (
        task.progress_true < 40.0
        and task.pressure_level > 40.0
        and assignee
        and assignee.report_honesty < 55.0
        and random.random() < 0.12
    ):
        from .signal_engine import create_signal

        create_signal(
            world,
            SignalType.CONCEALMENT.value,
            source_node_id=assignee.id,
            intended_receivers=["CHIEF"],
            content=f"{assignee.name} may be concealing delay on {task.name}",
            truth_status=TruthStatus.FALSE.value,
            intensity=40.0,
            secrecy=60.0,
            linked_objects=[task.id],
        )
        trace_id = _new_id("TR")
        world.traces[trace_id] = Trace(
            id=trace_id,
            tick_created=world.clock.current_tick,
            trace_type="schedule_delay",
            linked_world_object_id=task.id,
            strength=35.0,
            detectable_by=[ChannelType.AUDIT.value, ChannelType.PATROL.value],
        )
        signal_count += 1
        trace_count += 1

    if (
        task.reserved_budget > 300
        and assignee
        and assignee.greed_trait > 30.0
        and assignee.report_honesty < 55.0
        and world.clock.current_tick % 3 == 0
        and random.random() < 0.08
    ):
        from .signal_engine import create_signal

        create_signal(
            world,
            SignalType.CONCEALMENT.value,
            source_node_id=assignee.id,
            content=f"{assignee.name} may be diverting resources from {task.name}",
            truth_status=TruthStatus.MIXED.value,
            intensity=35.0,
            secrecy=70.0,
            linked_objects=[task.id],
        )
        trace_id = _new_id("TR")
        world.traces[trace_id] = Trace(
            id=trace_id,
            tick_created=world.clock.current_tick,
            trace_type="accounting_irregularity",
            linked_world_object_id=task.id,
            strength=30.0,
            detectable_by=[ChannelType.AUDIT.value, ChannelType.BUDGET_REVIEW.value],
        )
        signal_count += 1
        trace_count += 1

    return signal_count, trace_count, disturbance_count


def _scan_node(world: WorldState, node) -> tuple[int, int, int]:
    signal_count = trace_count = disturbance_count = 0
    from .signal_engine import create_signal

    if node.stress > 50.0 and node.resentment > 30.0 and random.random() < 0.10:
        create_signal(
            world,
            SignalType.COMPLAINT.value,
            source_node_id=node.id,
            content=f"{node.name} is privately complaining.",
            truth_status=TruthStatus.TRUE.value,
            intensity=25.0,
            secrecy=60.0,
            spread=30.0,
        )
        signal_count += 1

    if node.stress > 80.0 and random.random() < 0.05:
        create_signal(
            world,
            SignalType.WARNING.value,
            source_node_id=node.id,
            content=f"{node.name} is nearing a breakdown.",
            truth_status=TruthStatus.TRUE.value,
            intensity=55.0,
            secrecy=30.0,
        )
        node.health = clamp(node.health - 10.0)
        node.morale = clamp(node.morale - 15.0)
        signal_count += 1

    return signal_count, trace_count, disturbance_count


def _scan_conspiracies(world: WorldState) -> tuple[int, int, int]:
    signal_count = trace_count = disturbance_count = 0
    disloyal = []
    for node in world.social_nodes.values():
        if node.node_type == "chief" or not node.active:
            continue
        edge = world.social_edges.get(f"{node.id}->CHIEF")
        if edge and edge.trust < 35.0:
            disloyal.append(node)

    if len(disloyal) >= 2 and random.random() < 0.03:
        node_ids = [node.id for node in disloyal[:3]]
        from .signal_engine import create_signal

        create_signal(
            world,
            SignalType.CONSPIRACY.value,
            source_node_id=node_ids[0],
            intended_receivers=node_ids[1:],
            content="Private anti-chief coordination is forming.",
            truth_status=TruthStatus.TRUE.value,
            intensity=30.0,
            secrecy=80.0,
            spread=10.0,
        )
        signal_count += 1

        for index, a_id in enumerate(node_ids):
            for b_id in node_ids[index + 1:]:
                edge_ab = world.social_edges.get(f"{a_id}->{b_id}")
                if edge_ab:
                    edge_ab.secrecy = clamp(edge_ab.secrecy + 10.0)
                    edge_ab.information_flow = clamp(edge_ab.information_flow + 8.0)
                edge_ba = world.social_edges.get(f"{b_id}->{a_id}")
                if edge_ba:
                    edge_ba.secrecy = clamp(edge_ba.secrecy + 10.0)
                    edge_ba.information_flow = clamp(edge_ba.information_flow + 8.0)

    return signal_count, trace_count, disturbance_count
