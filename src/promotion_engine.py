"""Minimal actor-promotion loop for low-resolution background residents."""

from __future__ import annotations

from .influence_engine import create_disturbance
from .models import BackgroundResident, Memory, NodeType, SignalType, SocialNode, WorldState, _new_id, clamp
from .signal_engine import create_signal
from .social_network import get_or_create_edge


def initialize_background_residents(world: WorldState) -> None:
    if world.background_residents:
        return

    specs = [
        ("R101", "Mina Zhou", "G2", "B2", ["courtyard_helper"], ["courtyard"], 85, 80, 70, 75, 55, 72, 78, 62, 48, 68),
        ("R102", "Liu Sen", "G1", "B1", ["floor_runner"], ["stairwell"], 58, 52, 46, 60, 55, 88, 54, 57, 42, 45),
        ("R103", "He Lan", "G3", "B3", ["block_spokesperson"], ["lobby"], 92, 86, 61, 72, 60, 66, 80, 64, 40, 90),
        ("R104", "Qiao Jun", "G2", "B2", ["warehouse_helper"], ["storage", "warehouse"], 68, 70, 58, 52, 56, 60, 63, 86, 47, 50),
        ("R105", "Deng Yue", "G1", "B1", ["clinic_helper"], ["clinic"], 48, 44, 38, 65, 42, 68, 55, 58, 35, 35),
        ("R106", "Pan Rui", "G1", "B1", ["gate_volunteer"], ["gate"], 55, 49, 40, 57, 60, 54, 50, 52, 43, 41),
        ("R107", "Song Wei", "G1", "B1", ["maintenance_helper"], ["pipes"], 47, 51, 44, 48, 58, 50, 46, 72, 41, 39),
        ("R108", "Yao Lin", "G1", "B1", ["ledger_assistant"], ["office"], 59, 53, 51, 55, 45, 70, 52, 61, 52, 47),
        ("R109", "Bao Xi", "G1", "B1", ["courtyard_helper"], ["courtyard"], 50, 47, 37, 49, 41, 53, 44, 55, 34, 36),
        ("R110", "Guo Mei", "G1", "B1", ["night_watch"], ["gate"], 46, 43, 45, 50, 66, 58, 45, 50, 39, 33),
        ("R111", "Tang Hao", "G2", "B2", ["maintenance_helper"], ["boiler"], 53, 55, 42, 47, 52, 57, 49, 75, 44, 38),
        ("R112", "Feng Lu", "G2", "B2", ["ledger_assistant"], ["office"], 57, 52, 54, 58, 43, 73, 50, 63, 55, 46),
        ("R113", "Xu Qian", "G2", "B2", ["yard_runner"], ["yard"], 49, 45, 41, 52, 49, 52, 47, 56, 36, 37),
        ("R114", "Han Yu", "G2", "B2", ["gate_volunteer"], ["gate"], 52, 48, 40, 50, 60, 56, 48, 53, 40, 35),
        ("R115", "Lei Zhen", "G2", "B2", ["clinic_helper"], ["clinic"], 45, 44, 35, 59, 42, 64, 46, 54, 32, 30),
        ("R116", "Zheng Ao", "G3", "B3", ["warehouse_helper"], ["storage"], 54, 56, 48, 49, 55, 58, 51, 74, 45, 42),
        ("R117", "Luo Xin", "G3", "B3", ["floor_runner"], ["stairwell"], 47, 50, 38, 56, 44, 62, 48, 55, 39, 40),
        ("R118", "Wu Jia", "G3", "B3", ["maintenance_helper"], ["pipes"], 51, 48, 43, 46, 54, 55, 47, 70, 42, 34),
        ("R119", "Zhou Qing", "G3", "B3", ["courtyard_helper"], ["courtyard"], 52, 49, 39, 53, 48, 57, 50, 57, 37, 44),
        ("R120", "Lin Ke", "G3", "B3", ["ledger_assistant"], ["office"], 60, 54, 50, 60, 45, 76, 56, 62, 51, 49),
    ]

    for spec in specs:
        (
            resident_id, name, group_id, building_id, role_tags, location_tags, ambition, initiative,
            opportunism, social_skill, risk_tolerance, info_sensitivity, leadership, resourcefulness,
            moral_flexibility, visibility,
        ) = spec
        world.background_residents[resident_id] = BackgroundResident(
            id=resident_id,
            name=name,
            home_group_id=group_id,
            home_building_id=building_id,
            role_tags=list(role_tags),
            location_tags=list(location_tags),
            ambition=ambition,
            initiative=initiative,
            opportunism=opportunism,
            social_skill=social_skill,
            risk_tolerance=risk_tolerance,
            information_sensitivity=info_sensitivity,
            leadership_potential=leadership,
            resourcefulness=resourcefulness,
            moral_flexibility=moral_flexibility,
            visibility_seeking=visibility,
            created_tick=world.clock.current_tick,
            last_updated_tick=world.clock.current_tick,
        )


