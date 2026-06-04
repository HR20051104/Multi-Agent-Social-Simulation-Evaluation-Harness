"""World Clock — continuous time and tick coordination.

The clock runs regardless of player input. It orchestrates the full
tick pipeline: disturbances → signals → tasks → events → traces →
clues → memories → centralities → cognition → report.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from .models import (
    WorldClock, WorldState, clamp,
)

if TYPE_CHECKING:
    pass


def create_clock(ticks_per_day: int = 2) -> WorldClock:
    return WorldClock(ticks_per_day=ticks_per_day)


def advance_clock(clock: WorldClock) -> bool:
    """Advance the clock by one tick. Returns True if a new day started."""
    was_day = clock.current_day
    clock.advance()
    return clock.current_day > was_day


def wait_ticks(world: WorldState, n: int) -> list[dict]:
    """Advance world by n ticks without player input.

    Returns list of daily summaries for each day that passed.
    """
    from .world import run_tick

    summaries = []
    for _ in range(n):
        summary = run_tick(world, player_actions=[])
        summaries.append(summary)
    return summaries
