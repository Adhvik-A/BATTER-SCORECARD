from pydantic import BaseModel, Field


class BallEvent(BaseModel):
    shot: str
    bat_runs: int = Field(ge=0, le=6)
    is_legal: bool = True


class HistoricalShot(BaseModel):
    shot: str
    runs: int


class ShotEntry(BaseModel):
    shot: str
    runs: int
    angle: float


class Zone(BaseModel):
    name: str
    strength: int


class BatterState(BaseModel):
    name: str
    runs: int = 0
    balls: int = 0
    fours: int = 0
    sixes: int = 0
    strike_rate: float = 0.0
    wagon_wheel: list[ShotEntry] = []
    strong_zones: list[Zone] = []