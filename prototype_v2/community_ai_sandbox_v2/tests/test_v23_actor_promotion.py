import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.models import Clue, Memory, Trace
from src.report_engine import generate_debug, generate_status
from src.world import create_default_world, run_tick


def test_background_resident_pool_initializes():
    world = create_default_world()
    assert world.background_residents
    assert len(world.background_residents) >= 20
    for resident in world.background_residents.values():
        assert resident.home_group_id in {"G1", "G2", "G3"}
        assert resident.id not in world.social_nodes


def test_appoint_background_resident_promotes_to_social_node():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R101", "position_id": "position_supply_coordinator"}])

    resident = world.background_residents["R101"]
    assert resident.status == "promoted"
    assert resident.promoted_node_id == "R101"
    assert "R101" in world.social_nodes
    assert world.get_position("position_supply_coordinator").holder_node_id == "R101"
    assert world.get_edge("R101", "CHIEF") is not None
    assert world.get_edge("R101", "G2") is not None
    assert world.social_nodes["R101"].overall_core_score >= 0
    assert any(signal.signal_type == "actor_promotion" and "R101" in signal.content_summary for signal in world.signals.values())


def test_clue_holder_background_resident_promotes_as_witness():
    world = create_default_world()
    clue = Clue(
        id="CL_WITNESS",
        tick_created=world.clock.current_tick,
        source_channel="audit",
        holder_node_id="CHIEF",
        content="A resident near storage may know more.",
        confidence=82.0,
    )
    trace = Trace(
        id="TR_WITNESS",
        tick_created=world.clock.current_tick,
        trace_type="storage_irregularity",
        linked_world_object_id="B2",
        strength=75.0,
        detectable_by=["audit"],
    )
    world.clues[clue.id] = clue
    world.traces[trace.id] = trace
    resident = world.background_residents["R102"]
    resident.linked_clue_ids.append(clue.id)
    resident.linked_trace_ids.append(trace.id)
    resident.clue_relevance_score = 70.0

    run_tick(world)

    assert resident.status == "promoted"
    node = world.social_nodes["R102"]
    assert any(role in node.roles for role in ["witness", "informant", "issue_actor"])
    assert world.get_edge("R102", "CHIEF").information_flow > 0
    assert any(signal.signal_type in {"witness_emergence", "actor_promotion"} and "R102" in signal.content_summary for signal in world.signals.values())


def test_high_ambition_resident_self_promotes_under_opportunity():
    world = create_default_world()
    resident = world.background_residents["R103"]
    resident.ambition = 96.0
    resident.initiative = 92.0
    resident.visibility_seeking = 95.0
    resident.leadership_potential = 88.0
    resident.group_attention_score = 50.0
    resident.contact_with_core_score = 40.0
    world.social_nodes["A3"].stress = 45.0

    for _ in range(3):
        run_tick(world)

    assert resident.status in {"candidate", "promoted"}
    assert any(signal.signal_type == "self_nomination" and "R103" in signal.content_summary for signal in world.signals.values())


def test_resource_position_promotes_resident():
    world = create_default_world()
    resident = world.background_residents["R104"]
    resident.initiative = 78.0
    resident.leadership_potential = 72.0
    resident.resourcefulness = 90.0

    run_tick(world, [{"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage", "title": "Storage", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "force_task", "task_id": "T1"}])
    for _ in range(6):
        run_tick(world)

    assert resident.resource_position_score > 0
    assert resident.status == "promoted"
    assert world.social_nodes["R104"].resource_centrality > 20.0


def test_promotion_inherits_group_attitude_and_memory():
    world = create_default_world()
    world.get_edge("G2", "CHIEF").trust = 22.0
    world.get_edge("G2", "CHIEF").fear = 48.0
    memory = Memory(
        id="M_GROUP",
        holder_node_id="G2",
        source_signal_id="seed",
        topic="broken_expectation",
        sentiment=-0.7,
        strength=80.0,
        created_tick=0,
        last_reinforced_tick=0,
    )
    world.memories[memory.id] = memory
    world.social_nodes["G2"].memory_ids.append(memory.id)

    run_tick(world, [{"type": "appoint", "node_id": "R101", "position_id": "position_supply_coordinator"}])

    edge = world.get_edge("R101", "CHIEF")
    assert edge.trust <= 30.0
    assert edge.fear >= 40.0
    assert any(world.memories[mem_id].topic == "broken_expectation" for mem_id in world.social_nodes["R101"].memory_ids)


def test_no_random_mass_promotion():
    world = create_default_world()
    for _ in range(20):
        run_tick(world)

    promoted = [resident for resident in world.background_residents.values() if resident.status == "promoted"]
    assert len(promoted) <= 2


def test_report_only_shows_visible_promotion_information():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R101", "position_id": "position_supply_coordinator"}])
    report = generate_status(world)
    debug = generate_debug(world)

    assert "R101 emerged as an active actor" in report
    assert "promotion_pressure" not in report
    assert "R101: Mina Zhou status=promoted" in debug
