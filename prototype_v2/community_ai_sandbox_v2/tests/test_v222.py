import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.evidence_engine import run_audit
from src.report_engine import generate_debug, generate_status
from src.signal_engine import create_signal
from src.world import create_default_world, run_tick


def test_fulfilled_promise_improves_future_trust():
    world = create_default_world()
    baseline = world.social_edges["A2->CHIEF"].trust
    world.world_objects["FULFILL"] = world.get_object("B1")
    world.world_objects["FULFILL"].status = "completed"

    run_tick(world, [{
        "type": "promise",
        "targets": ["A2"],
        "content": "Promise: finish repair (deadline tick +2)",
        "deadline_ticks": 2,
        "promise_topic": "finish repair",
        "linked_fulfillment_targets": ["B1"],
    }])
    run_tick(world)

    assert world.social_edges["A2->CHIEF"].trust > baseline
    assert any(memory.topic == "promise_fulfilled" and memory.holder_node_id == "A2" for memory in world.memories.values())


def test_broken_promise_reduces_future_trust():
    world = create_default_world()
    baseline = world.social_edges["A2->CHIEF"].trust

    run_tick(world, [{
        "type": "promise",
        "targets": ["A2"],
        "content": "Promise: never done (deadline tick +1)",
        "deadline_ticks": 1,
        "promise_topic": "never done",
        "linked_fulfillment_targets": ["MISSING_TARGET"],
    }])
    run_tick(world)
    run_tick(world)

    assert world.social_edges["A2->CHIEF"].trust < baseline
    assert any(memory.topic == "broken_expectation" and memory.holder_node_id == "A2" for memory in world.memories.values())


def test_promise_history_affects_later_signal_response():
    world = create_default_world()

    run_tick(world, [{
        "type": "promise",
        "targets": ["A2"],
        "content": "Promise: never done (deadline tick +1)",
        "deadline_ticks": 1,
        "promise_topic": "never done",
        "linked_fulfillment_targets": ["MISSING_TARGET"],
    }])
    run_tick(world)
    run_tick(world)

    later = create_signal(
        world,
        "order",
        source_node_id="CHIEF",
        intended_receivers=["A2"],
        content="Later order",
        truth_status="true",
        intensity=80.0,
        spread=100.0,
        secrecy=0.0,
    )
    world.social_edges["CHIEF->A2"].information_flow = 100.0
    world.social_edges["CHIEF->A2"].bandwidth = 100.0
    random.seed(2400)
    for _ in range(3):
        run_tick(world)

    assert "A2" in later.current_holder_ids
    assert later.confidence < 64.0


def test_blocked_signal_leak_chain_over_multiple_ticks():
    random.seed(2401)
    world = create_default_world()
    world.social_nodes["A2"].stress = 90.0
    world.social_edges["CHIEF->A2"].tags.append("informant")

    blocked = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Blocked secret",
        truth_status="true",
        intensity=85.0,
        secrecy=95.0,
        spread=100.0,
    )
    blocked.blocked_by_node_ids.append("CHIEF")

    run_tick(world)
    run_tick(world)

    assert "CHIEF" not in blocked.current_holder_ids
    assert any(signal.signal_type == "leak" and signal.related_signal_id == blocked.id for signal in world.signals.values())
    assert any(clue.related_signal_id == blocked.id for clue in world.clues.values())


def test_leak_clue_confidence_can_escalate_after_audit():
    random.seed(2402)
    world = create_default_world()
    world.social_nodes["A2"].stress = 90.0
    world.social_edges["CHIEF->A2"].tags.append("informant")

    blocked = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Blocked secret",
        truth_status="true",
        intensity=85.0,
        secrecy=95.0,
        spread=100.0,
    )
    blocked.blocked_by_node_ids.append("CHIEF")
    run_tick(world)

    before = max(clue.confidence for clue in world.clues.values() if clue.related_signal_id == blocked.id)
    run_audit(world, "A2")
    after = max(clue.confidence for clue in world.clues.values() if clue.related_trace_id or clue.related_signal_id == blocked.id)

    assert after > before


