"""Influence Engine — disturbance creation and propagation.

Disturbances are ripples that travel through the social network.
They are NOT direct state changes — they are influence pulses that
decay, propagate along edges, and modify nodes/edges as they pass.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from .models import (
    Disturbance, DisturbanceType, SocialEdge,
    WorldState, clamp, _new_id,
)
from .social_network import (
    get_outgoing_edges, edge_channel_strength,
)

if TYPE_CHECKING:
    pass


def _make_effect(
    disturbance: Disturbance,
    target_node_id: str,
    attr: str,
    delta: float,
) -> dict[str, object]:
    return {
        "disturbance_id": disturbance.id,
        "source_node_id": disturbance.source_node_id,
        "target_node_id": target_node_id,
        "attr": attr,
        "delta": delta,
    }

MAX_PROPAGATION_DEPTH = 3
PROPAGATION_THRESHOLD = 0.05  # below this, stop propagating


# ── Disturbance creation ─────────────────────────────────────────────

def create_disturbance(
    world: WorldState,
    dist_type: str,
    source_node_id: str | None = None,
    entry_nodes: list[str] | None = None,
    entry_objects: list[str] | None = None,
    entry_signals: list[str] | None = None,
    intensity: float = 50.0,
    duration: int = 3,
    channels: list[str] | None = None,
    tags: list[str] | None = None,
) -> Disturbance:
    d = Disturbance(
        id=_new_id("D"),
        tick_created=world.clock.current_tick,
        disturbance_type=dist_type,
        source_node_id=source_node_id,
        entry_social_node_ids=entry_nodes or [],
        entry_world_object_ids=entry_objects or [],
        entry_signal_ids=entry_signals or [],
        intensity=intensity,
        duration_ticks=duration,
        propagation_channels=channels or [],
        tags=tags or [],
    )
    world.disturbances[d.id] = d
    world.add_debug(f"Disturbance {d.id} created: {dist_type} intensity={intensity:.0f}")
    return d


# ── Propagation ──────────────────────────────────────────────────────

def propagate_all_disturbances(world: WorldState) -> None:
    """Propagate all active disturbances for one tick."""
    for d in list(world.disturbances.values()):
        if not d.active:
            continue
        _propagate_one(world, d)
        d.age_ticks += 1
        # Decay intensity
        d.intensity = clamp(d.intensity - d.decay_rate, 0, 100)
        if d.age_ticks >= d.duration_ticks or d.intensity < 5.0:
            d.active = False
            world.add_debug(f"Disturbance {d.id} expired.")


def _propagate_one(world: WorldState, d: Disturbance) -> None:
    """BFS propagation of a single disturbance through the social network."""
    # Start from entry nodes
    frontier: set[str] = set(d.entry_social_node_ids)
    visited: set[str] = set()
    depth = 0

    # Temporary cache for accumulated effects this tick
    pending_effects: list[dict[str, object]] = []

    while frontier and depth < MAX_PROPAGATION_DEPTH:
        next_frontier: set[str] = set()
        for node_id in frontier:
            if node_id in visited:
                continue
            visited.add(node_id)

            # Calculate effect on this node
            depth_decay = 0.5 ** depth
            transmitted = d.intensity * depth_decay
            if transmitted < PROPAGATION_THRESHOLD * 100:
                continue

            # Accumulate effects
            _accumulate_disturbance_effects(d, node_id, transmitted, pending_effects)

            # Spread to neighbors via matching channels
            for edge in get_outgoing_edges(world, node_id):
                if edge.target_id in visited:
                    continue
                for channel in d.propagation_channels:
                    ch_strength = edge_channel_strength(edge, channel)
                    if ch_strength > 0.1:
                        next_frontier.add(edge.target_id)

        frontier = next_frontier
        depth += 1

    # Apply accumulated effects
    _apply_effects(world, pending_effects)


def _accumulate_disturbance_effects(
    d: Disturbance, node_id: str, intensity: float, pending_effects: list[dict[str, object]]
) -> None:
    """Determine what effects this disturbance type has on a node."""
    norm = intensity / 100.0

    type_effects: dict[str, dict[str, float]] = {
        DisturbanceType.COERCION.value: {
            "stress": 10.0, "fear": 8.0, "compliance_tendency": 5.0,
            "concealment_tendency": 3.0, "morale": -4.0,
            "trust_to_source": -5.0,
        },
        DisturbanceType.FUNDING.value: {
            "morale": 5.0, "cooperation_tendency": 3.0,
            "trust_to_source": 4.0, "hope": 3.0,
        },
        DisturbanceType.APPOINTMENT.value: {
            "stress": 3.0, "hope": 5.0,
            "trust_to_source": 3.0,
        },
        DisturbanceType.AUDIT.value: {
            "stress": 5.0, "fear": 4.0, "report_honesty": 2.0,
            "concealment_tendency": -3.0,
        },
        DisturbanceType.RESOURCE_SHORTAGE.value: {
            "stress": 8.0, "anger": 5.0, "morale": -5.0,
        },
        DisturbanceType.TASK_DELAY.value: {
            "stress": 4.0, "anger": 2.0, "morale": -3.0,
        },
        DisturbanceType.PUBLIC_SUPPORT.value: {
            "morale": 8.0, "hope": 5.0, "cooperation_tendency": 3.0,
            "trust_to_source": 6.0,
        },
        DisturbanceType.BROKEN_PROMISE.value: {
            "anger": 8.0, "trust_to_source": -8.0, "hope": -5.0,
            "morale": -5.0, "cooperation_tendency": -3.0,
        },
        DisturbanceType.PUBLIC_REBUKE.value: {
            "stress": 12.0, "fear": 8.0, "morale": -6.0,
            "trust_to_source": -6.0, "concealment_tendency": 5.0,
        },
        DisturbanceType.PRIVATE_WARNING.value: {
            "stress": 6.0, "fear": 5.0, "concealment_tendency": 4.0,
            "trust_to_source": -2.0,
        },
        DisturbanceType.RUMOR_BURST.value: {
            "stress": 3.0, "anger": 2.0, "trust_to_source": -2.0,
            "concealment_tendency": 1.0,
        },
    }

    effects = type_effects.get(d.disturbance_type, {})
    for attr, base_delta in effects.items():
        delta = base_delta * norm * random.uniform(0.7, 1.3)
        pending_effects.append(_make_effect(d, node_id, attr, delta))


# ── Apply effects (called from main tick after propagation) ──────────

def _apply_effects(world: WorldState, pending_effects: list[dict[str, object]]) -> None:
    """Apply disturbance effects using the source attached to each effect."""
    aggregated_node_effects: dict[str, dict[str, float]] = {}

    for effect in pending_effects:
        node_id = str(effect["target_node_id"])
        node = world.social_nodes.get(node_id)
        if not node:
            continue

        attr = str(effect["attr"])
        delta = float(effect["delta"])
        source_id = effect.get("source_node_id")

        if attr == "trust_to_source":
            if source_id and source_id != node_id:
                edge = world.social_edges.get(f"{node_id}->{source_id}")
                if edge:
                    edge.trust = clamp(edge.trust + delta)
            continue

        node_effects = aggregated_node_effects.setdefault(node_id, {})
        node_effects[attr] = node_effects.get(attr, 0.0) + delta

    for node_id, attrs in aggregated_node_effects.items():
        node = world.social_nodes.get(node_id)
        if not node:
            continue
        for attr, delta in attrs.items():
            if hasattr(node, attr):
                current = getattr(node, attr)
                setattr(node, attr, clamp(current + delta))
        node.clamp_all()
