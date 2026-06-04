#!/usr/bin/env python3
"""Run all test scenarios for the Rule Mode Text Prototype.

Tests the 4 scenarios from the implementation spec:
  1. Underfunded forced task
  2. Properly funded task
  3. Hidden misuse + audit discovery
  4. Deputy appointment
"""

import sys
import io
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent.parent
PROTO_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROTO_DIR))

from src.world import load_world, export_debug_state, daily_tick
from command_parser import parse_and_execute


DATA_DIR = PROTO_DIR / "data"
INITIAL_WORLD = DATA_DIR / "initial_world.json"


def run_commands(world, commands: list[str], label: str = ""):
    """Run a list of commands and print results."""
    if label:
        print(f"\n{'='*60}")
        print(f"  {label}")
        print(f"{'='*60}")
    for cmd in commands:
        print(f"\nDay {world.day} > {cmd}")
        result = parse_and_execute(world, cmd)
        print(result)
        if result == "__QUIT__":
            break


def scenario_1_underfunded_forced():
    """Scenario 1: Assign task without funding, then force it."""
    print("\n" + "=" * 80)
    print("  SCENARIO 1: Underfunded Forced Construction")
    print("  Expected: Task blocked, A2 stress rises, possible hidden events")
    print("=" * 80)

    world = load_world(INITIAL_WORLD)
    commands = [
        "assign_task A2 build_storage 1000 20 5",
        "force_task T1",
        "status",
        "tasks",
        "next_day",
        "tasks",
        "agents",
        "next_day",
        "tasks",
        "agents",
        "next_day",
        "tasks",
        "agents",
        "events_debug",
        "knowledge",
    ]
    for cmd in commands:
        print(f"\nDay {world.day} > {cmd}")
        result = parse_and_execute(world, cmd)
        print(result)

    export_debug_state(world, DATA_DIR / "debug_scenario_1.json")
    return world


def scenario_2_properly_funded():
    """Scenario 2: Assign task with full funding, normal completion."""
    print("\n" + "=" * 80)
    print("  SCENARIO 2: Properly Funded Task")
    print("  Expected: Task approved, budget frozen, progress advances, A1 stress low")
    print("=" * 80)

    world = load_world(INITIAL_WORLD)
    commands = [
        "assign_task A1 build_storage 1000 20 5",
        "approve_task T1 1000 20 5",
        "status",
        "tasks",
        "next_day",
        "tasks",
        "next_day",
        "tasks",
        "next_day",
        "tasks",
        "next_day",
        "tasks",
        "next_day",
        "tasks",
        "next_day",
        "tasks",
        "status",
        "agents",
    ]
    for cmd in commands:
        print(f"\nDay {world.day} > {cmd}")
        result = parse_and_execute(world, cmd)
        print(result)

    export_debug_state(world, DATA_DIR / "debug_scenario_2.json")
    return world


def scenario_3_hidden_misuse_audit():
    """Scenario 3: Hidden misuse event discovered through audit."""
    print("\n" + "=" * 80)
    print("  SCENARIO 3: Hidden Misuse + Audit Discovery")
    print("  Expected: A2 (greedy) may misuse, audit discovers clues with confidence")
    print("=" * 80)

    world = load_world(INITIAL_WORLD)
    commands = [
        "assign_task A2 build_storage 3000 40 6",
        "approve_task T1 3000 40 6",
        "force_task T1",
        "next_day",
        "next_day",
        "next_day",
        "tasks",
        "events_debug",
        "audit T1",
        "knowledge",
        "next_day",
        "audit T1",
        "knowledge",
        "events_debug",
    ]
    for cmd in commands:
        print(f"\nDay {world.day} > {cmd}")
        result = parse_and_execute(world, cmd)
        print(result)

    export_debug_state(world, DATA_DIR / "debug_scenario_3.json")
    return world


def scenario_4_deputy_appointment():
    """Scenario 4: Appoint a deputy leader for B2."""
    print("\n" + "=" * 80)
    print("  SCENARIO 4: Deputy Appointment")
    print("  Expected: Deputy position created, original leader affected, meeting reflects change")
    print("=" * 80)

    world = load_world(INITIAL_WORLD)
    commands = [
        "positions",
        "appoint_deputy A3 leader_B2",
        "positions",
        "agents",
        "meeting",
        "status",
    ]
    for cmd in commands:
        print(f"\nDay {world.day} > {cmd}")
        result = parse_and_execute(world, cmd)
        print(result)

    export_debug_state(world, DATA_DIR / "debug_scenario_4.json")
    return world


def scenario_5_continuous_10_days():
    """Bonus: Run 10 continuous days to verify stability."""
    print("\n" + "=" * 80)
    print("  SCENARIO 5: 10-Day Continuous Simulation")
    print("  Expected: No crash, world evolves naturally")
    print("=" * 80)

    world = load_world(INITIAL_WORLD)

    # Day 1: Create a task with partial funding
    print("\nDay 1 > assign_task A4 build_storage 1500 30 8")
    print(parse_and_execute(world, "assign_task A4 build_storage 1500 30 8"))
    print("\nDay 1 > approve_task T1 1000 20 5")
    print(parse_and_execute(world, "approve_task T1 1000 20 5"))

    # Run 9 more days
    for i in range(9):
        prev_day = world.day
        summary = daily_tick(world)
        print(f"\n=== Day {prev_day} -> Day {world.day} ===")
        print(f"  Budget: {summary['budget_available']} | Materials: {summary['materials']} | Labor: {summary['labor']}")
        print(f"  Sat: {summary['reported_satisfaction']:.0f} | Order: {summary['public_order']:.0f}")
        print(f"  New hidden events: {summary['new_events']} | New clues: {summary['new_clues']}")
        if summary['tick_log']:
            for msg in summary['tick_log'][:5]:
                print(f"  {msg}")

    print(f"\nDay {world.day} > tasks")
    print(parse_and_execute(world, "tasks"))
    print(f"\nDay {world.day} > events_debug")
    print(parse_and_execute(world, "events_debug"))
    print(f"\nDay {world.day} > knowledge")
    print(parse_and_execute(world, "knowledge"))
    print(f"\nDay {world.day} > status")
    print(parse_and_execute(world, "status"))

    export_debug_state(world, DATA_DIR / "debug_scenario_5.json")
    return world


def main():
    print("=" * 80)
    print("  Community AI Sandbox - Test Suite")
    print("  Running all 5 test scenarios")
    print("=" * 80)

    try:
        scenario_1_underfunded_forced()
    except Exception as e:
        print(f"\n[FAIL] Scenario 1 failed: {e}")
        import traceback
        traceback.print_exc()

    try:
        scenario_2_properly_funded()
    except Exception as e:
        print(f"\n[FAIL] Scenario 2 failed: {e}")
        import traceback
        traceback.print_exc()

    try:
        scenario_3_hidden_misuse_audit()
    except Exception as e:
        print(f"\n[FAIL] Scenario 3 failed: {e}")
        import traceback
        traceback.print_exc()

    try:
        scenario_4_deputy_appointment()
    except Exception as e:
        print(f"\n[FAIL] Scenario 4 failed: {e}")
        import traceback
        traceback.print_exc()

    try:
        scenario_5_continuous_10_days()
    except Exception as e:
        print(f"\n[FAIL] Scenario 5 failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("  Test suite complete.")
    print("=" * 80)


if __name__ == "__main__":
    main()
