from random import seed

import pytest

from partial_scheduling.algorithms.greedy import (
    greedy1,
    greedy1_1,
    greedy2,
    greedy2_1,
    greedy2_graph,
    greedy2_list,
    greedy2_prefer_short,
    greedy3,
    greedy3_1,
)
from partial_scheduling.algorithms.ilp import ilp
from partial_scheduling.models.job import Job
from partial_scheduling.util import scenario

seed(42)
optimal = ilp


class TestGreedy1:
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
        schedule = greedy1(jobs, 3)
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
        schedule = greedy1(jobs, 3)
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
        schedule = greedy1(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy1_1:
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
        schedule = greedy1_1(jobs, 3)
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
        schedule = greedy1_1(jobs, 3)
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
        schedule = greedy1_1(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy2:
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
        schedule = greedy2(jobs, 3)
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
        schedule = greedy2(jobs, 3)
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
        schedule = greedy2(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy2_1:
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
        schedule = greedy2_1(jobs, 3)
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
        schedule = greedy2_1(jobs, 3)
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
        schedule = greedy2_1(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy2_graph:
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
        schedule = greedy2_graph(jobs, 3)
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
        schedule = greedy2_graph(jobs, 3)
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
        schedule = greedy2_graph(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy2_list:
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
        schedule = greedy2_list(jobs, 3)
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
        schedule = greedy2_list(jobs, 3)
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
        schedule = greedy2_list(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy2_prefer_short:
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
        schedule = greedy2_prefer_short(jobs, 3)
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
        schedule = greedy2_prefer_short(jobs, 3)
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
        schedule = greedy2_prefer_short(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy3:
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
        schedule = greedy3(jobs, 3)
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
        schedule = greedy3(jobs, 3)
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
        schedule = greedy3(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost


class TestGreedy3_1:
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
        schedule = greedy3_1(jobs, 3)
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
        schedule = greedy3_1(jobs, 3)
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
        schedule = greedy3_1(jobs, 5)
        opt = optimal(jobs, 5)
        assert schedule.cost == opt.cost
