from random import seed

import pytest

from partial_scheduling.algorithms.brute_force import brute_force, brute_force_all
from partial_scheduling.algorithms.ilp import ilp
from partial_scheduling.models.job import Job
from partial_scheduling.util import scenario

seed(42)


class TestBruteForce:
    @staticmethod
    @pytest.mark.parametrize(
        ("jobs", "cost"),
        [
            (scenario.base1(5), 10),
            (scenario.base2(5), 25),
            (scenario.base3(5), 25),
            (scenario.base4(5), 25),
        ],
    )
    def test_base3out5(jobs: list[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost, f"{jobs}"

    @staticmethod
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
    def test_random5(jobs: list[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost, f"{jobs}"

    @staticmethod
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
    def test_random40(jobs: list[Job], cost: int) -> None:
        schedule = brute_force(jobs, 3)
        assert schedule.cost == cost


seed(42)


class TestBruteForceAll:
    @staticmethod
    @pytest.mark.parametrize(
        ("jobs", "cost"),
        [
            (scenario.base1(5), 10),
            (scenario.base2(5), 25),
            (scenario.base3(5), 25),
            (scenario.base4(5), 25),
        ],
    )
    def test_base3out5(jobs: list[Job], cost: int) -> None:
        schedules = brute_force_all(jobs, 3)
        for schedule in schedules:
            assert schedule.cost == cost

    @staticmethod
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
    def test_random5(jobs: list[Job], cost: int) -> None:
        schedules = brute_force_all(jobs, 3)
        for schedule in schedules:
            assert schedule.cost == cost

    @staticmethod
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
    def test_random40(jobs: list[Job], cost: int) -> None:
        schedules = brute_force_all(jobs, 3)
        for schedule in schedules:
            assert schedule.cost == cost


seed(42)


class TestILP:
    @staticmethod
    @pytest.mark.parametrize(
        ("jobs", "cost"),
        [
            (scenario.base1(5), 10),
            (scenario.base2(5), 25),
            (scenario.base3(5), 25),
            (scenario.base4(5), 25),
        ],
    )
    def test_base3out5(jobs: list[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost, f"{jobs}"

    @staticmethod
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
    def test_random5(jobs: list[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost, f"{jobs}"

    @staticmethod
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
    def test_random40(jobs: list[Job], cost: int) -> None:
        schedule = ilp(jobs, 3)
        assert schedule.cost == cost
