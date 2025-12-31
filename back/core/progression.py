from datetime import datetime, timedelta, timezone

def xp_to_next_level(level: int) -> int:
    return 100 * level * level


def calculate_xp(base_xp, streak):
    bonus = min(streak * 0.1, 1.0)
    return int(base_xp * (1 + bonus))


def calculate_level_and_xp(total_xp: int):
    level = 1
    remaining_xp = total_xp

    while remaining_xp >= xp_to_next_level(level):
        remaining_xp -= xp_to_next_level(level)
        level += 1

    return level, remaining_xp


def can_complete_task(task):
    if not task.last_completed_at:
        return True

    now = datetime.now(timezone.utc)

    if task.frequency == "daily":
        return now >= task.last_completed_at + timedelta(days=1)

    if task.frequency == "weekly":
        return now >= task.last_completed_at + timedelta(days=7)

    return True