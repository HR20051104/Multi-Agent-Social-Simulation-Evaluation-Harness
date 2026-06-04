"""Test auto-run: world ticks without player, player can intervene anytime."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.world import create_default_world, run_tick


def test_auto_run():
    """Simulate: world auto-ticks, player intervenes mid-run."""
    w = create_default_world()

    # Phase 1: World runs autonomously for 5 ticks
    print("Phase 1: Auto-run 5 ticks...")
    for i in range(5):
        s = run_tick(w)
        print(f"  T{s['tick']} D{s['day']}: tasks={s['active_tasks']} signals={s['active_signals']}")

    assert w.clock.current_tick == 5
    print(f"  After 5 ticks: day={w.clock.current_day}")

    # Phase 2: Player intervenes — assign a task
    print("\nPhase 2: Player intervenes mid-run...")
    action = {
        "type": "assign_task", "assignee_id": "A2", "task_type": "build_storage",
        "title": "修建仓库", "budget": 1500, "materials": 30, "labor": 8,
    }
    run_tick(w, player_actions=[action])
    tasks = w.get_active_tasks()
    assert len(tasks) == 1
    print(f"  Task created: {tasks[0].id} [{tasks[0].status}]")

    # Phase 3: World keeps running (task blocked, no resources)
    print("\nPhase 3: World keeps running with task...")
    for i in range(5):
        s = run_tick(w)
    task = w.get_active_tasks()[0]
    print(f"  After 5 more ticks: task [{task.status}] progress={task.progress_true:.0f}%")
    print(f"  Total ticks: {w.clock.current_tick}")

    # Phase 4: Player intervenes again — approve resources
    print("\nPhase 4: Player approves resources...")
    action = {"type": "approve_task", "task_id": task.id, "budget": 1500, "materials": 30, "labor": 8}
    run_tick(w, player_actions=[action])
    print(f"  Task [{task.status}] budget={task.reserved_budget}/{task.required_budget}")

    # Phase 5: World finishes the task
    print("\nPhase 5: World auto-completes task...")
    for i in range(10):
        s = run_tick(w)
        task = w.get_active_tasks()
        if not task:
            break
    task = [o for o in w.world_objects.values() if hasattr(o, 'task_type')][0]
    print(f"  Final: [{task.status}] progress={task.progress_true:.0f}%")
    print(f"  Total ticks: {w.clock.current_tick}, signals: {len(w.signals)}, clues: {len(w.clues)}")

    assert w.clock.current_tick > 10, "Should have advanced many ticks"
    print("\nPASS: World runs continuously, player can intervene anytime.")


if __name__ == "__main__":
    test_auto_run()
