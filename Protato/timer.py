from time import perf_counter_ns


class Timer:
    _stops: list[float]
    _starts: list[float]
    hits: int

    @property
    def total_time(self) -> float:
        return sum(self._stops) - sum(self._starts)

    @property
    def running(self) -> bool:
        return len(self._starts) != self.hits

    @property
    def time_per_call(self) -> None | float:
        if self.hits == 0:
            return None
        return self.total_time / self.hits

    def __init__(self) -> None:
        self._stops = []
        self._starts = []
        self.hits = 0

    def __repr__(self) -> str:
        return f"hits:{self.hits}, total:{self.total_time}, tpc:{self.time_per_call}"

    def start(self) -> None:
        self._starts.append(perf_counter_ns())

    def stop(self) -> None:
        self._stops.append(perf_counter_ns())
        self.hits += 1

    def hit(self) -> None:
        self.hits += 1
