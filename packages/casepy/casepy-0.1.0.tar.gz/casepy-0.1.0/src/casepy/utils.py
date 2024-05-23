""""""
"""
Utility functions for casepy.
"""

def in_list_to_bin(in_list: list):
    """
    Convert a list to a bin list.
    
    Args:
        in_list (list): The list to convert.
        
    Returns:
        tuple: The list of the number of elements and the list of elements.
    """
    result_dict = {}
    element_list = []
    for i in in_list:
        if i not in element_list:
            element_list.append(i)
            result_dict[i] = 1
        else:
            result_dict[i] += 1

    result_list = list(result_dict.values())
    return result_list, element_list
