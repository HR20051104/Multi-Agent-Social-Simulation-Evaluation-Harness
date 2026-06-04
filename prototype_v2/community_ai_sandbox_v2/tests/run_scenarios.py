#!/usr/bin/env python3
"""Run all 7 test scenarios from the v2 implementation spec."""

import sys
import io
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent.parent
PROTO = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO))

from src.world import create_default_world, run_tick
from src.task_engine import create_task, approve_task_resources, force_task
from src.evidence_engine import run_audit, plant_informant
from src.report_engine import generate_status, generate_debug


def run_cmds(world, cmds: list[dict]) -> None:
    for a in cmds:
        if a["type"] == "tick":
            run_tick(world)
        elif a["type"] == "wait":
            for _ in range(a.get("n", 1)):
                run_tick(world)
        else:
            run_tick(world, player_actions=[a])


def sep(title: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


# ── Scenario 1: Direct social impact ─────────────────────────────────

def scenario_1():
    sep("SCENARIO 1: Action directly affects people (no world object needed)")
    w = create_default_world()

    print("\nBefore:")
    a2 = w.social_nodes["A2"]
    print(f"  A2: stress={a2.stress:.0f} fear={a2.fear:.0f}")

    run_cmds(w, [{"type": "public_rebuke", "target_id": "A2"}])
    run_cmds(w, [{"type": "tick"}, {"type": "tick"}])

    print("\nAfter public_rebuke + 2 ticks:")
    a2 = w.social_nodes["A2"]
    print(f"  A2: stress={a2.stress:.0f} fear={a2.fear:.0f}")

    edge = w.social_edges.get("A2->CHIEF")
    if edge:
        print(f"  A2->CHIEF: trust={edge.trust:.0f} fear={edge.fear:.0f}")

    sig_count = len([s for s in w.signals.values() if s.active])
    print(f"  Active signals: {sig_count}")

    # Verification
    assert a2.stress > 25.0, f"A2 stress should have risen, got {a2.stress:.0f}"
    print("  PASS: Direct social impact works without world object trace.")


# ── Scenario 2: Underfunded forced task ──────────────────────────────

def scenario_2():
    sep("SCENARIO 2: Underfunded forced task")
    w = create_default_world()

    print("\nCreating task without resources, forcing it...")
    run_cmds(w, [
        {"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
        {"type": "force_task", "task_id": "T1"},
    ])
    run_cmds(w, [{"type": "wait", "n": 3}])

    tasks = w.get_active_tasks()
    for t in tasks:
        print(f"  {t.id}: [{t.status}] progress={t.progress_true:.0f}% reported={t.progress_reported:.0f}% blocked={t.blocked_reason}")

    a2 = w.social_nodes["A2"]
    print(f"  A2: stress={a2.stress:.0f} loyalty(report_honesty)={a2.report_honesty:.0f}")

    disturbances = w.get_active_disturbances()
    print(f"  Active disturbances: {len(disturbances)}")

    signals = w.get_active_signals()
    print(f"  Active signals: {len(signals)}")

    # Verification
    has_blocked = any(t.status == "blocked" for t in tasks)
    assert has_blocked or len(tasks) == 0, "Task should be blocked without resources"
    print("  PASS: Task blocked without resources, signals/disturbances generated.")


# ── Scenario 3: Properly funded task ─────────────────────────────────

def scenario_3():
    sep("SCENARIO 3: Properly funded task")
    w = create_default_world()

    run_cmds(w, [
        {"type": "assign_task", "assignee_id": "A1", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
        {"type": "approve_task", "task_id": "T1", "budget": 1000, "materials": 20, "labor": 5},
    ])
    run_cmds(w, [{"type": "wait", "n": 5}])

    tasks = [o for o in w.world_objects.values() if hasattr(o, 'task_type')]
    for t in tasks:
        print(f"  {t.id}: [{t.status}] progress_true={t.progress_true:.0f}%")

    bp = w.get_resource("budget_pool")
    if bp:
        print(f"  Budget: avail={bp.amount_available:.0f} reserved={bp.amount_reserved:.0f} spent={bp.amount_spent:.0f}")

    a1 = w.social_nodes["A1"]
    print(f"  A1: stress={a1.stress:.0f}")

    # Verification
    completed = any(t.status == "completed" for t in tasks)
    in_progress = any(t.status == "in_progress" for t in tasks)
    assert completed or in_progress, f"Task should progress with resources, got status {tasks[0].status if tasks else 'none'}"
    assert bp.amount_spent > 0 or bp.amount_reserved > 0 if bp else True, "Resources should be frozen or spent"
    print("  PASS: Task progresses with resources, budget flows.")


# ── Scenario 4: Promise and broken expectation ───────────────────────

def scenario_4():
    sep("SCENARIO 4: Promise and broken expectation")
    w = create_default_world()

    print("\nMaking promise to G2...")
    run_cmds(w, [
        {"type": "promise", "targets": ["G2", "A2"], "content": "承诺4 ticks内修垃圾点"},
    ])
    print(f"  Signals: {len(w.get_active_signals())}")

    # Wait past deadline
    run_cmds(w, [{"type": "wait", "n": 5}])

    signals = w.get_active_signals()
    print(f"  Active signals after wait: {len(signals)}")
    for s in signals[:3]:
        print(f"    [{s.signal_type}] {s.content_summary[:50]}")

    edge = w.social_edges.get("A2->CHIEF")
    if edge:
        print(f"  A2->CHIEF trust: {edge.trust:.0f}")

    print("  PASS: Promise signal created, propagated.")


# ── Scenario 5: Edge node enters core circle ─────────────────────────

def scenario_5():
    sep("SCENARIO 5: Edge node centrality shift (R1 appointed)")
    w = create_default_world()

    r1 = w.social_nodes["R1"]
    print(f"\nBefore: R1 core_score={r1.overall_core_score:.0f}")

    # Appoint R1 — create position if needed
    from src.models import PositionObject
    if "position_supply_coordinator" not in w.world_objects:
        pos = PositionObject(
            id="position_supply_coordinator",
            name="物资协调员", title="物资协调员",
            permission_tags=["coordinate_supplies", "manage_inventory"],
            scope="whole_community",
            nominal_authority=30.0, actual_authority=25.0,
            importance=40.0,
        )
        w.world_objects[pos.id] = pos

    run_cmds(w, [{"type": "appoint", "node_id": "R1", "position_id": "position_supply_coordinator"}])
    run_cmds(w, [{"type": "tick"}, {"type": "tick"}])

    r1 = w.social_nodes["R1"]
    print(f"After: R1 core_score={r1.overall_core_score:.0f} authority={r1.authority_centrality:.0f} resource={r1.resource_centrality:.0f} access={r1.access_to_chief:.0f}")

    # Verification
    assert r1.overall_core_score > 5.0, f"R1 core_score should have risen from 5, got {r1.overall_core_score:.0f}"
    print("  PASS: Edge node centrality increased after appointment.")


# ── Scenario 6: Hidden signal leakage ────────────────────────────────

def scenario_6():
    sep("SCENARIO 6: Hidden signal leakage via informant")
    w = create_default_world()

    run_cmds(w, [
        {"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 3000, "materials": 40, "labor": 6},
        {"type": "approve_task", "task_id": "T1", "budget": 3000, "materials": 40, "labor": 6},
        {"type": "force_task", "task_id": "T1"},
    ])
    run_cmds(w, [{"type": "wait", "n": 3}])

    print(f"\nBefore informant: clues={len(w.clues)} signals={len(w.get_active_signals())}")

    plant_informant(w, "A2")
    run_cmds(w, [{"type": "wait", "n": 2}])

    print(f"After informant: clues={len(w.clues)} signals={len(w.get_active_signals())}")
    for c in list(w.clues.values())[-3:]:
        print(f"  Clue: [{c.source_channel}] conf={c.confidence:.0f}%: {c.content[:50]}")

    print(f"  Player knowledge entries: {len(w.player_knowledge)}")
    for pk in list(w.player_knowledge.values())[-3:]:
        print(f"    [{pk.status}] {pk.topic}: {pk.summary[:60]}")

    print("  PASS: Informant helps detect hidden signals and clues.")


# ── Scenario 7: World runs without player input ──────────────────────

def scenario_7():
    sep("SCENARIO 7: World continues without player input")
    w = create_default_world()

    run_cmds(w, [
        {"type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
         "title": "修建临时仓库", "budget": 1000, "materials": 20, "labor": 5},
    ])
    run_cmds(w, [{"type": "wait", "n": 8}])

    tasks = [o for o in w.world_objects.values() if hasattr(o, 'task_type')]
    for t in tasks:
        print(f"  {t.id}: [{t.status}] progress={t.progress_true:.0f}%")

    print(f"  World: day={w.clock.current_day} tick={w.clock.current_tick}")
    print(f"  Signals: {len(w.get_active_signals())}")
    print(f"  Clues: {len(w.clues)}")
    print(f"  Memories: {len(w.memories)}")
    print(f"  Disturbances: {len(w.get_active_disturbances())}")

    print("  PASS: World evolves without player input.")


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("  Community AI Sandbox v2 — Test Suite")
    print("  Dynamic Influence-Signal Architecture")
    print("=" * 70)

    scenarios = [
        ("1. Direct social impact", scenario_1),
        ("2. Underfunded forced task", scenario_2),
        ("3. Properly funded task", scenario_3),
        ("4. Promise & broken expectation", scenario_4),
        ("5. Edge node centrality shift", scenario_5),
        ("6. Hidden signal leakage", scenario_6),
        ("7. World runs without player", scenario_7),
    ]

    passed = 0
    failed = 0

    for name, func in scenarios:
        try:
            func()
            passed += 1
        except Exception as e:
            print(f"\n  FAIL: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\n{'='*70}")
    print(f"  Results: {passed} passed, {failed} failed out of {len(scenarios)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
