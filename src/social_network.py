"""Social Network Layer — nodes, edges, and basic graph operations.

Manages SocialNode and SocialEdge CRUD. Does NOT include centrality
calculations (see centrality_engine.py).
"""

from __future__ import annotations

import random
from typing import Optional, TYPE_CHECKING

from .models import (
    SocialNode, SocialEdge, WorldState,
    clamp, _new_id,
)

if TYPE_CHECKING:
    pass


# ── Node operations ──────────────────────────────────────────────────

def get_or_create_node(world: WorldState, node_id: str,
                       name: str = "", node_type: str = "resident") -> SocialNode:
    if node_id in world.social_nodes:
        return world.social_nodes[node_id]
    node = SocialNode(id=node_id, name=name or node_id, node_type=node_type)
    world.social_nodes[node_id] = node
    return node


def update_node_psychology(node: SocialNode) -> None:
    """Natural recovery/decay of psychological states per tick."""
    # Stress recovery
    if node.stress > 20.0:
        node.stress = clamp(node.stress - random.uniform(0.3, 1.5))
    else:
        node.stress = clamp(node.stress + random.uniform(-0.5, 0.5))

    # Fear decay
    if node.fear > 10.0:
        node.fear = clamp(node.fear - random.uniform(0.1, 0.6))

    # Resentment decay if morale is decent
    if node.morale > 40.0 and node.resentment > 5.0:
        node.resentment = clamp(node.resentment - random.uniform(0.2, 1.0))

    # Health recovery
    if node.health < 80.0 and node.stress < 50.0:
        node.health = clamp(node.health + random.uniform(0.2, 1.0))

    # Morale drift toward neutrality based on conditions
    if node.stress > 60.0:
        node.morale = clamp(node.morale - random.uniform(0.3, 1.0))
    elif node.hope > 40.0:
        node.morale = clamp(node.morale + random.uniform(0.2, 0.8))

    node.clamp_all()


# ── Edge operations ──────────────────────────────────────────────────

def get_or_create_edge(world: WorldState, source_id: str, target_id: str) -> SocialEdge:
    key = f"{source_id}->{target_id}"
    if key in world.social_edges:
        return world.social_edges[key]
    edge = SocialEdge(id=_new_id("E"), source_id=source_id, target_id=target_id)
    world.social_edges[key] = edge
    return edge


def ensure_bidirectional_edge(world: WorldState, a_id: str, b_id: str) -> tuple[SocialEdge, SocialEdge]:
    """Create or get edges in both directions between two nodes."""
    forward = get_or_create_edge(world, a_id, b_id)
    backward = get_or_create_edge(world, b_id, a_id)
    return forward, backward


def get_outgoing_edges(world: WorldState, node_id: str) -> list[SocialEdge]:
    """All edges where source == node_id."""
    prefix = f"{node_id}->"
    return [e for k, e in world.social_edges.items() if k.startswith(prefix)]


def get_incoming_edges(world: WorldState, node_id: str) -> list[SocialEdge]:
    """All edges where target == node_id."""
    suffix = f"->{node_id}"
    return [e for k, e in world.social_edges.items() if k.endswith(suffix)]


def get_all_edges_for_node(world: WorldState, node_id: str) -> list[SocialEdge]:
    """All edges involving this node (in either direction)."""
    return get_outgoing_edges(world, node_id) + get_incoming_edges(world, node_id)


# ── Edge weight helpers ──────────────────────────────────────────────

def edge_channel_strength(edge: SocialEdge, channel: str) -> float:
    """Get the strength of a specific channel on this edge (0-1 normalized)."""
    channel_map = {
        "authority": edge.authority / 100.0,
        "fear": edge.fear / 100.0,
        "information_flow": edge.information_flow / 100.0,
        "empathy": edge.empathy / 100.0,
        "trust": edge.trust / 100.0,
        "hostility": edge.hostility / 100.0,
        "dependency": edge.dependency / 100.0,
    }
    return channel_map.get(channel, 0.1)


def effective_information_flow(edge: SocialEdge) -> float:
    """Effective information flow (0-1) considering bandwidth and distortion."""
    raw = (edge.information_flow / 100.0) * (edge.bandwidth / 100.0)
    raw *= (1.0 - edge.distortion)
    return clamp(raw, 0.0, 1.0)
