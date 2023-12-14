import sympy

NUM_JOBS = 4


def build_expression(jobs):
    job_symbols = get_symbols(jobs)
    expression = sympy.S.Zero

    for index, (weight, p_time) in enumerate(zip(*job_symbols)):
        part_times = sum(job_symbols[1][: index + 1])
        expression += part_times * weight

    return expression, job_symbols


def get_symbols(jobs):
    weights = [f"w{job}" for job in jobs]
    p_times = [f"p{job}" for job in jobs]

    job_symbols = sympy.symbols([weights, p_times])
    return job_symbols


def main1():
    base_expression, _ = build_expression([1, 2])
    base_expression2, symbols = build_expression([3, 4])
    base_equation = base_expression - base_expression2
    simple_base_equation = sympy.expand(base_equation)
    collected_simple_base_equation = sympy.collect(simple_base_equation, symbols[0][1])

    print(collected_simple_base_equation)


def main2():
    base_expression, ((w1, w2), (p1, p2)) = build_expression([1, 2])
    base_expression2, ((w3, w4), (p3, p4)) = build_expression([3, 4])
    exp1 = (p1 * (w1 + w2) + p2 * w2 - p3 * w3) * (p1 + p4)
    exp2 = ((p1 + p2) * w2) * (p3 + p4)
    # exp1 = (
    #     p3 * w3 * (p1 * (p2 * w2 - p1 * w1) + p1 * p1 * (w1 + w2) - p2 * w2 * (p1 + p2))
    # )
    # exp2 = p1 * (
    #     p1 * w1 + p1 * w2 + p2 * w2 + w1 * (p1 * p1 * (w1 + w2) - p2 * w2 * (p1 + p2))
    # ) - p3 * (p2 * w2 - p1 * w1) * (p1 * w1 + p2 * w2)
    base = exp1 - exp2
    print(sympy.expand(exp1))
    # print(sympy.collect(sympy.expand(exp1), p3 * w2 * w3))
    print(sympy.expand(exp2))
    print(sympy.expand(base))
    exp = sympy.expand(base)
    exp = sympy.collect(exp, p4)
    # exp = sympy.collect(exp, p3)
    # exp = sympy.collect(exp, p1)
    exp = -(
        p1**2 * w1
        + p1**2 * w2
        + p1 * p2 * w2
        - p1 * p3 * w2
        - p1 * p3 * w3
        - p2 * p3 * w2
    )
    exp2 = w2 * (p1 + p2) * (p3 - p1) + p1 * (p3 * w3 - p1 * w1)
    exp = sympy.collect(exp, p1 * w2)
    print(sympy.expand(exp) == sympy.expand(exp2))
    # print(sympy.collect(sympy.expand(exp2), p1))
    # base_equation = exp1 - exp2
    # simple_base_equation = sympy.expand(base_equation)
    # collected_simple_base_equation = sympy.collect(simple_base_equation, w4)

    # print(collected_simple_base_equation)


if __name__ == "__main__":
    main2()
