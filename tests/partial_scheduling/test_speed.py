from random import seed

import pytest

from partial_scheduling.algorithms.brute_force import brute_force
from partial_scheduling.algorithms.dynamic_programming import (
    dynamic_programming,
    dynamic_programming_with_schedule,
)
from partial_scheduling.algorithms.greedy import (
    greedy1,
    greedy1_1,
    greedy2,
    greedy2_graph,
    greedy3,
    greedy3_1,
)
from partial_scheduling.algorithms.ilp import ilp
from partial_scheduling.models.job import Job
from partial_scheduling.util import scenario


@pytest.mark.parametrize(
    ("jobs", "cost"),
    [
        (scenario.base1(5), 10),
        (scenario.base2(5), 25),
        (scenario.base3(5), 25),
        (scenario.base4(5), 25),
    ],
)
class TestBase3out5:
    @staticmethod
    def test_greedy1(jobs: set[Job], cost: int) -> None:
        schedule = greedy1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy1_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy1_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy2(jobs: set[Job], cost: int) -> None:
        schedule = greedy2(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3(jobs: set[Job], cost: int) -> None:
        schedule = greedy3(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy3_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_bf(jobs: set[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_ilp(jobs: set[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost, f"{schedule} {cost}"


seed(42)


@pytest.mark.parametrize(
    ("jobs", "cost"),
    [
        (scenario.random(5), 15),
        (scenario.random(5), 13),
        (scenario.random(5), 29),
        (scenario.random(5), 15),
        (scenario.random(5), 18),
        (scenario.random(5), 11),
        (scenario.random(5), 23),
        (scenario.random(5), 32),
        (scenario.random(5), 15),
        (scenario.random(5), 36),
        (scenario.random(5), 50),
        (scenario.random(5), 14),
        (scenario.random(5), 29),
    ],
)
class TestRandom3out5:
    @staticmethod
    def test_greedy1(jobs: set[Job], cost: int) -> None:
        schedule = greedy1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy1_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy1_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy2(jobs: set[Job], cost: int) -> None:
        schedule = greedy2(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3(jobs: set[Job], cost: int) -> None:
        schedule = greedy3(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy3_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_bf(jobs: set[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp2(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_ilp(jobs: set[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost


@pytest.mark.parametrize(
    ("jobs", "cost"),
    [
        (scenario.random(40), 62),
        (scenario.random(40), 93),
        (scenario.random(40), 68),
        (scenario.random(40), 110),
        (scenario.random(40), 42),
        (scenario.random(40), 218),
        (scenario.random(40), 93),
        (scenario.random(40), 77),
        (scenario.random(40), 133),
        (scenario.random(40), 121),
        (scenario.random(40), 113),
        (scenario.random(40), 160),
        (scenario.random(40), 108),
        (scenario.random(40), 54),
        (scenario.random(40), 65),
        (scenario.random(40), 74),
        (scenario.random(40), 57),
        (scenario.random(40), 155),
        (scenario.random(40), 189),
        (scenario.random(40), 106),
        (scenario.random(40), 118),
        (scenario.random(40), 171),
        (scenario.random(40), 132),
        (scenario.random(40), 78),
        (scenario.random(40), 51),
        (scenario.random(40), 222),
        (scenario.random(40), 74),
        (scenario.random(40), 65),
    ],
)
class TestRandom3out40:
    @staticmethod
    def test_greedy2(jobs: set[Job], cost: int) -> None:
        schedule = greedy2(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy2graph(jobs: set[Job], cost: int) -> None:
        schedule = greedy2_graph(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3(jobs: set[Job], cost: int) -> None:
        schedule = greedy3(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy3_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_bf(jobs: set[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp2(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_ilp(jobs: set[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost, f"{schedule} {cost}"


@pytest.mark.parametrize(
    ("jobs", "cost"),
    [
        (scenario.case2(40), 200),
    ],
)
class TestCase2:
    @staticmethod
    def test_greedy2(jobs: set[Job], cost: int) -> None:
        schedule = greedy2(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy2graph(jobs: set[Job], cost: int) -> None:
        schedule = greedy2_graph(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3(jobs: set[Job], cost: int) -> None:
        schedule = greedy3(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3_1(jobs: set[Job], cost: int) -> None:
        schedule = greedy3_1(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_bf(jobs: set[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_dp2(jobs: set[Job], cost: int) -> None:
        schedule = dynamic_programming_with_schedule(jobs, 3)
        assert schedule.cost == cost

    @staticmethod
    def test_ilp(jobs: set[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost


@pytest.mark.parametrize(
    ("jobs", "cost", "k"),
    # [(*scenario.problem_case1(n), 2 for n in range(3, 15)]
    # +
    [(*scenario.problem_case2(k), k) for k in range(3, 10)],
)
class TestProblems:
    @staticmethod
    def test_greedy2(jobs: set[Job], cost: float, k: int) -> None:
        schedule = greedy2(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy2graph(jobs: set[Job], cost: float, k: int) -> None:
        schedule = greedy2_graph(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3(jobs: set[Job], cost: float, k: int) -> None:
        schedule = greedy3(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_greedy3_1(jobs: set[Job], cost: float, k: int) -> None:
        schedule = greedy3_1(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_dp(jobs: set[Job], cost: float, k: int) -> None:
        schedule = dynamic_programming(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_bf(jobs: set[Job], cost: float, k: int) -> None:
        schedule = brute_force(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_dp2(jobs: set[Job], cost: float, k: int) -> None:
        schedule = dynamic_programming_with_schedule(jobs, k)
        assert schedule.cost == cost

    @staticmethod
    def test_ilp(jobs: set[Job], cost: float, k: int) -> None:
        schedule = ilp(jobs, k)
        assert schedule.cost == cost
