"""Cognition Engine (v2).

Projects the player-facing knowledge layer from visible clues and signals.
The player only sees what has actually reached CHIEF.
"""

from __future__ import annotations

from .models import KnowledgeStatus, PlayerKnowledge, WorldState, _new_id, clamp


def update_player_knowledge(world: WorldState) -> None:
    """Synthesize all player-visible information into knowledge entries."""
    for clue in list(world.clues.values()):
        if clue.holder_node_id != "CHIEF":
            continue

        topic = _clue_topic(world, clue)
        confidence = clue.confidence
        existing = _find_knowledge(world, topic)
        if existing:
            if clue.id not in existing.source_ids:
                existing.source_ids.append(clue.id)
            existing.confidence = clamp(existing.confidence * 0.6 + confidence * 0.4)
            existing.last_updated_tick = world.clock.current_tick
            existing.status = _status_from_confidence(existing.confidence)
            existing.summary = _merge_summary(existing.summary, clue.content)
        else:
            knowledge_id = _new_id("PK")
            world.player_knowledge[knowledge_id] = PlayerKnowledge(
                id=knowledge_id,
                topic=topic,
                confidence=confidence,
                summary=clue.content,
                source_ids=[clue.id],
                status=_status_from_confidence(confidence),
                last_updated_tick=world.clock.current_tick,
            )

    for signal in world.signals.values():
        if not signal.active:
            continue
        if "CHIEF" not in signal.current_holder_ids:
            continue

        topic = f"signal_{signal.signal_type}"
        confidence = signal.confidence if signal.truth_status != "false" else signal.confidence * 0.5
        existing = _find_knowledge(world, topic)
        if existing:
            if signal.id not in existing.source_ids:
                existing.source_ids.append(signal.id)
            existing.confidence = clamp(existing.confidence * 0.7 + confidence * 0.3)
            existing.last_updated_tick = world.clock.current_tick
            existing.status = _status_from_confidence(existing.confidence)
            existing.summary = _merge_summary(existing.summary, signal.content_summary)
        else:
            knowledge_id = _new_id("PK")
            world.player_knowledge[knowledge_id] = PlayerKnowledge(
                id=knowledge_id,
                topic=topic,
                confidence=confidence,
                summary=signal.content_summary,
                source_ids=[signal.id],
                status=_status_from_confidence(confidence),
                last_updated_tick=world.clock.current_tick,
            )


def _find_knowledge(world: WorldState, topic: str) -> PlayerKnowledge | None:
    for knowledge in world.player_knowledge.values():
        if knowledge.topic == topic:
            return knowledge
    return None


def _clue_topic(world: WorldState, clue) -> str:
    if clue.related_trace_id:
        trace = world.traces.get(clue.related_trace_id)
        if trace:
            object_id = trace.linked_world_object_id or "world"
            return f"trace_{object_id}_{trace.trace_type}"
        return f"trace_{clue.related_trace_id}"
    if clue.related_signal_id:
        return f"signal_{clue.related_signal_id}"
    return f"clue_{clue.id}"


def _status_from_confidence(confidence: float) -> str:
    if confidence >= 80.0:
        return KnowledgeStatus.CONFIRMED.value
    if confidence >= 55.0:
        return KnowledgeStatus.PROBABLE.value
    if confidence >= 35.0:
        return KnowledgeStatus.SUSPECTED.value
    if confidence >= 15.0:
        return KnowledgeStatus.WEAK_SUSPICION.value
    return KnowledgeStatus.UNKNOWN.value


def _merge_summary(existing: str, latest: str) -> str:
    latest = latest.strip()
    if not existing:
        return latest
    if latest == existing or latest in existing:
        return existing
    return f"{existing} | {latest}"
