import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.models import ChannelType, PositionObject, Trace
from src.signal_engine import create_signal
from src.world import create_default_world, run_tick


def run_cmds(world, cmds: list[dict]) -> None:
    for action in cmds:
        if action["type"] == "tick":
            run_tick(world)
        elif action["type"] == "wait":
            for _ in range(action.get("n", 1)):
                run_tick(world)
        else:
            run_tick(world, player_actions=[action])


def test_scenario_1_direct_social_impact():
    random.seed(2001)
    world = create_default_world()
    before = world.social_nodes["A2"].stress

    run_cmds(world, [{"type": "public_rebuke", "target_id": "A2"}])
    run_cmds(world, [{"type": "tick"}, {"type": "tick"}])

    assert world.social_nodes["A2"].stress > before
    assert world.social_edges["A2->CHIEF"].trust < 55.0


def test_scenario_2_underfunded_forced_task():
    random.seed(2002)
    world = create_default_world()

    run_cmds(world, [
        {"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
        {"type": "force_task", "task_id": "T1"},
    ])
    run_cmds(world, [{"type": "wait", "n": 3}])

    task = world.get_task("T1")
    assert task is not None
    assert task.status == "blocked"
    assert task.linked_trace_ids
    assert any(s.linked_world_object_ids == ["T1"] for s in world.signals.values())


def test_scenario_3_properly_funded_task():
    random.seed(2003)
    world = create_default_world()

    run_cmds(world, [
        {"type": "assign_task", "assignee_id": "A1", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
        {"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5},
    ])
    run_cmds(world, [{"type": "wait", "n": 5}])

    task = world.get_task("T1")
    budget_pool = world.get_resource("budget_pool")
    assert task is not None
    assert task.status in {"in_progress", "completed"}
    assert task.progress_true > 0
    assert budget_pool is not None and (budget_pool.amount_spent > 0 or budget_pool.amount_reserved > 0)


def test_scenario_4_promise_signal():
    random.seed(2004)
    world = create_default_world()

    run_cmds(world, [
        {"type": "promise", "targets": ["G2", "A2"], "content": "承诺4 ticks内修垃圾点"},
    ])

    promise_signals = [s for s in world.signals.values() if s.signal_type == "promise"]
    assert promise_signals

    run_cmds(world, [{"type": "wait", "n": 2}])
    assert any(pk.topic == "signal_promise" for pk in world.player_knowledge.values())


def test_scenario_5_edge_node_centrality_shift():
    random.seed(2005)
    world = create_default_world()
    before = world.social_nodes["R1"].overall_core_score

    if "position_supply_coordinator" not in world.world_objects:
        world.world_objects["position_supply_coordinator"] = PositionObject(
            id="position_supply_coordinator",
            name="物资协调员",
            title="物资协调员",
            permission_tags=["coordinate_supplies", "manage_inventory"],
            scope="whole_community",
            nominal_authority=30.0,
            actual_authority=25.0,
            importance=40.0,
        )

    run_cmds(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    run_cmds(world, [{"type": "tick"}, {"type": "tick"}])

    assert world.social_nodes["R1"].overall_core_score > before


def test_scenario_6_hidden_signal_detection_with_informant():
    random.seed(2006)
    world = create_default_world()

    world.traces["TR_hidden"] = Trace(
        id="TR_hidden",
        tick_created=world.clock.current_tick,
        trace_type="private_meeting_pattern",
        linked_world_object_id="B2",
        location="B2",
        strength=95.0,
        detectable_by=[ChannelType.INFORMANT.value],
    )

    run_cmds(world, [{"type": "plant_informant", "target_id": "A2"}])
    run_cmds(world, [{"type": "wait", "n": 3}])

    assert any(c.source_channel == ChannelType.INFORMANT.value for c in world.clues.values())


def test_scenario_7_world_runs_without_player_input():
    random.seed(2007)
    world = create_default_world()

    run_cmds(world, [
        {"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
    ])
    run_cmds(world, [{"type": "wait", "n": 8}])

    task = world.get_task("T1")
    assert world.clock.current_tick >= 9
    assert task is not None
    assert len(world.signals) > 0
    assert len(world.memories) >= 0
