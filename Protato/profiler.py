import functools
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from .meta import Singleton, TimerException
from .timer import Timer
from .util import format_time

T = TypeVar("T")
RT = TypeVar("RT")
P = ParamSpec("P")


class Profiler(metaclass=Singleton):
    _timers: dict[str, Timer]
    _disabled: bool

    def clean(self) -> None:
        del self._timers
        self._timers = dict()

    def __init__(self) -> None:
        self._timers = dict()
        self._disabled = False

    def disable(self) -> None:
        self._disabled = True

    def __getitem__(self, name: str) -> Timer:
        return self._timers[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self._timers[name] = value

    def __contains__(self, item: str) -> bool:
        return item in self._timers

    def __call__(self, func: Callable[P, RT]) -> Callable[P, RT]:
        return self.profile(func)

    def switch(self, name1: str, name2: str) -> None:
        self.stop(name1)
        self.start(name2)

    def start(self, name: str) -> None:
        if self._disabled:
            return
        if name not in self:
            self[name] = Timer()
        self[name].start()

    def stop(self, name: str) -> None:
        if self._disabled:
            return
        if name not in self:
            raise TimerException(f"{name} is not a valid timer")
        self[name].stop()

    def hit(self, name: str) -> None:
        if self._disabled:
            return
        if name not in self:
            self[name] = Timer()
        self[name].hit()

    def profile(self, func: Callable[P, RT]) -> Callable[P, RT]:
        name = f"Function:{func.__name__}"
        self[name] = Timer()

        @functools.wraps(func)
        def new_func(*args: P, **kwargs: P) -> RT:
            self.start(name)
            result = func(*args, **kwargs)
            self.stop(name)
            return result

        return new_func

    def result(self) -> list[tuple[str, Timer]]:
        return sorted(self._timers.items(), key=lambda x: x[1].total_time, reverse=True)

    def show(self, zero_runners: bool = True, min_time: int = 0) -> None:
        print("\n", "=" * 100, "\n")
        self._print_manual_timers(zero_runners, min_time)
        print("\n", "=" * 100, "\n")

    def _print_manual_timers(self, zero_runners: bool, min_time: int) -> None:
        if len(self._timers) == 0:
            return
        longest_key = max(len(str(k)) for k in self._timers)
        print(
            f"[Timer]{' '*(longest_key-7)}\t|\t[time]  \t|\t[hit counts]\t|\t[time per call]"
        )
        for timer_name, timer in sorted(
            self._timers.items(), key=lambda x: x[1].total_time, reverse=True
        ):
            ftt = format_time(timer.total_time)

            if not zero_runners and timer.hits == 0:
                continue

            tpc = timer.time_per_call or "N/A"
            if min_time != 0 and (
                timer.hits == 0 or (timer.time_per_call or 0) < min_time
            ):
                continue
            if not isinstance(tpc, str):
                tpc = format_time(tpc)
            print(
                f"{timer_name:{max(longest_key,7)}}\t|\t{ftt:8}\t|\t{timer.hits:12}\t|\t{tpc}"
            )
