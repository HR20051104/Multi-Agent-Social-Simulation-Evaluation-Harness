"""Evidence engine for trace detection, audits, clues, and memories."""

from __future__ import annotations

import random

from .models import (
    ChannelType,
    Clue,
    ClueStatus,
    Memory,
    Trace,
    WorldState,
    _new_id,
    clamp,
)


CHANNEL_DEFAULTS = {
    ChannelType.AUDIT.value: {"reliability": 0.85, "misleading": 0.10, "cost": 200},
    ChannelType.INFORMANT.value: {"reliability": 0.55, "misleading": 0.35, "cost": 50},
    ChannelType.PATROL.value: {"reliability": 0.65, "misleading": 0.20, "cost": 30},
    ChannelType.MEETING.value: {"reliability": 0.40, "misleading": 0.40, "cost": 0},
    ChannelType.ROUTINE_REPORT.value: {"reliability": 0.50, "misleading": 0.30, "cost": 0},
    ChannelType.ACCIDENT_EXPOSURE.value: {"reliability": 0.80, "misleading": 0.15, "cost": 0},
    ChannelType.BUDGET_REVIEW.value: {"reliability": 0.75, "misleading": 0.12, "cost": 100},
}


def scan_all_traces(world: WorldState) -> list[Clue]:
    new_clues: list[Clue] = []
    for trace in list(world.traces.values()):
        if trace.discovered or trace.strength < 5.0:
            continue
        for channel_name in trace.detectable_by:
            clue = _try_detect(world, trace, channel_name)
            if clue:
                world.clues[clue.id] = clue
                trace.discovered = True
                new_clues.append(clue)
                break
    return new_clues


def _try_detect(world: WorldState, trace: Trace, channel_name: str) -> Clue | None:
    channel = CHANNEL_DEFAULTS.get(channel_name, {})
    reliability = channel.get("reliability", 0.50)
    misleading_risk = channel.get("misleading", 0.25)

    probability = clamp(trace.strength / 100.0 * reliability, 0.02, 0.90)
    if channel_name == ChannelType.INFORMANT.value:
        informant_power = sum(1 for edge in world.social_edges.values() if "informant" in edge.tags)
        probability = clamp(probability + informant_power * 0.05, 0.02, 0.95)

    if random.random() > probability:
        return None

    confidence = clamp(trace.strength * reliability * random.uniform(0.75, 1.25), 10, 95)
    status = ClueStatus.SUSPECTED.value if confidence >= 45 else ClueStatus.UNVERIFIED.value
    return Clue(
        id=_new_id("CL"),
        tick_created=world.clock.current_tick,
        source_channel=channel_name,
        holder_node_id="CHIEF",
        related_trace_id=trace.id,
        content=_clue_text(trace.trace_type, channel_name, confidence),
        confidence=confidence,
        source_reliability=clamp(reliability * 100, 20, 95),
        misleading_risk=clamp(misleading_risk * 100, 5, 70),
        status=status,
        possible_explanations=_alt_explanations(trace.trace_type),
    )


def run_audit(world: WorldState, target_id: str) -> list[Clue]:
    clues: list[Clue] = []
    budget_pool = world.get_resource("budget_pool")
    if budget_pool and budget_pool.amount_available >= 100:
        budget_pool.amount_available -= 100
        budget_pool.amount_spent += 100
    else:
        return clues

    relevant_traces = [
        trace
        for trace in world.traces.values()
        if trace.strength > 5.0 and (
            trace.linked_world_object_id == target_id or target_id in str(trace.location or "")
        )
    ]

    for trace in relevant_traces:
        confidence = clamp(trace.strength * 0.90 * random.uniform(0.9, 1.15), 35, 98)
        clue = Clue(
            id=_new_id("CL"),
            tick_created=world.clock.current_tick,
            source_channel=ChannelType.AUDIT.value,
            holder_node_id="CHIEF",
            related_trace_id=trace.id,
            content=_clue_text(trace.trace_type, ChannelType.AUDIT.value, confidence),
            confidence=confidence,
            source_reliability=85.0,
            misleading_risk=10.0,
            status=ClueStatus.CONFIRMED.value if confidence >= 70 else ClueStatus.SUSPECTED.value,
            possible_explanations=_alt_explanations(trace.trace_type),
        )
        world.clues[clue.id] = clue
        trace.discovered = True
        clues.append(clue)
        _apply_audit_consequence(world, target_id, trace, clue)

    world.add_history(f"Audit on {target_id}: {len(clues)} clues found.")
    return clues


def plant_informant(world: WorldState, target_id: str) -> tuple[bool, str]:
    budget_pool = world.get_resource("budget_pool")
    if budget_pool and budget_pool.amount_available >= 50:
        budget_pool.amount_available -= 50
        budget_pool.amount_spent += 50
    else:
        return False, "Not enough budget."

    edge = world.social_edges.get(f"CHIEF->{target_id}")
    if not edge:
        from .social_network import get_or_create_edge

        edge = get_or_create_edge(world, "CHIEF", target_id)
    edge.information_flow = clamp(edge.information_flow + 20.0)
    if "informant" not in edge.tags:
        edge.tags.append("informant")
    world.add_history(f"Informant planted to monitor {target_id}.")
    return True, f"Informant planted on {target_id}."


