
import pytest

from src.secure_aggregation import (
    DEFAULT_MODULUS,
    aggregate_shares,
    reconstruct_secret,
    split_secret,
)


def test_split_and_reconstruct_small_integer():
    shares = split_secret(17)
    assert reconstruct_secret(*shares) == 17


def test_split_and_reconstruct_zero():
    shares = split_secret(0)
    assert reconstruct_secret(*shares) == 0


def test_split_and_reconstruct_maximum_secret():
    secret = DEFAULT_MODULUS - 1
    shares = split_secret(secret)
    assert reconstruct_secret(*shares) == secret


def test_aggregate_two_institutions():
    a1, a2 = split_secret(17)
    b1, b2 = split_secret(23)

    result = aggregate_shares([a1, b1], [a2, b2])

    assert result == 40


def test_aggregate_multiple_institutions():
    counts = [17, 23, 5, 0, 12]
    first_shares = []
    second_shares = []

    for count in counts:
        share1, share2 = split_secret(count)
        first_shares.append(share1)
        second_shares.append(share2)

    result = aggregate_shares(first_shares, second_shares)

    assert result == sum(counts)


def test_reject_negative_secret():
    with pytest.raises(ValueError):
        split_secret(-1)


def test_reject_secret_equal_to_modulus():
    with pytest.raises(ValueError):
        split_secret(DEFAULT_MODULUS)


def test_reject_non_integer_secret():
    with pytest.raises(TypeError):
        split_secret(17.5)


def test_reject_boolean_secret():
    with pytest.raises(TypeError):
        split_secret(True)


def test_reject_mismatched_share_lists():
    with pytest.raises(ValueError):
        aggregate_shares([1, 2], [3])


def test_reject_invalid_modulus():
    with pytest.raises(ValueError):
        split_secret(1, modulus=2)



def test_reject_share_outside_modulus():
    with pytest.raises(ValueError):
        reconstruct_secret(5, 11, modulus=11)

