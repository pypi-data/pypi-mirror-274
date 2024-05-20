from .simple_methods import *
from .utils import *
import random


class PermutationGenerator:

    def __init__(self):
        self.element_list_initialized = False
        self.number_of_selection_initialized = False
        self.must_have_elements = False

    def set_parameters(self, in_number_of_selection: int, element_list: list):
        self.in_number_of_selection = in_number_of_selection
        self.element_list = element_list

        self.element_list_initialized = True
        self.number_of_selection_initialized = True
        self.max_possible = self.__duplicated_case_recursive(
            in_list_to_bin(self.element_list)[0], self.in_number_of_selection
        )

    # def set_must_have_elements(self, in_elements_list: list):
    #     if len(in_elements_list) == len(self.element_list):
    #         # TODO: [A, "", E, D, ""] -> replace elements in ""
    #         pass
    #     else:
    #         self.must_have_elements = True
    #         self.must_have_list = in_elements_list
    #         for element in in_elements_list:
    #             self.element_list.remove(element)

    #         self.in_number_of_selection -= len(in_elements_list)
    #         self.max_possible = permutation(
    #             len(self.element_list), self.in_number_of_selection
    #         ) * (self.in_number_of_selection + 1)

    def __duplicated_case_recursive(self, in_list: list, in_number_of_select: int):
        if sum(in_list) == 1:
            return 1

        result_sum = 0
        if in_number_of_select == 1:
            for i in in_list:
                if i != 0:
                    result_sum += 1
            return result_sum
        for i in range(len(in_list)):
            if in_list[i] != 0:
                result_sum += self.__duplicated_case_recursive(
                    in_list[:i] + [in_list[i] - 1] + in_list[i + 1 :],
                    in_number_of_select - 1,
                )
        return result_sum

    def possible_cases(self):
        return self.max_possible

    def all_case(self) -> list:
        if not self.element_list_initialized:
            raise Exception("element_list is not initialized")
        if not self.number_of_selection_initialized:
            raise Exception("number_of_selection is not initialized")

        result_list = []
        for i in range(self.max_possible):
            result_list.append(
                self.permutation_core(i, self.in_number_of_selection, self.element_list)
            )
        return result_list

    def random_case(self, return_i=False) -> list:
        if not self.element_list_initialized:
            raise Exception("element_list is not initialized")
        if not self.number_of_selection_initialized:
            raise Exception("number_of_selection is not initialized")

        random_i = (int)(random.random() * self.max_possible)

        if return_i:
            return random_i, self.permutation_core(
                random_i,
                self.in_number_of_selection,
                self.element_list,
            )
        return self.permutation_core(
            random_i,
            self.in_number_of_selection,
            self.element_list,
        )

    def i_case(self, in_iterator: int) -> list:
        if not self.element_list_initialized:
            raise Exception("element_list is not initialized")
        if not self.number_of_selection_initialized:
            raise Exception("number_of_selection is not initialized")

        return self.__permutation_core(in_iterator)

    def permutation_core_old(
        self, in_iterator: int, in_number_of_selection: int, element_list: list
    ) -> list:
        result_list = []
        buff_element_list = element_list.copy()
        number_of_element = len(buff_element_list)

        iterator = in_iterator

        if self.must_have_elements:
            iterator = in_iterator // (self.in_number_of_selection + 1)

        for i in range(in_number_of_selection):
            current_permutation = permutation(
                number_of_element - i - 1, in_number_of_selection - i - 1
            )
            current_permutation_index = iterator // current_permutation
            iterator = iterator % current_permutation
            result_list.append(buff_element_list[current_permutation_index])
            buff_element_list.pop(current_permutation_index)

        if self.must_have_elements:
            insert_index = in_iterator % (self.in_number_of_selection + 1)
            for i, element in enumerate(self.must_have_list):
                result_list.insert(insert_index + i, element)

        return result_list

    def __permutation_recursive(
        self, in_iterator: int, in_list: list, in_number_of_select: int
    ):
        result_list = []
        if in_number_of_select == 1:
            filtered_list = []
            # print("in 0 -> ", in_list, in_iterator)
            for i, data in enumerate(in_list):
                if data != 0:
                    filtered_list.append(i)
            result_list.append(filtered_list[in_iterator])
            # print("in 1 -> ", filtered_list, result_list)
            return result_list
        if in_number_of_select == 0:
            return result_list
        # results = list(filter(lambda x: x.startswith('f'), animals))

        for i in range(len(in_list)):
            if in_list[i] != 0:
                test_list = in_list[:i] + [in_list[i] - 1] + in_list[i + 1 :]
                test_list_possible_cases = self.__duplicated_case_recursive(
                    test_list, in_number_of_select - 1
                )
                if test_list_possible_cases > in_iterator:
                    result_list.append(i)
                    result_list += self.__permutation_recursive(
                        in_iterator,
                        test_list,
                        in_number_of_select - 1,
                    )

                    break
                else:
                    in_iterator -= test_list_possible_cases

        return result_list

    def __permutation_core(self, in_iterator: int):
        if not in_iterator < self.max_possible:
            return []

        bin_list, element_list = in_list_to_bin(self.element_list)

        result_iterator = self.__permutation_recursive(
            in_iterator, bin_list, self.in_number_of_selection
        )

        result_list = []
        for i in result_iterator:
            result_list.append(element_list[i])

        return result_list
