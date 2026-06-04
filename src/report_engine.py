"""Player-facing report generation and developer debug output."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Iterable

from .models import Clue, WorldState


def generate_status(world: WorldState) -> str:
    budget_pool = world.get_resource("budget_pool")
    material_pool = world.get_resource("material_pool")
    labor_pool = world.get_resource("labor_pool")
    active_tasks = world.get_active_tasks()
    visible_clues = [clue for clue in world.clues.values() if clue.holder_node_id == "CHIEF"]
    clue_groups = _group_visible_clues(visible_clues)
    fresh_clues = [summary for summary in clue_groups if summary["confidence"] >= 45]
    anomalies = [summary for summary in clue_groups if summary["confidence"] < 45]
    developments = _visible_social_developments(world)

    lines = [
        "Public Situation",
        (
            f"Tick {world.clock.current_tick}, Day {world.clock.current_day} ({world.clock.time_of_day}). "
            f"Budget {budget_pool.amount_available if budget_pool else 0:.0f}, "
            f"materials {material_pool.amount_available if material_pool else 0:.0f}, "
            f"labor {labor_pool.amount_available if labor_pool else 0:.0f}."
        ),
        "",
        "Tasks",
    ]

    if active_tasks:
        for task in active_tasks:
            reported = task.progress_reported if task.progress_reported > 0 else task.progress_true
            line = (
                f"- {task.id}: {task.name} [{task.status}] "
                f"reported {reported:.0f}% budget {task.reserved_budget}/{task.required_budget}"
            )
            if task.blocked_reason:
                line += f"; blocked by {task.blocked_reason}"
            lines.append(line)
    else:
        lines.append("- No active tasks.")

    lines.extend(["", "New Clues"])
    if fresh_clues:
        for summary in fresh_clues[:5]:
            lines.append(f"- {summary['text']}")
    else:
        lines.append("- No strong new clues have reached CHIEF.")

    lines.extend(["", "Unconfirmed Anomalies"])
    if anomalies:
        for summary in anomalies[:5]:
            lines.append(f"- {summary['text']}")
    else:
        lines.append("- No unresolved weak anomalies are currently visible.")

    lines.extend(["", "New Social Development"])
    if developments:
        for item in developments[:5]:
            lines.append(f"- {item}")
    else:
        lines.append("- No new residents have stepped into the active network.")

    lines.extend(["", "Social Atmosphere", f"- {_social_atmosphere(world)}"])
    lines.extend(["", "Suggested Attention"])
    attention = _suggested_attention(active_tasks, anomalies, world)
    if attention:
        for item in attention:
            lines.append(f"- {item}")
    else:
        lines.append("- No immediate attention hotspots.")
    return "\n".join(lines)


def generate_debug(world: WorldState) -> str:
    lines = [
        "=== DEBUG: True State ===",
        f"Tick: {world.clock.current_tick} / Day: {world.clock.current_day}",
        "",
        "--- Social Nodes ---",
    ]
    for node in world.social_nodes.values():
        lines.append(
            f"  {node.id}: {node.name} ({node.node_type}) "
            f"stress={node.stress:.0f} fear={node.fear:.0f} honesty={node.report_honesty:.0f} "
            f"core={node.overall_core_score:.0f} sustained_core={node.sustained_core_score:.0f}"
        )
        lines.append(
            f"    metrics: signal={node.signal_exposure_score:.0f} resource={node.resource_control_score:.0f} "
            f"task={node.task_relevance_score:.0f} contact={node.contact_frequency_score:.0f} "
            f"clue={node.clue_relevance_score:.0f} attention={node.group_attention_score:.0f}"
        )

    lines.extend(["", "--- Background Residents ---"])
    for resident in world.background_residents.values():
        lines.append(
            f"  {resident.id}: {resident.name} status={resident.status} group={resident.home_group_id} "
            f"pressure={resident.promotion_pressure:.0f} reason={resident.promotion_reason or '-'} "
            f"candidate_since={resident.candidate_since_tick} promoted_node={resident.promoted_node_id}"
        )
        lines.append(
            f"    latent: ambition={resident.ambition:.0f} initiative={resident.initiative:.0f} "
            f"social={resident.social_skill:.0f} leadership={resident.leadership_potential:.0f} "
            f"resourceful={resident.resourcefulness:.0f} info_sense={resident.information_sensitivity:.0f}"
        )
        lines.append(
            f"    trajectory: signal={resident.signal_exposure_score:.0f} clue={resident.clue_relevance_score:.0f} "
            f"resource={resident.resource_position_score:.0f} attention={resident.group_attention_score:.0f} "
            f"event={resident.event_relevance_score:.0f} contact={resident.contact_with_core_score:.0f}"
        )

    lines.extend(["", "--- Social Edges (to CHIEF) ---"])
    for key, edge in world.social_edges.items():
        if key.endswith("->CHIEF"):
            lines.append(
                f"  {key}: trust={edge.trust:.0f} fear={edge.fear:.0f} obedience={edge.obedience:.0f} "
                f"secrecy={edge.secrecy:.0f} info_flow={edge.information_flow:.0f} "
                f"competition={edge.competition:.0f} hostility={edge.hostility:.0f}"
            )

    lines.extend(["", "--- Active Signals ---"])
    for signal in world.signals.values():
        if signal.active:
            pending = ", ".join(
                f"{receiver}@{arrival_tick}" for receiver, arrival_tick in sorted(signal.pending_holder_arrivals.items())
            ) or "-"
            blocked = ", ".join(signal.blocked_by_node_ids) or "-"
            lines.append(
                f"  {signal.id}: [{signal.signal_type}] '{signal.content_summary[:60]}' "
                f"holders={signal.current_holder_ids} pending=[{pending}] "
                f"secrecy={signal.secrecy_level:.0f} spread={signal.spread_rate:.0f} "
                f"decay={signal.decay_rate:.0f} blocked_by=[{blocked}] "
                f"promise_status={signal.promise_status} fulfillment={signal.fulfillment_progress:.2f}"
            )

    lines.extend(["", "--- Traces ---"])
    for trace in world.traces.values():
        lines.append(f"  {trace.id}: [{trace.trace_type}] strength={trace.strength:.0f} discovered={trace.discovered}")

    lines.extend(["", "--- Clues (Full) ---"])
    for clue in world.clues.values():
        lines.append(
            f"  {clue.id}: holder={clue.holder_node_id} channel={clue.source_channel} "
            f"confidence={clue.confidence:.0f} content={clue.content}"
        )

    lines.extend(["", "--- Active Disturbances ---"])
    for disturbance in world.disturbances.values():
        if disturbance.active:
            lines.append(
                f"  {disturbance.id}: [{disturbance.disturbance_type}] intensity={disturbance.intensity:.0f} "
                f"age={disturbance.age_ticks}/{disturbance.duration_ticks} source={disturbance.source_node_id}"
            )
    return "\n".join(lines)


def _group_visible_clues(clues: Iterable[Clue]) -> list[dict]:
    groups: dict[tuple[str, str, int], list[Clue]] = defaultdict(list)
    for clue in sorted(clues, key=lambda item: item.tick_created):
        topic = clue.related_trace_id or clue.related_signal_id or clue.content
        bucket = clue.tick_created // 5
        groups[(topic, clue.source_channel, bucket)].append(clue)

    summaries: list[dict] = []
    for grouped_clues in groups.values():
        grouped_clues.sort(key=lambda item: item.confidence, reverse=True)
        top = grouped_clues[0]
        avg_confidence = sum(item.confidence for item in grouped_clues) / len(grouped_clues)
        text = _clean_confidence_text(top.content)
        if len(grouped_clues) > 1:
            text = f"{text} (merged {len(grouped_clues)} similar clues)"
        summaries.append({"tick": top.tick_created, "confidence": avg_confidence, "text": f"[{top.source_channel}] {text}"})
    summaries.sort(key=lambda item: item["tick"], reverse=True)
    return summaries


def _clean_confidence_text(text: str) -> str:
    cleaned = re.sub(r"(confidence\s+\d+%)(?:\s+\1)+", r"\1", text, flags=re.IGNORECASE)
    cleaned = cleaned.replace("confidence confidence", "confidence").replace("%%", "%")
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    return cleaned.strip(" :")


def _visible_social_developments(world: WorldState) -> list[str]:
    items: list[str] = []
    for signal in world.signals.values():
        if not signal.active or "CHIEF" not in signal.current_holder_ids:
            continue
        if signal.signal_type in {"actor_promotion", "witness_emergence", "self_nomination"}:
            items.append(signal.content_summary)
    return items[-5:]


def _social_atmosphere(world: WorldState) -> str:
    if not world.social_nodes:
        return "No active social readings."
    avg_stress = sum(node.stress for node in world.social_nodes.values()) / len(world.social_nodes)
    avg_fear = sum(node.fear for node in world.social_nodes.values()) / len(world.social_nodes)
    if avg_stress > 45 or avg_fear > 30:
        return "Pressure is elevated and several relationships are carrying tension."
    if avg_stress > 30:
        return "The network is alert but still mostly manageable."
    return "The network is relatively stable on the surface."


def _suggested_attention(active_tasks, anomalies: list[dict], world: WorldState) -> list[str]:
    suggestions: list[str] = []
    blocked = [task for task in active_tasks if task.blocked_reason]
    if blocked:
        suggestions.append(f"{len(blocked)} task(s) are blocked and may need intervention.")
    if anomalies:
        suggestions.append("Weak anomalies are accumulating; consider audit or patrol.")
    if any(signal.signal_type in {"broken_expectation", "disappointment"} and signal.active for signal in world.signals.values()):
        suggestions.append("Promise credibility is under pressure.")
    if any(node.sustained_core_score > 45 for node in world.social_nodes.values() if node.node_type in {"resident", "emergent_actor"}):
        suggestions.append("A resident-level actor is sustaining unusual core relevance.")
    if any(resident.status == "candidate" for resident in world.background_residents.values()):
        suggestions.append("Some background residents are nearing promotion thresholds.")
    return suggestions[:5]
