def factorial(in_target_number: int) -> int:
    result = 1
    for i in range(1, in_target_number + 1):
        result *= i
    return result


def combination(in_number_of_elements: int, in_number_of_select: int) -> int:
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


def permutation(in_elements_info, in_number_of_select: int) -> int:
    if type(in_elements_info) == int:
        return permutation_core(in_elements_info, in_number_of_select)
    else:
        setted_elements_list = list(set(in_elements_info))
        setted_elements_list.sort()

        element_counting = []
        for element in setted_elements_list:
            element_counting.append(in_elements_info.count(element))

        result = permutation_core(len(in_elements_info), in_number_of_select)
        for count in element_counting:
            result /= factorial(count)

        return int(result)


def permutation_core(in_number_of_elements: int, in_number_of_select: int) -> int:
    if in_number_of_elements == in_number_of_select:
        return factorial(in_number_of_elements)
    if in_number_of_elements < in_number_of_select:
        return 0

    return (int)(
        factorial(in_number_of_elements)
        / factorial(in_number_of_elements - in_number_of_select)
    )
