from .simple_methods import *
from .combination_generator import *


class BinaryGenerator(CombinationGenerator):
    def __init__(self) -> None:
        super().__init__()

    def set_parameters(self, in_number_of_one, in_total_length):
        self.in_number_of_one = in_number_of_one
        self.in_total_length = in_total_length
        element_list = []
        for i in range(in_total_length):
            if i < in_number_of_one:
                element_list.append(1)
            element_list.append(0)
        super().set_parameters(in_number_of_one, element_list)

    def i_case(self, in_iterator: int) -> list:
        result = []
        pass

    def case_to_i(self, in_case: list) -> int:
        pass
