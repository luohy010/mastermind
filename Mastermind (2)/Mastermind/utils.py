from typing import List


def prompt() -> str:
    """ perform prompt input from user starting with >
    :return: the input string """
    return input('> ')


def convert_input_to_code_values(input_code: str) -> List[str]:
    """ convert string values of the code to list with each character peg as an element
     :param: input code in string
     :return: input code as a list of all pegs """
    return [char for char in input_code]


class MasterMindException(Exception):
    """ MasterMindException for defining the type of exception to be coming from mastermind game """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CodeParsingException(Exception):
    """ CodeParsingException for defining the type of exception to be coming from failing to parse the code values """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