def update_background_residents(world: WorldState) -> None:
    for resident in world.background_residents.values():
        if resident.status in {"promoted", "inactive"}:
            continue
        _update_trajectory_scores(world, resident)
        _update_promotion_pressure(world, resident)
        _advance_candidate_status(world, resident)
        _maybe_promote(world, resident)


def promote_resident(world: WorldState, resident_id: str, reason: str, role_hint: str | None = None) -> SocialNode:
    resident = world.get_background_resident(resident_id)
    if resident is None:
        raise KeyError(resident_id)
    if resident.promoted_node_id and resident.promoted_node_id in world.social_nodes:
        return world.social_nodes[resident.promoted_node_id]

    group_edge = world.get_edge(resident.home_group_id, "CHIEF")
    inherited_trust = group_edge.trust if group_edge else 50.0
    inherited_fear = group_edge.fear if group_edge else 10.0
    inherited_anger = 15.0
    group_node = world.get_node(resident.home_group_id)
    if group_node:
        inherited_anger = clamp(group_node.resentment + group_node.stress * 0.2)

    competence = clamp(
        resident.social_skill * 0.4 + resident.resourcefulness * 0.3 + resident.leadership_potential * 0.3
    )
    honesty_trait = clamp(50.0 + (100.0 - resident.moral_flexibility) * 0.2)
    greed_trait = clamp(resident.opportunism * 0.5 + resident.moral_flexibility * 0.3)
    concealment = clamp(resident.opportunism * 0.4 + resident.moral_flexibility * 0.3)
    cooperation = clamp(resident.social_skill * 0.4 + resident.leadership_potential * 0.3)

    node = SocialNode(
        id=resident.id,
        name=resident.name,
        node_type=NodeType.EMERGENT_ACTOR.value,
        roles=["promoted_resident"] + ([role_hint] if role_hint else []),
        group_tags=list(dict.fromkeys(resident.role_tags + [resident.home_group_id])),
        stress=clamp(20.0 + resident.event_relevance_score * 0.2),
        fear=inherited_fear,
        anger=inherited_anger,
        hope=clamp(50.0 + resident.initiative / 10.0),
        morale=50.0,
        competence=competence,
        honesty_trait=honesty_trait,
        greed_trait=greed_trait,
        risk_tolerance=resident.risk_tolerance,
        concealment_tendency=concealment,
        cooperation_tendency=cooperation,
        report_honesty=clamp(55.0 + honesty_trait * 0.15 - concealment * 0.1),
        signal_exposure_score=resident.signal_exposure_score,
        resource_control_score=resident.resource_position_score,
        resource_centrality=resident.resource_position_score,
        clue_relevance_score=resident.clue_relevance_score,
        group_attention_score=resident.group_attention_score,
        sustained_core_score=clamp(resident.promotion_pressure * 0.3),
        overall_core_score=clamp(resident.promotion_pressure * 0.2),
    )
    node.known_signal_ids = list(dict.fromkeys(resident.known_signal_ids))
    world.social_nodes[node.id] = node

    _seed_edges(world, resident, node, inherited_trust, inherited_fear, reason)
    _inherit_memories(world, resident, node)

    signal_type = SignalType.ACTOR_PROMOTION.value
    if reason == "witness":
        signal_type = SignalType.WITNESS_EMERGENCE.value
    elif reason == "self_driven":
        signal_type = SignalType.SELF_NOMINATION.value

    promotion_signal = create_signal(
        world,
        signal_type=signal_type,
        source_node_id="CHIEF" if reason == "appointment" else None,
        intended_receivers=["CHIEF"] if reason != "resource_position" else [resident.home_group_id],
        content=f"{resident.id} emerged as an active actor due to {reason.replace('_', ' ')}.",
        truth_status="true",
        intensity=max(35.0, resident.promotion_pressure * 0.75),
        secrecy=0.0 if reason in {"appointment", "witness", "self_driven"} else 20.0,
        spread=55.0,
        memory_strength=55.0,
        tags=["promotion_event", reason],
    )
    if reason in {"appointment", "witness", "self_driven"}:
        if "CHIEF" not in promotion_signal.current_holder_ids:
            promotion_signal.current_holder_ids.append("CHIEF")

    create_disturbance(
        world,
        "actor_promotion",
        source_node_id="CHIEF" if reason == "appointment" else node.id,
        entry_nodes=[node.id],
        intensity=max(30.0, resident.promotion_pressure * 0.6),
        channels=["information_flow", "competition", "empathy", "authority"],
    )

    resident.status = "promoted"
    resident.promoted_node_id = node.id
    resident.promotion_reason = reason
    world.add_history(f"{resident.name} ({resident.id}) was promoted into the active network via {reason}.")
    return node


