"""Test background ticks + foreground commands with lock."""
import sys, threading, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.world import create_default_world, run_tick
from command_parser import parse_and_execute

lock = threading.Lock()

def bg_ticks(world, stop, n):
    count = 0
    while not stop.is_set() and count < n:
        with lock:
            run_tick(world)
        count += 1
        time.sleep(0.1)

w = create_default_world()
stop = threading.Event()

# Start background
t = threading.Thread(target=bg_ticks, args=(w, stop, 20), daemon=True)
t.start()

# Simulate user commands mid-run
time.sleep(0.5)  # let a few ticks pass

with lock:
    print(parse_and_execute(w, "status"))

time.sleep(0.5)

with lock:
    print(parse_and_execute(w, "assign_task A2 build_storage 1000 20 5"))

time.sleep(0.5)

with lock:
    print(parse_and_execute(w, "tasks"))

time.sleep(1.0)

with lock:
    print(parse_and_execute(w, "nodes"))

stop.set()
t.join(timeout=2)

print(f"\nFinal: tick={w.clock.current_tick} day={w.clock.current_day} tasks={len(w.get_active_tasks())} signals={len(w.get_active_signals())}")
print("PASS: Background ticks + foreground commands work with lock.")
