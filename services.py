from collections import defaultdict
from schemas import BatterState, BallEvent, HistoricalShot, ShotEntry, Zone


SHOT_MAP = {
    "cover_drive": 30,
    "straight_drive": 90,
    "on_drive": 120,
    "square_cut": 0,
    "pull_shot": 200,
    "hook_shot": 240,
    "sweep": 270,
    "lofted_drive": 80,
    "flick": 150
}


# -----------------------------
# Strike Rate Calculation
# -----------------------------
def calculate_strike_rate(runs: int, balls: int) -> float:
    if balls == 0:
        return 0.0
    return round((runs / balls) * 100, 2)


# -----------------------------
# Shot Angle → Zone Mapping
# -----------------------------
def get_zone(angle: float) -> str:
    if 0 <= angle < 60:
        return "off_side"
    elif 60 <= angle < 140:
        return "straight"
    elif 140 <= angle < 220:
        return "leg_side"
    else:
        return "fine_leg"


# -----------------------------
# Strong Zones from History
# -----------------------------
def compute_strong_zones(history: list[HistoricalShot]) -> list[Zone]:
    zone_count = defaultdict(int)

    for h in history:
        angle = SHOT_MAP.get(h.shot, 0)
        zone = get_zone(angle)

        if h.runs >= 4:
            zone_count[zone] += 1

    return [
        Zone(name=z, strength=c)
        for z, c in sorted(zone_count.items(), key=lambda x: -x[1])
    ]


# -----------------------------
# Main Update Function
# -----------------------------
def update_batter(
    state: BatterState,
    event: BallEvent,
    history: list[HistoricalShot]
) -> BatterState:

    # 🏏 Runs update
    state.runs += event.bat_runs

    # Boundaries
    if event.bat_runs == 4:
        state.fours += 1
    elif event.bat_runs == 6:
        state.sixes += 1

    # Balls only for legal delivery
    if event.is_legal:
        state.balls += 1

    # 🎯 Wagon wheel update
    angle = SHOT_MAP.get(event.shot, 0)

    if event.bat_runs > 0:
        state.wagon_wheel.append(
            ShotEntry(
                shot=event.shot,
                runs=event.bat_runs,
                angle=angle
            )
        )

    # 📊 Strike rate (computed internally)
    state.strike_rate = calculate_strike_rate(state.runs, state.balls)

    # 🧠 Strong zones (from history only)
    state.strong_zones = compute_strong_zones(history)

    return state