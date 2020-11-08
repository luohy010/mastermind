import copy
import random
from abc import abstractmethod, ABC
from enum import Enum
from typing import List, Optional

import messages
from messages import MessageBankInterface
from utils import prompt, MasterMindException, CodeParsingException, convert_input_to_code_values


class Peg(Enum):
    """ Peg enum to store all Peg values """
    RED = 'R'
    BLACK = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    BLUE = 'L'
    WHITE = 'W'
    BLANK = '_'

    @staticmethod
    def get_peg_by_value(value: str) -> "Peg":
        """ from the given peg value, get the corresponding Peg object
         :param: value: the string value of the peg
         :return: the corresponding Peg object
         :except: value not found"""
        value_list = list(Peg._value2member_map_.keys())
        value_upper = value.upper()
        if value_upper not in value_list:
            raise CodeParsingException()
        return Peg._value2member_map_.get(value_upper)

    @staticmethod
    def generate_random_peg() -> "Peg":
        """ :return:generate a random Peg object """
        all_possible_pegs = list(Peg._value2member_map_.values())
        index = random.randint(0, len(all_possible_pegs) - 1)
        return all_possible_pegs[index]


class FeedBackValue(Enum):
    """ FeedbackValue enum to store feedback values """
    BLACK = 'B'
    WHITE = 'W'


class Code:
    """ Code class to represents a Code created by CodeMaker and CodeBreaker """
    def __init__(self, pegs: List[Peg]) -> None:
        super().__init__()
        self.__pegs: List[Peg] = pegs

    @staticmethod
    def parse(pegs_input: str, game_rule: "GameRule") -> "Code":
        """ parse an input code string to the corresponding Code object, with the check to make sure it follows the game rule
         :param: pegs_input: input string value of the pegs, game_rule: the game_rule to check the code follows
         :return: the parsed Code object"""
        peg_value_list: List[str] = convert_input_to_code_values(pegs_input)
        if not Code.__is_peg_values_usable(peg_value_list, game_rule):
            raise CodeParsingException()
        return Code(list(map(lambda peg_value: Peg.get_peg_by_value(peg_value), peg_value_list)))

    def get_pegs(self) -> List[Peg]:
        return self.__pegs

    @staticmethod
    def __is_peg_values_usable(peg_values: List[str], game_rule: "GameRule") -> bool:
        """ check if the peg string values follow the game rule
        :param: peg_values: input string value of the pegs, game_rule: the game_rule to check the code follows
        :return: the boolean value whether the values follow the game rule """
        if game_rule.allow_blank():
            blank_rule_followed = len(list(filter(lambda peg_value: peg_value == '_', peg_values))) < 2
        else:
            blank_rule_followed = '_' not in peg_values
        return len(peg_values) == game_rule.get_max_code_peg() and blank_rule_followed

    def __str__(self) -> str:
        return ' '.join(list(map(lambda peg: peg.value, self.__pegs)))


class CodeBreaker:
    """ CodeBreaker class represents code breaker """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.__name: str = name

    def make_a_guess(self, guess_values: Code, final_code: Code) -> "AttemptFeedback":
        """ perform guessing and give feedback """
        return AttemptFeedback.evaluate(guess_values, final_code)

    def get_name(self) -> str:
        return self.__name


class AttemptFeedback:
    """ AttemptFeedback class represents a feedback after evaluating a guess code and the final code """

    def __init__(self, feedback: List[FeedBackValue]) -> None:
        super().__init__()
        self.__feedback_values: List[FeedBackValue] = feedback

    @staticmethod
    def __fill_in_black_feedback(current_feedback: List[FeedBackValue], guess_pegs: List[Peg], final_code_pegs: List[Peg]) -> (List[FeedBackValue or None], List[Peg]):
        """ find all correct peg in each position and change the position feedback value to Black, then update the remaining checkable final code pegs
        :param: current_feedback: current state of the feedback, guess_pegs: list of guess pegs, final_code_pegs: list of final code pegs
        :return: tuple of updated feedback values after filled black in and the list of remaining checkable final code pegs"""
        updated_feedback = copy.deepcopy(current_feedback)
        pegs_range = range(len(final_code_pegs))
        remaining_final_code_pegs = []
        for i in pegs_range:
            final_code_peg = final_code_pegs[i]
            if guess_pegs[i] == final_code_peg:
                updated_feedback[i] = FeedBackValue.BLACK
            else:
                remaining_final_code_pegs.append(final_code_peg)
        return updated_feedback, remaining_final_code_pegs

    @staticmethod
    def __fill_in_white_feedback(current_feedback: List[FeedBackValue], guess_pegs: List[Peg], remaining_final_pegs: List[Peg]) -> List[FeedBackValue]:
        """ from the remaining final pegs, check if any other position in the current feedback (currently not assigned Black) to exists in the remaining final pegs, then update
        it to white and remove it from the remaining final pegs counter
        :param: current_feedback: current state of the feed back, guess_pegs: list of guess pegs, remaining_final_pegs: remaining pegs counter of the final code
        :return: the feed back values after fill white feedback in"""
        updated_feedback = copy.deepcopy(current_feedback)
        if len(remaining_final_pegs) == 0:
            return updated_feedback
        updated_remaining_final_pegs = copy.deepcopy(remaining_final_pegs)
        for i in range(len(guess_pegs)):
            if updated_feedback[i] is None and guess_pegs[i] in updated_remaining_final_pegs:
                updated_remaining_final_pegs.remove(guess_pegs[i])
                updated_feedback[i] = FeedBackValue.WHITE
        return updated_feedback

    @staticmethod
    def evaluate(guess: Code, final_code: Code) -> "AttemptFeedback":
        """ creation method to evaluate the guess code with the final code
         :param: guess code and final code
         :return the AttemptFeedback object corresponding to the guess """
        guess_pegs = guess.get_pegs()
        final_pegs = final_code.get_pegs()
        # init the feedback values to all None
        initial_feedback: List[FeedBackValue or None] = [None for i in range(len(final_code.get_pegs()))]
        # fill the feed back with Black values, and retrieveing the remaining final code pegs that can be check for white
        filled_black_feedback, remaining_final_pegs_checkable = AttemptFeedback.__fill_in_black_feedback(initial_feedback, guess_pegs, final_pegs)
        # check for white
        filled_white_feedback = AttemptFeedback.__fill_in_white_feedback(filled_black_feedback, guess_pegs, remaining_final_pegs_checkable)
        # filter out the None value
        final_feedback = list(filter(lambda peg: peg is not None, filled_white_feedback))
        return AttemptFeedback(final_feedback)

    def is_winning_state(self, required_correct_values: int) -> bool:
        """ :param: required_correct_values: number of black feedback value required to be considered sufficient to win
        check whether feedback returns all Black for each of the value corresponding to the required correct values
        :return whether it's sufficient to win """
        return len(list(filter(lambda feedback_value: feedback_value == FeedBackValue.BLACK, self.__feedback_values))) == required_correct_values

    def __str__(self) -> str:
        """ display feedback values """
        if len(self.__feedback_values) == 0:
            return "Nothing."
        return ' '.join(list(map(lambda feedback: feedback.value, self.__feedback_values)))


