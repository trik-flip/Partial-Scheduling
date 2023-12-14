from random import seed

import pytest

from partial_scheduling.algorithms.brute_force import brute_force
from partial_scheduling.algorithms.dynamic_programming import (
    dynamic_programming,
    dynamic_programming_with_schedule,
)
from partial_scheduling.algorithms.ilp import ilp
from partial_scheduling.models.job import Job
from partial_scheduling.util import scenario

seed(42)


def optimal(jobs: list[Job], k: int):
    if len(jobs) > 30:
        return ilp(jobs, k)
    return brute_force(jobs, k)


class TestDynamicProgramming:
    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [
            scenario.base1(5),
            scenario.base2(5),
            scenario.base3(5),
            scenario.base4(5),
        ],
    )
    def test_base3out5(jobs: list[Job]) -> None:
        schedule = dynamic_programming(jobs, 3)
        opt = optimal(jobs, 3)
        assert schedule.cost == opt.cost

    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [scenario.random(5) for _ in range(20)]
        + [scenario.random(15) for _ in range(20)]
        + [scenario.random(40) for _ in range(20)],
    )
    def test_random3(jobs: list[Job]) -> None:
        schedule = dynamic_programming(jobs, 3)
        opt = optimal(jobs, 3)
        assert schedule.cost == opt.cost, f"{jobs}"

    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [scenario.random(10) for _ in range(20)]
        + [scenario.random(20) for _ in range(20)]
        + [scenario.random(40) for _ in range(20)],
    )
    def test_random5(jobs: list[Job]) -> None:
        schedule = dynamic_programming(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestDynamicProgrammingWithSchedule:
    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [
            scenario.base1(5),
            scenario.base2(5),
            scenario.base3(5),
            scenario.base4(5),
        ],
    )
    def test_base3out5(jobs: list[Job]) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 3)
        opt = optimal(jobs, 3)
        assert schedule.cost == opt.cost

    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [scenario.random(5) for _ in range(20)]
        + [scenario.random(15) for _ in range(20)]
        + [scenario.random(40) for _ in range(20)],
    )
    def test_random3(jobs: list[Job]) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 3)
        opt = optimal(jobs, 3)
        assert schedule.cost == opt.cost, f"{jobs}"

    @staticmethod
    @pytest.mark.parametrize(
        ("jobs"),
        [scenario.random(10) for _ in range(20)]
        + [scenario.random(20) for _ in range(20)]
        + [scenario.random(40) for _ in range(20)],
    )
    def test_random5(jobs: list[Job]) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost
