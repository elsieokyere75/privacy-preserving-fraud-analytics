
"""Educational additive secret sharing for secure aggregation.

This module demonstrates how integer values can be split into two
shares and reconstructed using arithmetic modulo a prime.

It is a learning prototype, not a production cryptographic system.
"""

import secrets


DEFAULT_MODULUS = 2**127 - 1


def _validate_modulus(modulus: int) -> None:
    """Require a modulus greater than two."""
    if isinstance(modulus, bool) or not isinstance(modulus, int):
        raise TypeError("modulus must be an integer")
    if modulus <= 2:
        raise ValueError("modulus must be greater than 2")


def split_secret(
    secret: int,
    modulus: int = DEFAULT_MODULUS,
) -> tuple[int, int]:
    """Split an integer into two additive shares modulo modulus.

    Returns two shares whose modular sum equals secret modulo modulus.
    The secret must be a non-negative integer smaller than modulus.
    """
    _validate_modulus(modulus)

    if isinstance(secret, bool) or not isinstance(secret, int):
        raise TypeError("secret must be an integer")
    if not 0 <= secret < modulus:
        raise ValueError("secret must be between 0 and modulus - 1")

    first_share = secrets.randbelow(modulus)
    second_share = (secret - first_share) % modulus

    return first_share, second_share


def reconstruct_secret(
    first_share: int,
    second_share: int,
    modulus: int = DEFAULT_MODULUS,
) -> int:
    """Reconstruct a secret from two additive shares."""
    _validate_modulus(modulus)

    for name, share in (
        ("first_share", first_share),
        ("second_share", second_share),
    ):
        if isinstance(share, bool) or not isinstance(share, int):
            raise TypeError(f"{name} must be an integer")
        if not 0 <= share < modulus:
            raise ValueError(f"{name} must be between 0 and modulus - 1")

    return (first_share + second_share) % modulus


def aggregate_shares(
    first_shares: list[int],
    second_shares: list[int],
    modulus: int = DEFAULT_MODULUS,
) -> int:
    """Aggregate shares from multiple institutions.

    Each list represents the shares held by one aggregation server.
    The lists must contain the same number of shares.
    """
    _validate_modulus(modulus)

    if len(first_shares) != len(second_shares):
        raise ValueError("share lists must have the same length")

    for shares in (first_shares, second_shares):
        for share in shares:
            if isinstance(share, bool) or not isinstance(share, int):
                raise TypeError("all shares must be integers")
            if not 0 <= share < modulus:
                raise ValueError("each share must be within the modulus")

    server_one_total = sum(first_shares) % modulus
    server_two_total = sum(second_shares) % modulus

    return reconstruct_secret(server_one_total, server_two_total, modulus)


if __name__ == "__main__":
    institution_a_count = 17
    institution_b_count = 23

    a_share_1, a_share_2 = split_secret(institution_a_count)
    b_share_1, b_share_2 = split_secret(institution_b_count)

    combined_total = aggregate_shares(
        [a_share_1, b_share_1],
        [a_share_2, b_share_2],
    )

    print("Institution A: 17 cases")
    print("Institution B: 23 cases")
    print("Combined total reconstructed by aggregation: ", combined_total)