def deposit_memories(world: WorldState) -> int:
    count = 0
    for signal in list(world.signals.values()):
        if not signal.active or signal.memory_strength < 40.0:
            continue
        for holder_id in signal.current_holder_ids:
            if random.random() >= signal.memory_strength / 200.0:
                continue

            sentiment = 0.0
            if signal.signal_type == "broken_expectation":
                sentiment = -0.7
            elif signal.signal_type == "disappointment":
                sentiment = -0.35
            elif signal.signal_type in {"promise", "appointment"} and signal.truth_status == "true":
                sentiment = 0.25
            elif signal.truth_status == "true":
                sentiment = 0.3 if "complaint" in signal.signal_type else -0.2
            elif signal.truth_status == "false":
                sentiment = -0.4

            memory = Memory(
                id=_new_id("M"),
                holder_node_id=holder_id,
                source_signal_id=signal.id,
                topic=signal.signal_type,
                sentiment=sentiment,
                strength=signal.memory_strength,
                created_tick=world.clock.current_tick,
                last_reinforced_tick=world.clock.current_tick,
            )
            world.memories[memory.id] = memory
            if holder_id in world.social_nodes:
                world.social_nodes[holder_id].memory_ids.append(memory.id)
            count += 1
    return count


def _apply_audit_consequence(world: WorldState, target_id: str, trace: Trace, clue: Clue) -> None:
    from .signal_engine import create_signal

    task = world.get_task(target_id)
    if task and task.assignee_node_id in world.social_nodes:
        assignee = world.social_nodes[task.assignee_node_id]
        if trace.trace_type == "schedule_delay" and (
            task.progress_reported - task.progress_true >= 10.0 or task.false_report_risk >= 20.0
        ):
            assignee.report_honesty = clamp(assignee.report_honesty - 8.0)
            assignee.fear = clamp(assignee.fear + 5.0)
            assignee.concealment_tendency = clamp(assignee.concealment_tendency - 4.0)
            create_signal(
                world,
                "audit_result",
                source_node_id="CHIEF",
                intended_receivers=[assignee.id],
                content=f"Accountability review triggered for {task.id}",
                truth_status="true",
                intensity=55.0,
                secrecy=10.0,
                memory_strength=60.0,
                linked_objects=[task.id],
                tags=["accountability"],
            )
            memory = Memory(
                id=_new_id("M"),
                holder_node_id=assignee.id,
                source_signal_id=clue.id,
                topic="accountability",
                sentiment=-0.45,
                strength=60.0,
                created_tick=world.clock.current_tick,
                last_reinforced_tick=world.clock.current_tick,
            )
            world.memories[memory.id] = memory
            assignee.memory_ids.append(memory.id)
        return

    node = world.get_node(target_id)
    if node and trace.trace_type == "concealment_pattern":
        node.report_honesty = clamp(node.report_honesty - 6.0)
        node.fear = clamp(node.fear + 4.0)
        node.concealment_tendency = clamp(node.concealment_tendency - 6.0)
        edge = world.get_edge(target_id, "CHIEF")
        if edge:
            edge.trust = clamp(edge.trust - 6.0)
            edge.fear = clamp(edge.fear + 3.0)


def _clue_text(trace_type: str, channel: str, confidence: float) -> str:
    if trace_type == "schedule_delay":
        if confidence >= 70:
            return "Audit found a confirmed mismatch between reported and actual task progress."
        if confidence >= 40:
            return "Audit suggests task progress may have been overstated."
        return "A weak sign suggests task reporting may not match reality."
    if trace_type == "accounting_irregularity":
        return "Records suggest resources may have been diverted."
    if trace_type == "concealment_pattern":
        return "There are signs someone tried to suppress or conceal a report."
    if trace_type == "private_meeting_pattern":
        return "Repeated private coordination patterns were observed."
    return f"{channel} noticed an irregular pattern around {trace_type}."


def _alt_explanations(trace_type: str) -> list[str]:
    defaults = {
        "schedule_delay": ["real delay", "optimistic reporting", "concealment"],
        "accounting_irregularity": ["bookkeeping issue", "resource diversion", "late paperwork"],
        "concealment_pattern": ["routine secrecy", "active blocking", "rumor spillover"],
    }
    return defaults.get(trace_type, ["uncertain anomaly", "partial information"])


def hold_meeting(world: WorldState) -> list[str]:
    lines = [f"=== Meeting (Tick {world.clock.current_tick}) ==="]
    for node in world.social_nodes.values():
        if not node.active or node.node_type == "chief":
            continue
        if node.stress > 70 and node.report_honesty < 50:
            statement = "The speaker is evasive and clearly under pressure."
        elif node.stress > 50:
            statement = "The speaker acknowledges pressure and asks for slack."
        elif node.report_honesty > 60:
            statement = "The speaker gives a relatively open status update."
        else:
            statement = "The speaker offers a guarded and limited update."
        lines.append(f"  {node.name}: {statement}")
    return lines
