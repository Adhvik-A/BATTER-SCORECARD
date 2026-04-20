from fastapi import FastAPI
from schemas import BatterState, BallEvent, HistoricalShot
from services import update_batter

app = FastAPI(title="Final Cricket Batter Analytics API")


@app.post("/ball", response_model=BatterState)
def ball_event(
    state: BatterState,
    event: BallEvent,
    history: list[HistoricalShot] = []
):
    """
    FINAL API:
    - ball-by-ball updates
    - wagon wheel auto generation
    - strong zones from historical boundary shots
    - strike rate computed internally
    """
    return update_batter(state, event, history)