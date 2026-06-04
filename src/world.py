"""World State Manager (v2): initialization, tick orchestration, persistence."""

from __future__ import annotations

import json
from pathlib import Path

from .centrality_engine import update_all_centralities
from .cognition_engine import update_player_knowledge
from .event_engine import scan_and_generate
from .evidence_engine import deposit_memories, scan_all_traces
from .influence_engine import create_disturbance, propagate_all_disturbances
from .models import (
    BackgroundResident,
    NodeType,
    ObjectType,
    PositionObject,
    ResourcePool,
    SocialEdge,
    SocialNode,
    TaskObject,
    WorldClock,
    WorldObject,
    WorldState,
    clamp,
)
from .promotion_engine import initialize_background_residents, promote_resident, update_background_residents
from .signal_engine import create_signal, propagate_all_signals
from .social_network import get_or_create_edge, update_node_psychology
from .task_engine import advance_all_tasks


def load_world(path: str | Path) -> WorldState:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return WorldState.from_dict(data)


def save_world(world: WorldState, path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(world.to_dict(), f, ensure_ascii=False, indent=2)


def export_debug(world: WorldState, path: str | Path) -> None:
    from .report_engine import generate_debug

    debug_text = generate_debug(world)
    data = {"debug_text": debug_text, "full_state": world.to_dict()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_default_world() -> WorldState:
    """Create a readable default scenario for the sandbox CLI and tests."""
    w = WorldState(clock=WorldClock(ticks_per_day=2))

    nodes = [
        SocialNode(
            id="CHIEF",
            name="Chief Coordinator",
            node_type=NodeType.CHIEF.value,
            authority_centrality=80.0,
            access_to_chief=100.0,
            overall_core_score=80.0,
            sustained_core_score=80.0,
        ),
        SocialNode(
            id="A1",
            name="Building 1 Leader",
            node_type=NodeType.LEADER.value,
            report_honesty=70.0,
            competence=65.0,
            greed_trait=20.0,
            compliance_tendency=55.0,
            concealment_tendency=15.0,
            risk_tolerance=25.0,
        ),
        SocialNode(
            id="A2",
            name="Building 2 Leader",
            node_type=NodeType.LEADER.value,
            report_honesty=45.0,
            competence=55.0,
            greed_trait=45.0,
            stress=35.0,
            compliance_tendency=45.0,
            concealment_tendency=35.0,
            risk_tolerance=35.0,
            resentment=20.0,
        ),
        SocialNode(
            id="A3",
            name="Building 3 Leader",
            node_type=NodeType.LEADER.value,
            report_honesty=65.0,
            competence=50.0,
            greed_trait=25.0,
            compliance_tendency=50.0,
            concealment_tendency=15.0,
            risk_tolerance=20.0,
        ),
        SocialNode(
            id="A4",
            name="Property Manager",
            node_type=NodeType.PROPERTY.value,
            report_honesty=50.0,
            competence=70.0,
            greed_trait=35.0,
            compliance_tendency=50.0,
            concealment_tendency=25.0,
            risk_tolerance=40.0,
        ),
        SocialNode(
            id="A5",
            name="Security Chief",
            node_type=NodeType.SECURITY.value,
            report_honesty=60.0,
            competence=60.0,
            greed_trait=20.0,
            compliance_tendency=60.0,
            concealment_tendency=10.0,
            risk_tolerance=35.0,
        ),
        SocialNode(
            id="R1",
            name="Resident Liaison",
            node_type=NodeType.RESIDENT.value,
            report_honesty=55.0,
            competence=40.0,
            greed_trait=15.0,
            overall_core_score=5.0,
            sustained_core_score=5.0,
        ),
        SocialNode(id="G1", name="Building 1 Residents", node_type=NodeType.RESIDENT_GROUP.value),
        SocialNode(id="G2", name="Building 2 Residents", node_type=NodeType.RESIDENT_GROUP.value),
        SocialNode(id="G3", name="Building 3 Residents", node_type=NodeType.RESIDENT_GROUP.value),
    ]
    for node in nodes:
        w.social_nodes[node.id] = node

    for leader_id in ["A1", "A2", "A3", "A4", "A5"]:
        w.set_edge(
            SocialEdge(
                id=f"E_CHIEF_{leader_id}",
                source_id="CHIEF",
                target_id=leader_id,
                authority=70.0,
                information_flow=50.0,
                bandwidth=60.0,
                visibility=0.8,
            )
        )
        w.set_edge(
            SocialEdge(
                id=f"E_{leader_id}_CHIEF",
                source_id=leader_id,
                target_id="CHIEF",
                trust=55.0,
                fear=10.0,
                obedience=60.0,
                information_flow=40.0,
                bandwidth=40.0,
                visibility=0.6,
            )
        )

    for group_id in ["G1", "G2", "G3"]:
        w.set_edge(
            SocialEdge(
                id=f"E_CHIEF_{group_id}",
                source_id="CHIEF",
                target_id=group_id,
                authority=45.0,
                information_flow=30.0,
                bandwidth=35.0,
                visibility=0.6,
            )
        )
        w.set_edge(
            SocialEdge(
                id=f"E_{group_id}_CHIEF",
                source_id=group_id,
                target_id="CHIEF",
                trust=48.0 if group_id == "G2" else 54.0,
                fear=18.0 if group_id == "G2" else 12.0,
                obedience=42.0,
                information_flow=18.0,
                bandwidth=24.0,
                visibility=0.5,
            )
        )

    w.set_edge(SocialEdge(id="E_A1_A2", source_id="A1", target_id="A2", trust=50.0, empathy=30.0, information_flow=35.0))
    w.set_edge(SocialEdge(id="E_A2_A1", source_id="A2", target_id="A1", trust=45.0, empathy=25.0, information_flow=30.0))
    w.set_edge(SocialEdge(id="E_A2_A3", source_id="A2", target_id="A3", trust=55.0, empathy=40.0, information_flow=40.0))
    w.set_edge(SocialEdge(id="E_A3_A2", source_id="A3", target_id="A2", trust=55.0, empathy=35.0, information_flow=35.0))
    w.set_edge(SocialEdge(id="E_A4_A2", source_id="A4", target_id="A2", dependency=30.0, information_flow=40.0))
    for leader_id in ["A1", "A2", "A3"]:
        w.set_edge(
            SocialEdge(
                id=f"E_A5_{leader_id}",
                source_id="A5",
                target_id=leader_id,
                information_flow=25.0,
                trust=55.0,
            )
        )

    w.world_objects["budget_pool"] = ResourcePool(
        id="budget_pool",
        name="Budget Pool",
        resource_type="budget",
        amount_available=10000.0,
        importance=90.0,
        visibility=0.8,
        manager_node_id="A4",
    )
    w.world_objects["material_pool"] = ResourcePool(
        id="material_pool",
        name="Material Pool",
        resource_type="materials",
        amount_available=100.0,
        importance=70.0,
        visibility=0.7,
        manager_node_id="A4",
    )
    w.world_objects["labor_pool"] = ResourcePool(
        id="labor_pool",
        name="Labor Pool",
        resource_type="labor",
        amount_available=20.0,
        importance=60.0,
        visibility=0.6,
    )

    for object_id, name, location in [
        ("B1", "Building 1", "west"),
        ("B2", "Building 2", "center"),
        ("B3", "Building 3", "east"),
    ]:
        w.world_objects[object_id] = WorldObject(
            id=object_id,
            name=name,
            object_type=ObjectType.BUILDING.value,
            location=location,
            condition=80.0,
            importance=60.0,
            visibility=0.7,
        )

    positions = [
        ("leader_B1", "Building 1 Leader", "A1", ["report_building_status", "organize_residents"], "B1", 40.0),
        ("leader_B2", "Building 2 Leader", "A2", ["report_building_status", "organize_residents"], "B2", 40.0),
        ("leader_B3", "Building 3 Leader", "A3", ["report_building_status", "organize_residents"], "B3", 40.0),
        (
            "property_manager",
            "Property Manager",
            "A4",
            ["manage_property", "coordinate_tasks", "procure_materials"],
            "whole_community",
            55.0,
        ),
        ("security_chief", "Security Chief", "A5", ["patrol", "enforce_order"], "whole_community", 40.0),
        (
            "position_supply_coordinator",
            "Supply Coordinator",
            None,
            ["coordinate_supplies", "manage_inventory"],
            "whole_community",
            30.0,
        ),
    ]
    for position_id, title, holder_id, permissions, scope, authority in positions:
        w.world_objects[position_id] = PositionObject(
            id=position_id,
            name=title,
            title=title,
            holder_node_id=holder_id,
            permission_tags=permissions,
            scope=scope,
            nominal_authority=authority,
            actual_authority=authority,
            importance=50.0,
        )
        if holder_id in w.social_nodes:
            w.social_nodes[holder_id].roles.append(title)

    initialize_background_residents(w)
    return w


def run_tick(world: WorldState, player_actions: list[dict] | None = None) -> dict:
    """Execute one full tick."""
    clock = world.clock
    is_new_day = clock.current_tick > 0 and clock.current_tick % clock.ticks_per_day == 0
    clock.advance()
    if clock.current_tick == 0:
        clock.current_tick = 1

    for action in player_actions or []:
        _process_action(world, action)

    for node in world.social_nodes.values():
        if node.active:
            update_node_psychology(node)

    task_msgs = advance_all_tasks(world)
    propagate_all_disturbances(world)
    new_signals = propagate_all_signals(world)
    event_counts = scan_and_generate(world)
    new_clues = scan_all_traces(world)
    mem_count = deposit_memories(world)
    update_background_residents(world)
    update_all_centralities(world)
    update_player_knowledge(world)

    return {
        "tick": clock.current_tick,
        "day": clock.current_day,
        "time_of_day": clock.time_of_day,
        "is_new_day": is_new_day,
        "active_tasks": len(world.get_active_tasks()),
        "active_disturbances": len(world.get_active_disturbances()),
        "active_signals": len(world.get_active_signals()),
        "new_signals": len(new_signals),
        "new_clues": len(new_clues),
        "memories_deposited": mem_count,
        "task_messages": task_msgs,
        "event_counts": event_counts,
    }


def _process_action(world: WorldState, action: dict) -> None:
    """Turn player commands into signals, disturbances, and world-object changes."""
    action_type = action.get("type", "")

    if action_type == "assign_task":
        from .task_engine import create_task

        task = create_task(
            world,
            title=action.get("title", "Task"),
            task_type=action.get("task_type", "generic"),
            assignee_node_id=action.get("assignee_id", ""),
            required_budget=action.get("budget", 0),
            required_materials=action.get("materials", 0),
            required_labor=action.get("labor", 0),
        )
        create_signal(
            world,
            "order",
            source_node_id="CHIEF",
            intended_receivers=[action.get("assignee_id", "")],
            content=f"Task order: {task.name}",
            truth_status="true",
            linked_objects=[task.id],
        )
        create_disturbance(
            world,
            "coercion" if action.get("forced") else "funding",
            source_node_id="CHIEF",
            entry_nodes=[action.get("assignee_id", "")],
            entry_objects=[task.id],
            intensity=30.0 if action.get("forced") else 15.0,
            channels=["authority", "information_flow"],
        )
        return

    if action_type == "approve_task":
        from .task_engine import approve_task_resources

        ok, _ = approve_task_resources(
            world,
            action.get("task_id", ""),
            budget=action.get("budget", 0),
            materials=action.get("materials", 0),
            labor=action.get("labor", 0),
        )
        if ok:
            create_disturbance(
                world,
                "funding",
                source_node_id="CHIEF",
                entry_objects=[action.get("task_id", "")],
                channels=["authority", "information_flow"],
                intensity=25.0,
            )
        return

    if action_type == "force_task":
        from .task_engine import force_task

        force_task(world, action.get("task_id", ""))
        task = world.get_task(action.get("task_id", ""))
        if task:
            create_disturbance(
                world,
                "coercion",
                source_node_id="CHIEF",
                entry_nodes=[task.assignee_node_id] if task.assignee_node_id else [],
                entry_objects=[task.id],
                intensity=60.0,
                channels=["authority", "fear"],
            )
        return

    if action_type == "appoint":
        _handle_appoint(world, action)
        return

    if action_type == "appoint_deputy":
        _handle_appoint_deputy(world, action)
        return

    if action_type == "promise":
        deadline_delta = int(action.get("deadline_ticks", 0) or 0)
        create_signal(
            world,
            "promise",
            source_node_id="CHIEF",
            intended_receivers=action.get("targets", []),
            content=action.get("content", "Promise issued"),
            intensity=60.0,
            memory_strength=70.0,
            deadline_tick=(world.clock.current_tick + deadline_delta if deadline_delta > 0 else None),
            promise_topic=action.get("promise_topic"),
            fulfillment_conditions=action.get("fulfillment_conditions"),
            linked_fulfillment_targets=action.get("linked_fulfillment_targets"),
        )
        return

    if action_type == "public_rebuke":
        target = action.get("target_id", "")
        create_signal(
            world,
            "public_gesture",
            source_node_id="CHIEF",
            intended_receivers=[target],
            content=f"Public rebuke of {target}",
            intensity=70.0,
            memory_strength=60.0,
        )
        create_disturbance(
            world,
            "public_rebuke",
            source_node_id="CHIEF",
            entry_nodes=[target],
            intensity=70.0,
            channels=["authority", "fear", "information_flow"],
        )
        return

    if action_type == "private_warning":
        target = action.get("target_id", "")
        create_signal(
            world,
            "warning",
            source_node_id="CHIEF",
            intended_receivers=[target],
            content=f"Private warning to {target}",
            secrecy=50.0,
            intensity=40.0,
        )
        create_disturbance(
            world,
            "private_warning",
            source_node_id="CHIEF",
            entry_nodes=[target],
            intensity=40.0,
            channels=["fear", "information_flow"],
        )
        return

    if action_type == "audit":
        from .evidence_engine import run_audit

        run_audit(world, action.get("target_id", ""))
        return

    if action_type == "plant_informant":
        from .evidence_engine import plant_informant

        plant_informant(world, action.get("target_id", ""))


def _handle_appoint(world: WorldState, action: dict) -> None:
    node_id = action.get("node_id", "")
    pos_id = action.get("position_id", "")
    position = world.get_position(pos_id)
    node = world.get_node(node_id)
    if not position:
        return
    if not node:
        background = world.get_background_resident(node_id)
        if background is None:
            return
        node = promote_resident(world, node_id, reason="appointment", role_hint="appointed_actor")

    old_holder = position.holder_node_id
    position.holder_node_id = node_id
    if position.title not in node.roles:
        node.roles.append(position.title)

    chief_to_node = get_or_create_edge(world, "CHIEF", node_id)
    chief_to_node.authority = clamp(chief_to_node.authority + 40.0)
    chief_to_node.information_flow = clamp(chief_to_node.information_flow + 25.0)

    node_to_chief = get_or_create_edge(world, node_id, "CHIEF")
    node_to_chief.obedience = clamp(node_to_chief.obedience + 15.0)
    node_to_chief.information_flow = clamp(node_to_chief.information_flow + 20.0)

    if old_holder and old_holder in world.social_nodes:
        holder = world.social_nodes[old_holder]
        holder.roles = [role for role in holder.roles if role != position.title]
        create_disturbance(
            world,
            "appointment",
            source_node_id="CHIEF",
            entry_nodes=[old_holder],
            intensity=20.0,
            channels=["authority", "information_flow"],
        )

    create_signal(
        world,
        "appointment",
        source_node_id="CHIEF",
        intended_receivers=[node_id],
        content=f"Appointment: {node.name} -> {position.title}",
        truth_status="true",
        intensity=50.0,
        memory_strength=50.0,
        linked_objects=[pos_id],
    )
    create_disturbance(
        world,
        "appointment",
        source_node_id="CHIEF",
        entry_nodes=[node_id],
        intensity=40.0,
        channels=["authority", "information_flow"],
    )

    if position.id == "position_supply_coordinator":
        material_pool = world.get_resource("material_pool")
        labor_pool = world.get_resource("labor_pool")
        if material_pool:
            material_pool.manager_node_id = node_id
        if labor_pool:
            labor_pool.manager_node_id = node_id

        a4_to_new = get_or_create_edge(world, "A4", node_id)
        a4_to_new.competition = clamp(a4_to_new.competition + 35.0)
        a4_to_new.hostility = clamp(a4_to_new.hostility + 15.0)
        a4_to_new.information_flow = clamp(a4_to_new.information_flow + 15.0)
        a4_to_new.trust = clamp(a4_to_new.trust - 10.0)

        new_to_a4 = get_or_create_edge(world, node_id, "A4")
        new_to_a4.fear = clamp(new_to_a4.fear + 8.0)
        new_to_a4.information_flow = clamp(new_to_a4.information_flow + 10.0)
        new_to_a4.trust = clamp(new_to_a4.trust - 3.0)

        create_disturbance(
            world,
            "funding",
            source_node_id="CHIEF",
            entry_nodes=[node_id],
            entry_objects=["material_pool", "labor_pool"],
            intensity=30.0,
            channels=["authority", "information_flow", "dependency"],
        )
        create_disturbance(
            world,
            "appointment",
            source_node_id="CHIEF",
            entry_nodes=["A4"],
            entry_objects=[pos_id],
            intensity=20.0,
            channels=["authority", "dependency", "information_flow"],
        )


def _handle_appoint_deputy(world: WorldState, action: dict) -> None:
    node_id = action.get("node_id", "")
    pos_id = action.get("position_id", "")
    position = world.get_position(pos_id)
    node = world.get_node(node_id)
    if not position or not node:
        return

    if node_id not in position.deputy_node_ids:
        position.deputy_node_ids.append(node_id)

    deputy_position_id = f"deputy_{pos_id}"
    if deputy_position_id not in world.world_objects:
        world.world_objects[deputy_position_id] = PositionObject(
            id=deputy_position_id,
            name=f"Deputy {position.title}",
            title=f"Deputy {position.title}",
            holder_node_id=node_id,
            permission_tags=["assist_leader", "collect_feedback"],
            scope=position.scope,
            nominal_authority=position.nominal_authority * 0.6,
            actual_authority=position.nominal_authority * 0.5,
            importance=35.0,
        )

    if position.holder_node_id and position.holder_node_id in world.social_nodes:
        leader = world.social_nodes[position.holder_node_id]
        edge = world.social_edges.get(f"{leader.id}->CHIEF")
        if edge:
            edge.trust = clamp(edge.trust - 3.0)
        leader.resentment = clamp(leader.resentment + 5.0)

    world.add_history(f"Appointed {node.name} as deputy of {position.title}.")
