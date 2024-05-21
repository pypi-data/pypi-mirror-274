import math


def pass_at_k(num_total_samples_n: int, num_correct_samples_c: int, k: int) -> float:
    """Evaluate the pass@k metric.

    Args:
        num_total_samples_n: total number of samples (`n`)
        num_correct_samples_c: number of correct samples (`c`)
        k: k in pass@k (`k`)
    """

    # assert types
    assert isinstance(num_total_samples_n, int), "num_total_samples_n must be an integer"
    assert isinstance(num_correct_samples_c, int), "num_correct_samples_c must be an integer"
    assert isinstance(k, int), "k must be an integer"

    # assert ranges
    assert (
        0 <= num_correct_samples_c <= num_total_samples_n
    ), "num_correct_samples_c must be between 0 and num_total_samples_n"
    assert num_total_samples_n > 0, "num_total_samples_n must be greater than 0"
    assert k > 0, "k must be greater than 0"

    if num_total_samples_n - num_correct_samples_c < k:
        return 1.0

    # calculate the actual pass@k metric
    range_list = range(num_total_samples_n - num_correct_samples_c + 1, num_total_samples_n + 1)
    differences = [(1.0 - k / x) for x in range_list]
    product = math.prod(differences)
    return 1.0 - product
