from partial_scheduling.models.job import create_from, reduce


def test_reduce_strong() -> None:
    # Arrange
    data = create_from([(1, 3), (1, 4), (1, 4), (2, 2), (2, 3), (2, 2)])

    # Act
    over = reduce(data)

    # Assert
    assert over, create_from([(1, 3), (2, 2), (2, 2)])


def test_reduce_weak() -> None:
    # Arrange
    data = create_from([(1, 3), (1, 4), (1, 4), (2, 2), (2, 3), (2, 2)])

    # Act
    over = reduce(data, True)

    # Assert
    assert over, create_from([(1, 3), (2, 2)])
