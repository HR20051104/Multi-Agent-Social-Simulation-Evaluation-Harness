import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.models import Clue, ClueStatus, TaskObject, WorldObject
from src.report_engine import generate_status
from src.signal_engine import create_signal
from src.world import create_default_world, run_tick


def test_promise_fulfilled_before_deadline():
    world = create_default_world()
    world.world_objects["OBJ_DONE"] = WorldObject(id="OBJ_DONE", name="Done", status="completed")

    run_tick(
        world,
        [{
            "type": "promise",
            "targets": ["A2"],
            "content": "Promise: repair well (deadline tick +2)",
            "deadline_ticks": 2,
            "promise_topic": "repair well",
            "linked_fulfillment_targets": ["OBJ_DONE"],
        }],
    )
    run_tick(world)

    promise = next(signal for signal in world.signals.values() if signal.signal_type == "promise")
    assert promise.promise_status == "fulfilled"
    assert not any(signal.signal_type == "broken_expectation" for signal in world.signals.values())


def test_promise_partial_fulfillment():
    world = create_default_world()
    world.world_objects["OBJ_PART_1"] = WorldObject(id="OBJ_PART_1", name="Part 1", status="completed")
    world.world_objects["OBJ_PART_2"] = WorldObject(id="OBJ_PART_2", name="Part 2", status="active")

    run_tick(
        world,
        [{
            "type": "promise",
            "targets": ["A2"],
            "content": "Promise: staged repair (deadline tick +1)",
            "deadline_ticks": 1,
            "promise_topic": "staged repair",
            "linked_fulfillment_targets": ["OBJ_PART_1", "OBJ_PART_2"],
        }],
    )
    run_tick(world)
    run_tick(world)

    promise = next(signal for signal in world.signals.values() if signal.signal_type == "promise")
    disappointment = [signal for signal in world.signals.values() if signal.signal_type == "disappointment"]
    assert promise.promise_status == "delayed"
    assert promise.fulfillment_progress == 0.5
    assert disappointment
    assert not any(signal.signal_type == "broken_expectation" for signal in world.signals.values())


def test_promise_broken_only_when_unfulfilled():
    world = create_default_world()

    run_tick(
        world,
        [{
            "type": "promise",
            "targets": ["A2"],
            "content": "Promise: no delivery (deadline tick +1)",
            "deadline_ticks": 1,
            "promise_topic": "no delivery",
            "linked_fulfillment_targets": ["OBJ_NEVER"],
        }],
    )
    run_tick(world)
    run_tick(world)

    promise = next(signal for signal in world.signals.values() if signal.signal_type == "promise")
    broken = [signal for signal in world.signals.values() if signal.signal_type == "broken_expectation"]
    assert promise.promise_status == "broken"
    assert broken


def test_signal_blocked_from_chief():
    random.seed(2301)
    world = create_default_world()
    world.social_edges["A2->CHIEF"].latency = 1

    signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Hidden diversion details",
        truth_status="true",
        intensity=80.0,
        secrecy=90.0,
        spread=100.0,
        decay=1.0,
        tags=["concealment"],
    )
    signal.blocked_by_node_ids.append("CHIEF")

    run_tick(world)
    run_tick(world)

    assert "CHIEF" not in signal.current_holder_ids


def test_blocked_signal_leaks_via_informant():
    random.seed(2302)
    world = create_default_world()
    world.social_nodes["A2"].stress = 90.0
    world.social_edges["CHIEF->A2"].tags.append("informant")

    signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Full hidden diversion details",
        truth_status="true",
        intensity=80.0,
        secrecy=95.0,
        spread=100.0,
        decay=1.0,
        tags=["concealment"],
    )
    signal.blocked_by_node_ids.append("CHIEF")

    run_tick(world)

    assert any(leak.signal_type == "leak" and "CHIEF" in leak.current_holder_ids for leak in world.signals.values())


def test_leak_creates_low_confidence_clue_not_truth_dump():
    random.seed(2303)
    world = create_default_world()
    world.social_nodes["A2"].stress = 90.0
    world.social_edges["CHIEF->A2"].tags.append("informant")

    signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Exact bribe ledger and hidden diversion route",
        truth_status="true",
        intensity=90.0,
        secrecy=95.0,
        spread=100.0,
        decay=1.0,
        tags=["concealment"],
    )
    signal.blocked_by_node_ids.append("CHIEF")

    run_tick(world)

    clue = next(clue for clue in world.clues.values() if clue.related_signal_id == signal.id)
    assert clue.confidence < 40
    assert "Exact bribe ledger" not in clue.content


def test_report_deduplicates_confidence_text():
    world = create_default_world()
    for idx in range(2):
        world.clues[f"CL_CONF_{idx}"] = Clue(
            id=f"CL_CONF_{idx}",
            tick_created=idx,
            source_channel="audit",
            holder_node_id="CHIEF",
            content="confidence 32% confidence 32% suspicious mismatch",
            confidence=32.0,
            status=ClueStatus.UNVERIFIED.value,
        )

    report = generate_status(world)

    assert "confidence 32% confidence 32%" not in report
    assert "confidence confidence" not in report


def test_report_keeps_hidden_truth_out():
    world = create_default_world()
    world.clues["CL_VISIBLE"] = Clue(
        id="CL_VISIBLE",
        tick_created=1,
        source_channel="informant",
        holder_node_id="CHIEF",
        content="Low-confidence hint of concealed report around A2.",
        confidence=25.0,
    )
    hidden_signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Secret exact embezzlement ledger",
        truth_status="true",
        intensity=80.0,
        secrecy=95.0,
    )
    hidden_signal.blocked_by_node_ids.append("CHIEF")

    report = generate_status(world)

    assert "Secret exact embezzlement ledger" not in report
    assert "Low-confidence hint of concealed report around A2." in report
