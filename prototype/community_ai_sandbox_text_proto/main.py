#!/usr/bin/env python3
"""Community AI Sandbox — Rule Mode Text Prototype v0.1

A command-line text prototype that validates the core game loop:
  Player command → Structured action → Resource/permission checks
  → Task execution → Background event generation
  → Evidence pipeline → Information filtering → Player knowledge

Run: python main.py
"""

import sys
import io
from pathlib import Path

# Fix Windows console encoding for Chinese characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")

# Ensure root src is importable
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.world import load_world, export_debug_state
from command_parser import parse_and_execute


DATA_DIR = Path(__file__).parent / "data"
INITIAL_WORLD = DATA_DIR / "initial_world.json"
DEBUG_STATE = DATA_DIR / "debug_state.json"


def main():
    print("=" * 60)
    print("  Community AI Sandbox — Rule Mode Text Prototype v0.1")
    print("  今日小区例会 · 文本原型")
    print("=" * 60)
    print(f"  加载初始世界: {INITIAL_WORLD}")
    print()

    try:
        world = load_world(INITIAL_WORLD)
    except FileNotFoundError:
        print(f"[ERROR] 找不到初始世界文件: {INITIAL_WORLD}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 加载初始世界失败: {e}")
        sys.exit(1)

    print("  Type 'help' for available commands.")
    print()

    while True:
        try:
            prompt = f"Day {world.day} > "
            cmd = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            break

        if not cmd:
            continue

        result = parse_and_execute(world, cmd)

        if result == "__QUIT__":
            # Save debug state before quitting
            export_debug_state(world, DEBUG_STATE)
            print(f"Debug state saved to {DEBUG_STATE}")
            print("再见。")
            break

        print(result)
        print()


if __name__ == "__main__":
    main()
