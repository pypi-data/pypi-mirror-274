import pytest

from pass_at_k import pass_at_k


def test_always_passes():
    assert True


def test_pass_at_k_1():
    assert pass_at_k(20, 10, 5) == pytest.approx(0.983746130)
    assert pass_at_k(20, 10, 20) == pytest.approx(1.0)
    assert pass_at_k(20, 0, 5) == (0.0)

    # Per: https://ai.stackexchange.com/a/40396
    assert pass_at_k(2, 1, 1) == pytest.approx(0.5)

    # Assorted generated test cases
    assert pass_at_k(67, 64, 1) == pytest.approx(0.9552238805970149)
    assert pass_at_k(72, 28, 25) == pytest.approx(0.9999999077053778)
    assert pass_at_k(97, 48, 10) == pytest.approx(0.9993465715964786)
    assert pass_at_k(22, 21, 1) == pytest.approx(0.9545454545454545)
    assert pass_at_k(17, 15, 5) == pytest.approx(1.0)
    assert pass_at_k(83, 17, 1) == pytest.approx(0.2048192771084335)
    assert pass_at_k(29, 0, 1) == pytest.approx(0.0)
    assert pass_at_k(5, 1, 25) == pytest.approx(1.0)
    assert pass_at_k(93, 9, 1) == pytest.approx(0.09677419354838701)
    assert pass_at_k(96, 2, 1) == pytest.approx(0.02083333333333337)
    assert pass_at_k(93, 38, 25) == pytest.approx(0.9999998973803372)
    assert pass_at_k(100, 62, 5) == pytest.approx(0.9933329986165038)
    assert pass_at_k(64, 32, 10) == pytest.approx(0.9995741013348244)
    assert pass_at_k(5, 4, 25) == pytest.approx(1.0)
    assert pass_at_k(49, 43, 25) == pytest.approx(1.0)
    assert pass_at_k(92, 22, 10) == pytest.approx(0.9449836504863601)
    assert pass_at_k(54, 15, 1) == pytest.approx(0.2777777777777779)
    assert pass_at_k(79, 1, 5) == pytest.approx(0.06329113924050633)
    assert pass_at_k(13, 0, 10) == pytest.approx(0.0)
    assert pass_at_k(92, 92, 10) == pytest.approx(1.0)

    # Examples in README:
    assert pass_at_k(
        num_total_samples_n=8,
        num_correct_samples_c=3,
        k=5,
    ) == pytest.approx(0.98214285714)
    assert pass_at_k(8, 3, 1) == pytest.approx(0.375)


def test_pass_at_k_invalid_input():
    # invalid types
    with pytest.raises(AssertionError):
        pass_at_k(20.0, 10, 5)
    with pytest.raises(AssertionError):
        pass_at_k(20, 10.0, 5)
    with pytest.raises(AssertionError):
        pass_at_k(20, 10, 5.0)

    # invalid range: total_samples vs. correct_samples
    with pytest.raises(AssertionError):
        pass_at_k(20, 21, 5)

    # invalid ranges
    with pytest.raises(AssertionError):
        pass_at_k(20, -1, 5)
    with pytest.raises(AssertionError):
        pass_at_k(-1, 10, 10)
    with pytest.raises(AssertionError):
        pass_at_k(0, 10, 10)
    with pytest.raises(AssertionError):
        pass_at_k(20, 10, 0)
    with pytest.raises(AssertionError):
        pass_at_k(20, 10, -1)
