import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from prototype_v2.community_ai_sandbox_v2.command_parser import parse_and_execute
from src.centrality_engine import update_all_centralities
from src.cognition_engine import update_player_knowledge
from src.models import ChannelType, Clue, Trace
from src.report_engine import generate_debug, generate_status
from src.signal_engine import create_signal
from src.world import create_default_world, run_tick


def test_appointment_requires_existing_position():
    world = create_default_world()
    before_tick = world.clock.current_tick

    result = parse_and_execute(world, "appoint R1 missing_position")

    assert "missing_position" in result
    assert world.clock.current_tick == before_tick
    assert not any(signal.signal_type == "appointment" for signal in world.signals.values())


def test_supply_coordinator_centrality_shift():
    random.seed(2201)
    world = create_default_world()
    update_all_centralities(world)

    resident = world.social_nodes["R1"]
    before_resource = resident.resource_centrality
    before_access = resident.access_to_chief
    before_core = resident.overall_core_score

    run_tick(world, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    update_all_centralities(world)

    resident = world.social_nodes["R1"]
    position = world.get_position("position_supply_coordinator")
    assert position is not None and position.holder_node_id == "R1"
    assert any(signal.signal_type == "appointment" for signal in world.signals.values())
    assert any(
        disturbance.disturbance_type == "appointment" and "R1" in disturbance.entry_social_node_ids
        for disturbance in world.disturbances.values()
    )
    assert any(
        disturbance.disturbance_type == "funding" and "material_pool" in disturbance.entry_world_object_ids
        for disturbance in world.disturbances.values()
    )
    assert resident.resource_centrality > before_resource
    assert resident.access_to_chief > before_access
    assert resident.overall_core_score > before_core

    a4_to_r1 = world.get_edge("A4", "R1")
    assert a4_to_r1 is not None
    assert a4_to_r1.competition > 0 or a4_to_r1.hostility > 0


def test_promise_deadline_creates_broken_expectation():
    random.seed(2202)
    world = create_default_world()
    trust_before = world.social_edges["A2->CHIEF"].trust

    run_tick(
        world,
        [{
            "type": "promise",
            "targets": ["A2"],
            "content": "承诺: build_garbage_point (deadline tick +1)",
            "deadline_ticks": 1,
            "promise_topic": "build_garbage_point",
        }],
    )
    run_tick(world)
    run_tick(world)

    broken = [signal for signal in world.signals.values() if signal.signal_type == "broken_expectation"]
    assert broken
    assert any(memory.topic == "broken_expectation" and memory.holder_node_id == "A2" and memory.sentiment < 0
               for memory in world.memories.values())
    assert world.social_edges["A2->CHIEF"].trust < trust_before


def test_pending_arrivals_do_not_enter_player_knowledge_until_delivery():
    random.seed(2203)
    world = create_default_world()
    world.social_edges["A2->CHIEF"].latency = 2

    signal = create_signal(
        world,
        "report",
        source_node_id="A2",
        intended_receivers=["CHIEF"],
        content="Delayed report to chief",
        truth_status="true",
        intensity=80.0,
        spread=100.0,
        secrecy=0.0,
        decay=1.0,
    )

    run_tick(world)
    assert "CHIEF" not in signal.current_holder_ids
    update_player_knowledge(world)
    assert not any("Delayed report to chief" in knowledge.summary for knowledge in world.player_knowledge.values())

    debug = generate_debug(world)
    assert "pending=[" in debug
    assert "CHIEF@" in debug
    assert "spread=" in debug and "decay=" in debug and "blocked_by=" in debug

    run_tick(world)
    run_tick(world)
    update_player_knowledge(world)
    assert any("Delayed report to chief" in knowledge.summary for knowledge in world.player_knowledge.values())


def test_report_deduplicates_repeated_clues():
    world = create_default_world()
    world.traces["TR_DUP"] = Trace(
        id="TR_DUP",
        tick_created=1,
        trace_type="schedule_delay",
        linked_world_object_id="T1",
        detectable_by=[ChannelType.AUDIT.value],
    )
    for idx in range(3):
        world.clues[f"CL_DUP_{idx}"] = Clue(
            id=f"CL_DUP_{idx}",
            tick_created=1 + idx,
            source_channel=ChannelType.AUDIT.value,
            holder_node_id="CHIEF",
            related_trace_id="TR_DUP",
            content="Repeated weak delay clue",
            confidence=25.0 + idx,
        )

    report = generate_status(world)

    assert report.count("Repeated weak delay clue") == 1
    assert "merged 3 similar clues" in report
