"""Signal Engine (v2).

Handles signal creation, delayed propagation, blocking, leakage, and decay.
"""

from __future__ import annotations

import random
import re
from typing import Optional

from .models import Clue, ClueStatus, Signal, SignalType, TruthStatus, WorldState, _new_id, clamp
from .social_network import effective_information_flow, get_outgoing_edges


def create_signal(
    world: WorldState,
    signal_type: str,
    source_node_id: str | None = None,
    intended_receivers: list[str] | None = None,
    content: str = "",
    truth_status: str = TruthStatus.UNKNOWN.value,
    intensity: float = 50.0,
    secrecy: float = 0.0,
    spread: float = 50.0,
    decay: float = 10.0,
    distortion: float = 10.0,
    memory_strength: float = 50.0,
    linked_objects: list[str] | None = None,
    linked_traces: list[str] | None = None,
    deadline_tick: int | None = None,
    promise_topic: str | None = None,
    related_signal_id: str | None = None,
    fulfilled: bool = False,
    fulfillment_conditions: list[str] | None = None,
    linked_fulfillment_targets: list[str] | None = None,
    promise_status: str = "pending",
    fulfillment_progress: float = 0.0,
    tags: list[str] | None = None,
) -> Signal:
    if signal_type == SignalType.PROMISE.value:
        if deadline_tick is None:
            match = re.search(r"deadline tick \+(\d+)", content, flags=re.IGNORECASE)
            if match:
                deadline_tick = world.clock.current_tick + int(match.group(1))
        if promise_topic is None:
            if ":" in content:
                promise_topic = content.split(":", 1)[1].split("(", 1)[0].strip()
            else:
                promise_topic = content.strip()

    signal = Signal(
        id=_new_id("S"),
        day_created=world.clock.current_day,
        tick_created=world.clock.current_tick,
        signal_type=signal_type,
        source_node_id=source_node_id,
        intended_receiver_ids=intended_receivers or [],
        current_holder_ids=[source_node_id] if source_node_id else [],
        content_summary=content,
        truth_status=truth_status,
        confidence=clamp(intensity * 0.8, 10, 90),
        intensity=intensity,
        secrecy_level=secrecy,
        spread_rate=spread,
        decay_rate=decay,
        distortion_rate=distortion,
        memory_strength=memory_strength,
        linked_world_object_ids=linked_objects or [],
        linked_trace_ids=linked_traces or [],
        deadline_tick=deadline_tick,
        promise_topic=promise_topic,
        related_signal_id=related_signal_id,
        fulfilled=fulfilled,
        promise_status=promise_status,
        fulfillment_conditions=fulfillment_conditions or [],
        linked_fulfillment_targets=linked_fulfillment_targets or [],
        fulfillment_progress=fulfillment_progress,
        tags=tags or [],
    )
    world.signals[signal.id] = signal

    if source_node_id and source_node_id in world.social_nodes:
        world.social_nodes[source_node_id].known_signal_ids.append(signal.id)

    world.add_debug(f"Signal {signal.id}: {signal_type} from {source_node_id}")
    return signal


def propagate_all_signals(world: WorldState) -> list[Signal]:
    """Propagate all active signals for one tick."""
    spawned: list[Signal] = []
    for signal in list(world.signals.values()):
        if not signal.active:
            continue

        _deliver_pending_arrivals(world, signal)
        spawned.extend(_propagate_one_signal(world, signal))
        _handle_blocked_signal_leakage(world, signal, spawned)

        signal.intensity = clamp(signal.intensity - signal.decay_rate * random.uniform(0.5, 1.5), 0, 100)
        if signal.intensity < 5.0:
            signal.active = False

    return spawned


def _propagate_one_signal(world: WorldState, signal: Signal) -> list[Signal]:
    spawned: list[Signal] = []
    for holder_id in list(signal.current_holder_ids):
        holder = world.social_nodes.get(holder_id)
        if not holder or not holder.active:
            continue

        for edge in get_outgoing_edges(world, holder_id):
            receiver_id = edge.target_id
            if receiver_id in signal.current_holder_ids or receiver_id in signal.pending_holder_arrivals:
                continue

            if receiver_id in signal.blocked_by_node_ids:
                continue

            propagation_penalty = max(0.05, 1.0 - signal.secrecy_level / 120.0)
            p_spread = (signal.spread_rate / 100.0) * effective_information_flow(edge) * propagation_penalty
            p_spread = clamp(p_spread, 0.0, 0.90)

            if random.random() < p_spread:
                signal.pending_holder_arrivals[receiver_id] = world.clock.current_tick + max(1, edge.latency)

                if random.random() < min(1.0, signal.distortion_rate / 100.0 + edge.distortion):
                    distorted = _spawn_distorted_signal(world, signal, holder_id, receiver_id)
                    if distorted:
                        spawned.append(distorted)

            p_leak = (
                signal.secrecy_level / 100.0
                * holder.stress / 100.0
                * max(edge.empathy / 100.0, edge.hostility / 100.0, 0.05)
            )
            if random.random() < clamp(p_leak, 0.0, 0.35):
                leak = _spawn_leak_signal(world, signal, holder_id, receiver_id)
                if leak:
                    spawned.append(leak)

    return spawned


def _deliver_pending_arrivals(world: WorldState, signal: Signal) -> None:
    due_receivers = [
        receiver_id
        for receiver_id, arrival_tick in list(signal.pending_holder_arrivals.items())
        if arrival_tick <= world.clock.current_tick
    ]
    for receiver_id in due_receivers:
        if receiver_id not in signal.current_holder_ids:
            signal.current_holder_ids.append(receiver_id)
            if receiver_id in world.social_nodes:
                world.social_nodes[receiver_id].known_signal_ids.append(signal.id)
                _apply_receiver_history_effects(world, signal, receiver_id)
        signal.pending_holder_arrivals.pop(receiver_id, None)


