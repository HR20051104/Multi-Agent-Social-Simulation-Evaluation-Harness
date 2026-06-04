"""Centrality and long-horizon importance scoring."""

from __future__ import annotations

from .models import SocialNode, WorldState, clamp
from .social_network import get_incoming_edges, get_outgoing_edges


def update_all_centralities(world: WorldState) -> None:
    for node in world.social_nodes.values():
        if node.active:
            _calc_node_centrality(world, node)


def _calc_node_centrality(world: WorldState, node: SocialNode) -> None:
    out_edges = get_outgoing_edges(world, node.id)
    in_edges = get_incoming_edges(world, node.id)
    all_edges = out_edges + in_edges

    managed_resources = [
        obj for obj in world.world_objects.values()
        if getattr(obj, "manager_node_id", None) == node.id
    ]
    held_positions = [
        obj for obj in world.world_objects.values()
        if getattr(obj, "holder_node_id", None) == node.id and hasattr(obj, "nominal_authority")
    ]
    active_tasks = [
        obj for obj in world.world_objects.values()
        if getattr(obj, "assignee_node_id", None) == node.id and getattr(obj, "status", "") not in ("completed", "failed", "cancelled")
    ]
    related_clues = [
        clue for clue in world.clues.values()
        if clue.holder_node_id == "CHIEF" and (
            node.id in clue.content
            or clue.related_signal_id in node.known_signal_ids
            or clue.related_trace_id in {
                trace.id for trace in world.traces.values()
                if trace.linked_world_object_id in {task.id for task in active_tasks}
                or trace.linked_world_object_id == node.id
            }
        )
    ]
    group_edges = [
        edge for edge in all_edges
        if (
            world.social_nodes.get(edge.source_id) and world.social_nodes[edge.source_id].node_type == "resident_group"
        ) or (
            world.social_nodes.get(edge.target_id) and world.social_nodes[edge.target_id].node_type == "resident_group"
        )
    ]
    signal_contacts = [
        signal for signal in world.signals.values()
        if signal.active and (
            node.id in signal.current_holder_ids
            or node.id in signal.intended_receiver_ids
            or node.id in signal.pending_holder_arrivals
        )
    ]

    auth_sum = sum(edge.authority for edge in out_edges) + sum(edge.obedience for edge in in_edges)
    for position in held_positions:
        activity_factor = 0.2
        if managed_resources:
            activity_factor = 1.0
        elif node.known_signal_ids or active_tasks:
            activity_factor = 0.7
        auth_sum += getattr(position, "nominal_authority", 0.0) * activity_factor
    if node.node_type == "chief":
        auth_sum += 80.0
    node.authority_centrality = clamp(auth_sum / max(len(all_edges), 1), 0, 100)

    signal_exposure = min(100.0, len(node.known_signal_ids) * 6.0)
    contact_frequency = clamp(
        (sum(edge.information_flow for edge in all_edges) / max(len(all_edges), 1))
        + len(all_edges) * 2.0
        + len(signal_contacts) * 6.0,
        0,
        100,
    )
    node.signal_exposure_score = signal_exposure
    node.contact_frequency_score = contact_frequency
    node.information_centrality = clamp((signal_exposure * 0.45) + (contact_frequency * 0.55), 0, 100)

    resource_control = max(node.resource_control_score * 0.7, sum(obj.importance for obj in managed_resources))
    for position in held_positions:
        permissions = getattr(position, "permission_tags", [])
        if "manage_inventory" in permissions:
            resource_control += getattr(position, "importance", 0.0) * 0.8
        elif "coordinate_supplies" in permissions:
            resource_control += getattr(position, "importance", 0.0) * 0.5
    if "resource_actor" in node.roles or any(
        tag in node.group_tags for tag in {"warehouse_helper", "maintenance_helper", "maintenance_worker", "ledger_assistant"}
    ):
        resource_control = max(resource_control, 25.0)
    resource_control += min(25.0, len(node.known_signal_ids) * 2.5)
    node.resource_control_score = clamp(resource_control, 0, 100)
    node.resource_centrality = node.resource_control_score

    task_relevance = 0.0
    for task in active_tasks:
        task_relevance += 12.0
        if getattr(task, "risk", 0.0) > 40.0:
            task_relevance += 12.0
    node.task_relevance_score = clamp(task_relevance, 0, 100)

    clue_relevance = sum(clue.confidence for clue in related_clues) / max(len(related_clues), 1) if related_clues else 0.0
    node.clue_relevance_score = clamp(clue_relevance, 0, 100)

    group_attention = sum(edge.information_flow + edge.dependency + edge.competition for edge in group_edges) / max(len(group_edges), 1) if group_edges else 0.0
    node.group_attention_score = clamp(group_attention, 0, 100)

    access = 0.0
    chief_out = world.social_edges.get(f"CHIEF->{node.id}")
    node_to_chief = world.social_edges.get(f"{node.id}->CHIEF")
    if chief_out:
        access += chief_out.information_flow * 0.3
        access += chief_out.authority * 0.5
    if node_to_chief:
        access += node_to_chief.information_flow * 0.2
    access += node.authority_centrality * 0.2
    node.access_to_chief = clamp(access, 0, 100)

    node.issue_relevance = clamp(
        node.task_relevance_score * 0.5
        + node.signal_exposure_score * 0.2
        + node.clue_relevance_score * 0.2
        + node.group_attention_score * 0.1,
        0,
        100,
    )

    raw_core = clamp(
        node.authority_centrality * 0.22
        + node.information_centrality * 0.16
        + node.resource_centrality * 0.20
        + node.access_to_chief * 0.16
        + node.issue_relevance * 0.12
        + node.contact_frequency_score * 0.06
        + node.clue_relevance_score * 0.04
        + node.group_attention_score * 0.04,
        0,
        100,
    )

    if not managed_resources and not node.known_signal_ids and not active_tasks and not held_positions:
        raw_core = clamp(raw_core - 8.0, 0, 100)
    elif held_positions and not managed_resources and not node.known_signal_ids and not active_tasks:
        raw_core = clamp(raw_core - 4.0, 0, 100)
    if held_positions and not managed_resources and any(
        "manage_inventory" in getattr(position, "permission_tags", [])
        or "coordinate_supplies" in getattr(position, "permission_tags", [])
        for position in held_positions
    ):
        raw_core = clamp(raw_core - 8.0, 0, 100)

    node.overall_core_score = raw_core
    previous_sustained = getattr(node, "sustained_core_score", raw_core)
    node.sustained_core_score = clamp(previous_sustained * 0.75 + raw_core * 0.25, 0, 100)


def get_core_nodes(world: WorldState, threshold: float = 40.0) -> list[SocialNode]:
    return [node for node in world.social_nodes.values() if node.active and node.overall_core_score >= threshold]


def get_periphery_nodes(world: WorldState, threshold: float = 25.0) -> list[SocialNode]:
    return [node for node in world.social_nodes.values() if node.active and node.overall_core_score < threshold]
