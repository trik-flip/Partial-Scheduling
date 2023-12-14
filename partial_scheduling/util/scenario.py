from random import randint

from ..models.job import Job, ratio


def problem_case1(cost_of_jobs: int = 3) -> tuple[list[Job], float]:
    assert (
        cost_of_jobs > 2
    ), "This is not a problem case when number_of_jobs is equal to or smaller than 2"
    return (
        [
            Job(1, (cost_of_jobs**2) + 1),
            Job(cost_of_jobs, cost_of_jobs),
            Job((cost_of_jobs**2) + 1, 1),
        ],
        2 * cost_of_jobs**2 + 3,
    )


def problem_case2(k: int = 3) -> tuple[list[Job], float]:
    """Generate the problem case for greedy2, from the thesis

    Args:
        k (int, optional): The number of jobs to choose. Defaults to 3.

    Returns:
        tuple[list[Job], float]: a list with all the jobs and the cost of the optimal schedule
    """
    assert k > 1
    delta = (6 ** (1 / 2)) - 2
    error = 1e-10
    jobs: list[Job] = []
    # 1 to k-2
    for _ in range(k - 2):
        jobs.append(Job(error**2, error))
    # k-1
    jobs.append(Job(delta, 1 / delta))
    # k
    jobs.append(Job(1, 1 - (k - 2) * (1 - delta) * error**2))
    # k+1
    jobs.append(Job(1 / delta, delta))
    return jobs, 2 + delta**2


def case1(number_of_jobs: int) -> list[Job]:
    """Generate jobs in the form of case1

    .. math::
        \frac{p_1}{w_1} \frac{,...,}{,...,} \frac{p_n}{w_n}
    """
    return NotImplemented


def case2(number_of_jobs: int) -> list[Job]:
    """Generate jobs in the form of case2

    .. math:
        \frac{p_1}{w_1} \frac{<...<}{>...>} \frac{p_n}{w_n}
    """
    return [Job(i + 1, number_of_jobs - i) for i in range(number_of_jobs)]


def case3(number_of_jobs: int) -> list[Job]:
    """Generate jobs in the form of case3

    .. math:
        \frac{p_1}{w_1} \frac{<...<}{<...<} \frac{p_n}{w_n}
    """
    return [Job(i + 1, i + 1) for i in range(number_of_jobs)]


def case4(number_of_jobs: int, i: int = 0) -> list[Job]:
    """Generate jobs in the form of case4

    .. math:

    """
    if i == 0:
        i = number_of_jobs // 2
    return case2(i) + case1(number_of_jobs - i)


def case5(number_of_jobs: int, i: int = 0) -> list[Job]:
    """Generate jobs in the form of case5

    .. math:

    """
    if i == 0:
        i = number_of_jobs // 2
    return case1(i) + case2(number_of_jobs - i)


def case6(number_of_jobs: int, i: int = 0, j: int = 0) -> list[Job]:
    """Generate jobs in the form of case6

    .. math:

    """

    return case1(i) + case2(j - i) + case1(number_of_jobs - j - i)


def case7(number_of_jobs: int, i: int = 0, j: int = 0) -> list[Job]:
    """Generate jobs in the form of case7

    .. math:

    """
    return NotImplemented


def random(number_of_jobs: int) -> list[Job]:
    """
    docstring
    """
    jobs = (
        Job(randint(1, number_of_jobs), randint(1, number_of_jobs))
        for _ in range(number_of_jobs)
    )
    return sorted(jobs, key=ratio)


def base1(number_of_jobs: int) -> list[Job]:
    return [Job(i + 1) for i in range(number_of_jobs)]


def base2(number_of_jobs: int) -> list[Job]:
    return [Job(i + 1, i + 1) for i in range(number_of_jobs)]


def base3(number_of_jobs: int) -> list[Job]:
    return [Job(i + 1, weight=number_of_jobs - i) for i in range(number_of_jobs)]


def base4(number_of_jobs: int) -> list[Job]:
    return [Job(number_of_jobs - i, i + 1) for i in range(number_of_jobs)]