def _spawn_distorted_signal(world: WorldState, original: Signal, from_id: str, to_id: str) -> Optional[Signal]:
    distorted = create_signal(
        world,
        signal_type=SignalType.RUMOR.value if original.signal_type != SignalType.RUMOR.value else original.signal_type,
        source_node_id=from_id,
        intended_receivers=[to_id],
        content=f"[Distorted from {original.id}] {original.content_summary}",
        truth_status=TruthStatus.MIXED.value,
        intensity=original.intensity * 0.6,
        secrecy=original.secrecy_level * 0.7,
        spread=original.spread_rate * 0.8,
        decay=original.decay_rate * 1.5,
        distortion=original.distortion_rate * 1.3,
        memory_strength=original.memory_strength * 0.5,
        tags=["distorted"],
    )
    return distorted


def _spawn_leak_signal(world: WorldState, original: Signal, from_id: str, to_id: str) -> Optional[Signal]:
    return create_signal(
        world,
        signal_type=SignalType.LEAK.value,
        source_node_id=from_id,
        intended_receivers=[to_id],
        content=f"[Leaked] {original.content_summary}",
        truth_status=original.truth_status,
        intensity=original.intensity * 0.5,
        secrecy=0.0,
        spread=original.spread_rate * 1.2,
        decay=original.decay_rate,
        distortion=original.distortion_rate * 1.5,
        memory_strength=original.memory_strength * 0.7,
        related_signal_id=original.id,
        tags=["leaked", f"from_{original.id}"],
    )


def _handle_blocked_signal_leakage(world: WorldState, signal: Signal, spawned: list[Signal]) -> None:
    if not signal.active or "CHIEF" not in signal.blocked_by_node_ids:
        return
    if signal.secrecy_level < 50.0:
        return
    if any(tag == f"blocked_leak_processed_{world.clock.current_tick}" for tag in signal.tags):
        return

    for holder_id in list(signal.current_holder_ids):
        holder = world.social_nodes.get(holder_id)
        if not holder:
            continue

        chief_edge = world.get_edge("CHIEF", holder_id)
        holder_to_chief = world.get_edge(holder_id, "CHIEF")
        has_informant = chief_edge is not None and "informant" in chief_edge.tags
        high_empathy = holder_to_chief is not None and holder_to_chief.empathy >= 60.0
        high_stress = holder.stress >= 70.0
        if not ((has_informant and high_stress) or (high_empathy and high_stress)):
            continue

        leak = create_signal(
            world,
            signal_type=SignalType.LEAK.value,
            source_node_id=holder_id,
            intended_receivers=["CHIEF"],
            content=f"[Leaked] restricted {signal.signal_type} around {holder_id}",
            truth_status=TruthStatus.MIXED.value,
            intensity=max(20.0, signal.intensity * 0.35),
            secrecy=0.0,
            spread=40.0,
            decay=signal.decay_rate,
            distortion=min(80.0, signal.distortion_rate + 25.0),
            memory_strength=signal.memory_strength * 0.5,
            related_signal_id=signal.id,
            tags=["blocked_leak"],
        )
        leak.current_holder_ids.append("CHIEF")
        spawned.append(leak)

        clue = Clue(
            id=_new_id("CL"),
            tick_created=world.clock.current_tick,
            source_channel="informant" if has_informant else "patrol",
            holder_node_id="CHIEF",
            related_signal_id=signal.id,
            content=f"Low-confidence hint of concealed {signal.signal_type} around {holder_id}.",
            confidence=28.0 if has_informant else 22.0,
            source_reliability=55.0 if has_informant else 45.0,
            misleading_risk=35.0,
            status=ClueStatus.UNVERIFIED.value,
            possible_explanations=["concealment", "rumor", "partial leak"],
        )
        world.clues[clue.id] = clue
        from .models import Trace

        trace = Trace(
            id=_new_id("TR"),
            tick_created=world.clock.current_tick,
            trace_type="concealment_pattern",
            linked_world_object_id=holder_id,
            location=holder_id,
            strength=min(80.0, signal.intensity * 0.7),
            detectable_by=["audit", "informant", "patrol"],
        )
        world.traces[trace.id] = trace
        signal.tags.append(f"blocked_leak_processed_{world.clock.current_tick}")
        break


def _apply_receiver_history_effects(world: WorldState, signal: Signal, receiver_id: str) -> None:
    if not signal.source_node_id or receiver_id not in world.social_nodes:
        return
    edge = world.get_edge(receiver_id, signal.source_node_id)
    if edge is None:
        return

    memory_bias = 0.0
    for memory_id in world.social_nodes[receiver_id].memory_ids:
        memory = world.memories.get(memory_id)
        if not memory:
            continue
        if memory.topic in {"promise_fulfilled", "broken_expectation", "disappointment", "accountability"}:
            memory_bias += memory.sentiment * (memory.strength / 100.0)

    if signal.source_node_id == "CHIEF" and signal.signal_type in {"promise", "order", "request", "appointment"}:
        edge.trust = clamp(edge.trust + memory_bias * 4.0)
        edge.obedience = clamp(edge.obedience + memory_bias * 2.0)
        signal.confidence = clamp(signal.confidence + memory_bias * 12.0, 5, 95)
        if memory_bias < 0:
            world.social_nodes[receiver_id].concealment_tendency = clamp(
                world.social_nodes[receiver_id].concealment_tendency + abs(memory_bias) * 2.0
            )


def deliver_signals_to_chief(world: WorldState) -> list[Signal]:
    return [signal for signal in world.signals.values() if signal.active and "CHIEF" in signal.current_holder_ids]