class CodeMaker(ABC):
    """ CodeMaker class represents a Generic CodeMaker """

    def __init__(self, name: str = None) -> None:
        super().__init__()
        self._name: str = name
        self._final_code: Optional[Code] = None

    @abstractmethod
    def make_new_final_code(self, game_rule: "GameRule"):
        """ perform making a new final code """
        pass

    def get_name(self):
        return self._name


class HumanCodeMaker(CodeMaker):
    """ HumanCodeMaker class represents a CodeMaker human type """

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @staticmethod
    def __prompt_final_code(game_rule: "GameRule") -> Code:
        """ prompt player to input the final code
        :param: game_rule: to check whether the final code follow the game rule
        :return: the final code object"""
        while True:
            try:
                print(messages.FINAL_CODE_ENTER)
                prompted_final_code_value: str = prompt()
                parsed_final_code_value: Code = Code.parse(prompted_final_code_value, game_rule)
                print(messages.FINAL_CODE_REENTER)
                prompted_final_code_value_reenter: str = prompt()
                if prompted_final_code_value != prompted_final_code_value_reenter:
                    raise MasterMindException(messages.REENTER_CODE_VALUES_NOT_MATCH)
                print(messages.FINAL_CODE_STORED)
                return parsed_final_code_value
            except CodeParsingException:
                print(MessageBankInterface.get_unparsable_token_mssg(game_rule.get_max_code_peg(), game_rule.allow_blank()))
            except MasterMindException as e:
                print(e)

    def make_new_final_code(self, game_rule: "GameRule") -> Code:
        """ prompt player to input the final code
        :param: game_rule: to check whether the final code follow the game rule
        :return: the final code object"""
        self._final_code = self.__prompt_final_code(game_rule)
        return self._final_code


class ComputerCodeMaker(CodeMaker):

    def __init__(self) -> None:
        super().__init__(None)

    def make_new_final_code(self, game_rule: "GameRule") -> Code:
        """ computer ganerates random final code
        :param: game_rule: to check whether the final code follow the game rule
        :return: the final code object"""
        max_code_pegs: int = game_rule.get_max_code_peg()
        code_pegs: List[Peg] = []
        for i in range(max_code_pegs):
            peg: Peg = Peg.generate_random_peg()
            while (not game_rule.allow_blank() or Peg.BLANK in code_pegs) and peg == Peg.BLANK:
                peg: Peg = Peg.generate_random_peg()
            code_pegs.append(peg)
        print(code_pegs)
        self._final_code = Code(code_pegs)
        return self._final_code


class GameRule:
    """ GameRule class represents a game rule that set the standards of the game """

    def __init__(self, is_computer_code_maker: bool, max_breakers: int, max_attempts: int, allow_blank: bool, max_code_peg: int) -> None:
        super().__init__()
        self._max_breakers = max_breakers
        self._max_attempts = max_attempts
        self._allow_blank = allow_blank
        self._max_code_peg = max_code_peg
        self._is_computer_code_maker = is_computer_code_maker

    def get_max_breakers(self) -> int:
        return self._max_breakers

    def get_max_attempts(self) -> int:
        return self._max_attempts

    def allow_blank(self) -> bool:
        return self._allow_blank

    def get_max_code_peg(self) -> int:
        return self._max_code_peg

    def is_computer_code_maker(self) -> bool:
        return self._is_computer_code_maker
