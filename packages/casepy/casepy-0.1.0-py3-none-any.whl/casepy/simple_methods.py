def factorial(in_target_number: int) -> int:
    result = 1
    for i in range(1, in_target_number + 1):
        result *= i
    return result


def combination_total(in_number_of_elements: int, in_number_of_select: int) -> int:
    if in_number_of_elements == in_number_of_select:
        return 1
    if in_number_of_elements < in_number_of_select:
        return 0

    return (int)(
        factorial(in_number_of_elements)
        / (
            factorial(in_number_of_elements - in_number_of_select)
            * factorial(in_number_of_select)
        )
    )


def permutation_total(in_number_of_elements: int, in_number_of_select: int) -> int:
    """
    Return the number of all possible permutation cases (tranditional method).

    Args:
        in_number_of_elements (int): The number of elements.
        in_number_of_select (int): The number of selections.

    Returns:
        int: The number of all possible permutation cases.
    """
    if in_number_of_elements == in_number_of_select:
        return factorial(in_number_of_elements)
    if in_number_of_elements < in_number_of_select:
        return 0

    return (int)(
        factorial(in_number_of_elements)
        / factorial(in_number_of_elements - in_number_of_select)
    )
