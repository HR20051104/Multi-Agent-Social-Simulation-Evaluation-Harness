#!/usr/bin/env python3
"""Community AI Sandbox — Rule Mode v2 Prototype.

Dynamic Influence-Signal Three-Layer Architecture.

The world runs silently in the background. Type commands anytime.
"""

import sys
import io
import time
import threading
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.world import create_default_world, run_tick, export_debug
from command_parser import parse_and_execute


BANNER = """============================================================
  Community AI Sandbox v2
  世界在后台持续运转。输入命令介入。
  help 查看命令 | quit 退出
============================================================"""


_world_lock = threading.Lock()


def _background_ticks(world, interval: float, stop_event: threading.Event):
    """Run ticks continuously in the background."""
    while not stop_event.is_set():
        with _world_lock:
            run_tick(world)
        time.sleep(interval)


def main():
    print(BANNER, flush=True)

    world = create_default_world()
    print(f"节点:{len(world.social_nodes)} 边:{len(world.social_edges)} 对象:{len(world.world_objects)}", flush=True)
    print(flush=True)

    # Start background tick thread
    stop_event = threading.Event()
    tick_thread = threading.Thread(
        target=_background_ticks,
        args=(world, 1.0, stop_event),
        daemon=True,
    )
    tick_thread.start()

    try:
        while True:
            try:
                cmd = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n再见。", flush=True)
                break

            if not cmd:
                continue

            if cmd.lower() == "quit":
                stop_event.set()
                export_debug(world, Path(__file__).parent / "data" / "debug_state.json")
                print("再见。", flush=True)
                break

            with _world_lock:
                result = parse_and_execute(world, cmd)
                if result == "__QUIT__":
                    stop_event.set()
                    export_debug(world, Path(__file__).parent / "data" / "debug_state.json")
                    print("再见。", flush=True)
                    break

            print(result, flush=True)
            print(flush=True)
    finally:
        stop_event.set()


if __name__ == "__main__":
    main()
