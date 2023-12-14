def bounds_in_terms(
    jobs_left: list[int], jobs_right: list[int], sign="=", term: int = 1
):
    left_components = job_cost_components_dict(jobs_left)
    right_components = job_cost_components_dict(jobs_right)
    left_side = ""
    right_side = ""
    if term in left_components:
        left_side = f"j{term}.w"
        left_components_l = []
        right_components_l = []
        for k, v in right_components.items():
            part_result = v + f" * j{k}.w"
            right_components_l.append(part_result)
        for k, v in left_components.items():
            if k == term:
                continue
            part_result = v + f" * j{k}.w"
            left_components_l.append(part_result)
        right_side = (
            "("
            + " + ".join(right_components_l)
            + " - "
            + " - ".join(left_components_l)
            + ")/("
            + left_components[term]
            + ")"
        )
        return left_side + " " + sign + " " + right_side

    if term in right_components:
        right_side = f"j{term}.w"
        left_components_l = []
        right_components_l = []
        for k, v in left_components.items():
            part_result = v + f" * j{k}.w"
            left_components_l.append(part_result)
        for k, v in right_components.items():
            if k == term:
                continue
            part_result = v + f" * j{k}.w"
            right_components_l.append(part_result)
        left_side = (
            "("
            + " + ".join(left_components_l)
            + " - "
            + " - ".join(right_components_l)
            + ")/("
            + right_components[term]
            + ")"
        )
        return left_side + " " + sign + " " + right_side
    return NotImplemented


def bounds_in_string(jobs_left: list[int], jobs_right: list[int], sign="="):
    left_side = job_cost_in_string(jobs_left)
    right_side = job_cost_in_string(jobs_right)
    return left_side + " " + sign + " " + right_side


def job_cost_in_string(jobs: list[int]):
    result = job_cost_components_list(jobs)
    return " + ".join(result)


def job_cost_components_list(jobs):
    result = []
    for index, job in enumerate(jobs):
        preceding_jobs = jobs[: index + 1]
        processing_times = " + ".join([f"j{p_jobs}.p" for p_jobs in preceding_jobs])
        result.append(f"({processing_times}) * j{job}.w")
    return result


def job_cost_components_dict(jobs: list[int]) -> dict[int, str]:
    result = {}
    for index, job in enumerate(jobs):
        preceding_jobs = jobs[: index + 1]
        processing_times = " + ".join([f"j{p_jobs}.p" for p_jobs in preceding_jobs])
        result[job] = f"({processing_times})"
    return result


if __name__ == "__main__":
    FORMULA: str = bounds_in_string([1, 2, 3], [4, 5], "<=")
    print(FORMULA)
    FORMULA: str = bounds_in_terms([1, 2, 3], [4, 5], "<=", 3)
    print(FORMULA)