def get_visible_promotion_candidates(world: WorldState) -> list[BackgroundResident]:
    return [
        resident for resident in world.background_residents.values()
        if resident.status == "candidate" and (
            resident.promotion_reason in {"self_driven", "witness"}
            or any(
                signal.signal_type in {SignalType.SELF_NOMINATION.value, SignalType.WITNESS_EMERGENCE.value}
                and "CHIEF" in signal.current_holder_ids
                and resident.id in signal.content_summary
                for signal in world.signals.values()
            )
        )
    ]


def _update_trajectory_scores(world: WorldState, resident: BackgroundResident) -> None:
    home_group_signals = [
        signal for signal in world.signals.values()
        if signal.active and (
            resident.home_group_id in signal.current_holder_ids
            or resident.home_group_id in signal.intended_receiver_ids
            or signal.source_node_id == resident.home_group_id
            or resident.id in signal.intended_receiver_ids
        )
    ]
    exposure_delta = sum(
        signal.intensity * (resident.information_sensitivity / 100.0) * 0.04
        for signal in home_group_signals
    )
    resident.signal_exposure_score = clamp(resident.signal_exposure_score * 0.92 + exposure_delta)
    for signal in home_group_signals:
        if signal.id not in resident.known_signal_ids:
            resident.known_signal_ids.append(signal.id)

    clue_relevance = 0.0
    for clue_id in resident.linked_clue_ids:
        clue = world.clues.get(clue_id)
        if clue:
            clue_relevance += clue.confidence * 0.5
    for trace_id in resident.linked_trace_ids:
        trace = world.traces.get(trace_id)
        if trace:
            clue_relevance += trace.strength * 0.4
    resident.clue_relevance_score = clamp(resident.clue_relevance_score * 0.9 + clue_relevance)

    resource_bonus = 0.0
    resource_tags = {"warehouse_helper", "maintenance_worker", "maintenance_helper", "gate_volunteer", "ledger_assistant"}
    if set(resident.role_tags) & resource_tags or set(resident.location_tags) & {"warehouse", "storage", "gate", "office", "clinic"}:
        resource_bonus += 12.0
    pressure_tasks = [
        task for task in world.get_active_tasks()
        if task.pressure_level > 20.0 or task.false_report_risk > 15.0 or task.blocked_reason
    ]
    if pressure_tasks:
        resource_bonus += min(48.0, len(pressure_tasks) * 8.0)
    if resident.home_group_id == "G2" and any("storage" in task.task_type for task in pressure_tasks):
        resource_bonus += 12.0
    resident.resource_position_score = clamp(resident.resource_position_score * 0.9 + resource_bonus)

    group_mentions = 0
    for signal in world.signals.values():
        if signal.active and resident.home_group_id in signal.content_summary:
            group_mentions += 1
    for clue in world.clues.values():
        if resident.home_group_id in clue.content:
            group_mentions += 1
    resident.group_attention_score = clamp(
        resident.group_attention_score * 0.92 + group_mentions * (resident.leadership_potential / 20.0)
    )

    event_relevance = 0.0
    for task in world.get_active_tasks():
        if resident.home_building_id and resident.home_building_id in task.name:
            event_relevance += 12.0
        if any(tag in task.task_type for tag in resident.location_tags + resident.role_tags):
            event_relevance += 10.0
        if "storage" in task.task_type and ("warehouse" in resident.location_tags or "warehouse_helper" in resident.role_tags):
            event_relevance += 20.0
    event_relevance += min(20.0, len(resident.linked_trace_ids) * 8.0)
    resident.event_relevance_score = clamp(resident.event_relevance_score * 0.9 + event_relevance)

    group_to_chief = world.get_edge(resident.home_group_id, "CHIEF")
    group_contact = 0.0
    if group_to_chief:
        group_contact += group_to_chief.information_flow * 0.25 + group_to_chief.trust * 0.1
    chief_to_group = world.get_edge("CHIEF", resident.home_group_id)
    if chief_to_group:
        group_contact += chief_to_group.information_flow * 0.25 + chief_to_group.authority * 0.15
    if any(signal.source_node_id == "CHIEF" and resident.id in signal.intended_receiver_ids for signal in world.signals.values()):
        group_contact += 20.0
    resident.contact_with_core_score = clamp(resident.contact_with_core_score * 0.9 + group_contact)

    resident.last_updated_tick = world.clock.current_tick
    resident.clamp_all()


