import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.models import PositionObject
from src.report_engine import generate_debug
from src.signal_engine import create_signal
from src.world import create_default_world, run_tick


def test_resource_backed_appointment_sustains_core_score_over_20_ticks():
    world = create_default_world()
    baseline = world.social_nodes["R1"].overall_core_score

    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    immediate = world.social_nodes["R1"].overall_core_score

    for _ in range(20):
        run_tick(world)

    resident = world.social_nodes["R1"]
    assert immediate > baseline
    assert resident.overall_core_score >= baseline + 8.0
    assert resident.sustained_core_score >= baseline + 10.0
    assert world.get_edge("A4", "R1").dependency > 0


def test_symbolic_position_decays_over_20_ticks():
    world = create_default_world()
    world.world_objects["symbolic_role"] = PositionObject(
        id="symbolic_role",
        name="Symbolic Role",
        title="Symbolic Role",
        holder_node_id=None,
        permission_tags=[],
        scope="whole_community",
        nominal_authority=25.0,
        actual_authority=25.0,
        importance=20.0,
    )

    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "symbolic_role"}])
    immediate = world.social_nodes["R1"].overall_core_score
    immediate_sustained = world.social_nodes["R1"].sustained_core_score

    for _ in range(20):
        run_tick(world)

    resident = world.social_nodes["R1"]
    assert resident.overall_core_score < immediate
    assert resident.sustained_core_score < immediate_sustained + 5.0


def test_contact_frequency_increases_information_centrality():
    world = create_default_world()
    resident = world.social_nodes["R1"]
    before_contact = resident.contact_frequency_score
    before_information = resident.information_centrality

    for idx in range(4):
        signal = create_signal(
            world,
            "coordination",
            source_node_id="CHIEF",
            intended_receivers=["R1"],
            content=f"Coordination loop {idx}",
            truth_status="true",
            intensity=55.0,
            spread=100.0,
            secrecy=0.0,
        )
        signal.current_holder_ids = ["CHIEF"]
        run_tick(world)

    resident = world.social_nodes["R1"]
    assert resident.contact_frequency_score > before_contact
    assert resident.information_centrality > before_information


def test_loss_of_resource_flow_reduces_core_score():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    for _ in range(4):
        run_tick(world)

    before_loss = world.social_nodes["R1"].overall_core_score
    before_sustained = world.social_nodes["R1"].sustained_core_score
    world.get_resource("material_pool").manager_node_id = "A4"
    world.get_resource("labor_pool").manager_node_id = "A4"

    for _ in range(10):
        run_tick(world)

    resident = world.social_nodes["R1"]
    assert resident.overall_core_score < before_loss
    assert resident.sustained_core_score < before_sustained


def test_debug_report_explains_centrality_change():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    for _ in range(3):
        run_tick(world)

    debug = generate_debug(world)
    assert "R1: Resident Liaison" in debug
    assert "sustained_core=" in debug
    assert "metrics: signal=" in debug