def test_confirmed_leak_changes_social_edges():
    random.seed(2403)
    world = create_default_world()
    world.social_nodes["A2"].stress = 90.0
    world.social_edges["CHIEF->A2"].tags.append("informant")
    trust_before = world.social_nodes["A2"].report_honesty
    fear_before = world.social_nodes["A2"].fear

    blocked = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Blocked secret",
        truth_status="true",
        intensity=85.0,
        secrecy=95.0,
        spread=100.0,
    )
    blocked.blocked_by_node_ids.append("CHIEF")
    run_tick(world)
    run_audit(world, "A2")

    assert world.social_nodes["A2"].report_honesty < trust_before
    assert world.social_nodes["A2"].fear > fear_before


def test_appointment_centrality_persists_with_resource_flow():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    initial = world.social_nodes["R1"].overall_core_score
    for _ in range(5):
        run_tick(world)
    assert world.social_nodes["R1"].overall_core_score >= initial - 2.0


def test_symbolic_appointment_without_resources_decays():
    from src.models import PositionObject

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
    initial = world.social_nodes["R1"].overall_core_score
    for _ in range(6):
        run_tick(world)
    assert world.social_nodes["R1"].overall_core_score < initial


def test_appointment_updates_neighbor_edges_over_time():
    world = create_default_world()
    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    base_dep = world.get_edge("A4", "R1").dependency
    for _ in range(4):
        run_tick(world)
    assert world.get_edge("A4", "R1").dependency > base_dep


def test_task_pressure_increases_report_distortion_over_time():
    world = create_default_world()
    run_tick(world, [{"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage", "title": "Storage", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "force_task", "task_id": "T1"}])
    task = world.get_task("T1")
    before = task.false_report_risk
    for _ in range(4):
        run_tick(world)
    assert task.false_report_risk > before


def test_progress_mismatch_generates_trace_not_truth_dump():
    world = create_default_world()
    run_tick(world, [{"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage", "title": "Storage", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "force_task", "task_id": "T1"}])
    for _ in range(5):
        run_tick(world)
    task = world.get_task("T1")
    assert task.progress_reported - task.progress_true > 0
    assert any(trace.linked_world_object_id == "T1" for trace in world.traces.values())
    report = generate_status(world)
    assert "progress_true" not in report


def test_confirmed_progress_mismatch_creates_accountability_consequence():
    world = create_default_world()
    run_tick(world, [{"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage", "title": "Storage", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5}])
    run_tick(world, [{"type": "force_task", "task_id": "T1"}])
    for _ in range(5):
        run_tick(world)
    honesty_before = world.social_nodes["A2"].report_honesty
    fear_before = world.social_nodes["A2"].fear
    run_audit(world, "T1")
    assert world.social_nodes["A2"].report_honesty <= honesty_before
    assert world.social_nodes["A2"].fear >= fear_before
    assert any(signal.signal_type == "audit_result" for signal in world.signals.values())


def test_30_tick_mixed_scenario_stability():
    random.seed(2404)
    world = create_default_world()
    actions = [
        [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}],
        [{"type": "promise", "targets": ["A2"], "content": "Promise: storage (deadline tick +3)", "deadline_ticks": 3, "promise_topic": "storage", "linked_fulfillment_targets": ["T1"]}],
        [{"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage", "title": "Storage", "budget": 1000, "materials": 20, "labor": 5}],
        [{"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5}],
        [{"type": "force_task", "task_id": "T1"}],
        [{"type": "audit", "target_id": "T1"}],
    ]
    for tick in range(30):
        if tick < len(actions):
            run_tick(world, actions[tick])
        else:
            run_tick(world)

    assert world.clock.current_tick >= 30
    assert len(world.get_active_signals()) < 120
    assert len(world.traces) < 120
    assert len(world.clues) < 120
    report = generate_status(world)
    debug = generate_debug(world)
    assert "Public Situation" in report and "Suggested Attention" in report
    assert "DEBUG: True State" in debug