def _update_promotion_pressure(world: WorldState, resident: BackgroundResident) -> None:
    personal_potential = (
        0.18 * resident.ambition
        + 0.16 * resident.initiative
        + 0.14 * resident.social_skill
        + 0.12 * resident.opportunism
        + 0.14 * resident.leadership_potential
        + 0.10 * resident.information_sensitivity
        + 0.08 * resident.resourcefulness
        + 0.04 * resident.risk_tolerance
        + 0.04 * resident.visibility_seeking
    )
    trajectory_score = (
        0.20 * resident.signal_exposure_score
        + 0.20 * resident.clue_relevance_score
        + 0.20 * resident.resource_position_score
        + 0.15 * resident.group_attention_score
        + 0.15 * resident.event_relevance_score
        + 0.10 * resident.contact_with_core_score
    )

    opportunity_bonus = 0.0
    if world.get_position("position_supply_coordinator") and world.get_position("position_supply_coordinator").holder_node_id is None:
        opportunity_bonus += 6.0
    if resident.home_group_id == "G2" and world.get_node("A2") and world.get_node("A2").stress > 30.0:
        opportunity_bonus += 4.0
    if resident.clue_relevance_score > 40.0:
        opportunity_bonus += 6.0
    if resident.resource_position_score > 45.0:
        opportunity_bonus += 6.0
    if resident.resource_position_score > 60.0:
        opportunity_bonus += 8.0
    if (
        resident.ambition >= 85.0
        and resident.initiative >= 80.0
        and resident.visibility_seeking >= 80.0
        and _has_network_gap(world, resident)
    ):
        opportunity_bonus += 24.0

    decay_or_suppression = 6.0 if (trajectory_score < 20.0 and resident.status == "background") else 0.0
    resident.promotion_pressure = clamp(0.55 * personal_potential + 0.45 * trajectory_score + opportunity_bonus - decay_or_suppression)
    if (
        resident.ambition >= 85.0
        and resident.initiative >= 80.0
        and resident.visibility_seeking >= 80.0
        and _has_network_gap(world, resident)
    ):
        resident.promotion_pressure = max(resident.promotion_pressure, 78.0)
    if resident.resource_position_score >= 65.0 and any(
        task.pressure_level > 20.0 or task.false_report_risk > 15.0 or task.blocked_reason
        for task in world.get_active_tasks()
    ):
        resident.promotion_pressure = max(resident.promotion_pressure, 76.0)


def _advance_candidate_status(world: WorldState, resident: BackgroundResident) -> None:
    if resident.status == "background" and resident.promotion_pressure >= 75.0:
        resident.status = "candidate"
        resident.candidate_since_tick = world.clock.current_tick


def _maybe_promote(world: WorldState, resident: BackgroundResident) -> None:
    if resident.status not in {"background", "candidate"}:
        return

    if resident.clue_relevance_score >= 60.0 and (resident.linked_trace_ids or resident.linked_clue_ids):
        resident.promotion_reason = "witness"
        promote_resident(world, resident.id, reason="witness", role_hint="witness")
        return

    if resident.resource_position_score >= 68.0 and resident.promotion_pressure >= 74.0:
        resident.promotion_reason = "resource_position"
        promote_resident(world, resident.id, reason="resource_position", role_hint="resource_actor")
        return

    if resident.promotion_pressure >= 78.0 and _has_network_gap(world, resident):
        if not any(
            signal.signal_type == SignalType.SELF_NOMINATION.value and resident.id in signal.content_summary
            for signal in world.signals.values()
        ):
            nomination = create_signal(
                world,
                signal_type=SignalType.SELF_NOMINATION.value,
                source_node_id=None,
                intended_receivers=["CHIEF"],
                content=f"{resident.id} is trying to step forward from {resident.home_group_id}.",
                truth_status="true",
                intensity=max(35.0, resident.promotion_pressure * 0.55),
                secrecy=10.0,
                spread=35.0,
                memory_strength=40.0,
                tags=["candidate_signal"],
            )
            nomination.current_holder_ids.append("CHIEF")
        resident.promotion_reason = "self_driven"
        if resident.promotion_pressure >= 84.0:
            promote_resident(world, resident.id, reason="self_driven", role_hint="issue_actor")


def _has_network_gap(world: WorldState, resident: BackgroundResident) -> bool:
    building_leader_id = _leader_for_group(resident.home_group_id)
    leader = world.get_node(building_leader_id) if building_leader_id else None
    if leader and (leader.stress > 30.0 or leader.report_honesty < 55.0):
        return True
    if resident.home_group_id == "G2" and world.get_position("position_supply_coordinator") and world.get_position("position_supply_coordinator").holder_node_id is None:
        return True
    return resident.group_attention_score > 28.0 or resident.contact_with_core_score > 24.0


def _seed_edges(world: WorldState, resident: BackgroundResident, node: SocialNode, inherited_trust: float, inherited_fear: float, reason: str) -> None:
    chief_in = get_or_create_edge(world, node.id, "CHIEF")
    chief_in.trust = clamp(inherited_trust)
    chief_in.fear = clamp(inherited_fear)
    chief_in.information_flow = clamp(15.0 + resident.contact_with_core_score * 0.3 + (10.0 if reason in {"witness", "self_driven"} else 0.0))
    chief_in.obedience = clamp(55.0 if reason == "appointment" else 35.0 + resident.initiative * 0.2)

    chief_out = get_or_create_edge(world, "CHIEF", node.id)
    chief_out.authority = clamp(35.0 + (20.0 if reason == "appointment" else 5.0))
    chief_out.information_flow = clamp(18.0 + resident.contact_with_core_score * 0.2)

    group_to_node = get_or_create_edge(world, resident.home_group_id, node.id)
    group_to_node.information_flow = clamp(45.0 + resident.group_attention_score * 0.3)
    group_to_node.empathy = clamp(50.0 + resident.social_skill * 0.2)
    group_to_node.dependency = clamp(25.0 + resident.leadership_potential * 0.15)

    node_to_group = get_or_create_edge(world, node.id, resident.home_group_id)
    node_to_group.information_flow = clamp(45.0 + resident.social_skill * 0.2)
    node_to_group.empathy = clamp(45.0 + resident.social_skill * 0.2)
    node_to_group.dependency = clamp(15.0 + resident.group_attention_score * 0.15)

    leader_id = _leader_for_group(resident.home_group_id)
    if leader_id:
        node_to_leader = get_or_create_edge(world, node.id, leader_id)
        leader_to_node = get_or_create_edge(world, leader_id, node.id)
        node_to_leader.information_flow = clamp(18.0 + resident.signal_exposure_score * 0.2)
        leader_to_node.information_flow = clamp(22.0 + resident.group_attention_score * 0.2)
        if reason == "self_driven":
            node_to_leader.competition = clamp(18.0 + resident.ambition * 0.2)
            leader_to_node.hostility = clamp(8.0 + resident.visibility_seeking * 0.15)
        elif reason == "witness":
            node_to_leader.fear = clamp(12.0 + resident.clue_relevance_score * 0.15)
            leader_to_node.secrecy = clamp(15.0 + resident.clue_relevance_score * 0.2)
        else:
            node_to_leader.trust = clamp(inherited_trust * 0.8)
            leader_to_node.trust = clamp(45.0)

    if reason in {"resource_position", "appointment"} or "warehouse_helper" in resident.role_tags:
        node_to_a4 = get_or_create_edge(world, node.id, "A4")
        a4_to_node = get_or_create_edge(world, "A4", node.id)
        node_to_a4.dependency = clamp(20.0 + resident.resource_position_score * 0.2)
        a4_to_node.competition = clamp(10.0 + resident.resource_position_score * 0.25)
        a4_to_node.information_flow = clamp(20.0 + resident.resource_position_score * 0.15)


def _inherit_memories(world: WorldState, resident: BackgroundResident, node: SocialNode) -> None:
    inherited_ids = list(resident.memory_seed_ids)
    group_node = world.get_node(resident.home_group_id)
    if group_node:
        inherited_ids.extend(group_node.memory_ids[:2])

    for memory_id in inherited_ids:
        source = world.memories.get(memory_id)
        if not source:
            continue
        memory = Memory(
            id=_new_id("M"),
            holder_node_id=node.id,
            source_signal_id=source.source_signal_id,
            topic=source.topic,
            sentiment=source.sentiment * 0.6,
            strength=clamp(source.strength * 0.55),
            decay_rate=source.decay_rate,
            created_tick=world.clock.current_tick,
            last_reinforced_tick=world.clock.current_tick,
        )
        world.memories[memory.id] = memory
        node.memory_ids.append(memory.id)


def _leader_for_group(group_id: str) -> str | None:
    return {
        "G1": "A1",
        "G2": "A2",
        "G3": "A3",
    }.get(group_id)
