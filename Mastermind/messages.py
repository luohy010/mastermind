from abc import ABC, abstractmethod
from typing import Optional

GAME_OPTIONS = 'Select which game you want to play: \n' \
               '   (A) Original Mastermind for 2 Players\n' \
               '   (B) Original Mastermind for 1 Player\n' \
               '   (C) Mastermind44 for 4 Players\n' \
               '*Enter A, B, or C to continue*'

WELCOME_MESSAGE = 'Welcome to Mastermind!\n' \
                  'Developed by {my_name}\n' \
                  'COMP 1046 Object-Oriented Programming\n'

PLAYER_NAME_PROMPT = "Player {player_number}: What is your name?"

FINAL_CODE_ENTER = 'Enter the code now:'
FINAL_CODE_REENTER = 'Enter the same code again:'
FINAL_CODE_STORED = 'The code was stored\n'

ORIGINAL_START_GUESSING = 'Welcome {player_name}. You can now start to play by guessing the code.\n' \
                          'Enter a guess by providing four characters and press Enter.'

UNPARSABLE_TOKEN = 'This attempt is incorrect. ' \
                   'You must provide exactly {max_code_length} characters and they can only be, {with_blank}R, L, G, Y, W or B.'

ORIGINAL_ATTEMPT = "Attempt #{current_round}: "
ORIGINAL_ATTEMPT_FEEDBACK = "Feedback on Attempt #{current_round}: "

CORRECT_ATTEMPT = '\nCongratulations! {who} broke the code in {attempt} attempts.'
GAME_OVER = '\nExceed {attempt} attempts. Game Over! The correct code is {final_code}'
PROMPT_PLAY_OR_QUIT = "What would you like to do?\n" \
                      "   (p)lay the game again\n" \
                      "   (q)uit"
QUIT_MESSAGE = "Goodbye!"

MASTERMIND_REVEAL_GUIDE = 'Player {player_name}: When you are ready for one position of the code to be revealed on the screen press <enter>.'
MASTERMIND_REVEAL_PEG = 'Position: {position} Colour: {color}'
MASTERMIND_CLEAR_SCREEN = 'Press <enter> to clear the screen'

MASTERMIND_PLAYER_TURN = '{player_name}, Attempt #{current_round}: Enter {max_code_length} colours using (R)ed, b(L)ue, (G)reen, (Y)ellow, (W)hite, or (B)lack:'
MASTERMIND_START_GUESSING = 'Each player can now start to guess the code.'
MASTERMIND_ATTEMPT_FEEDBACK = "Feedback on {who}, Attempt #{attempt}: "

INVALID_SELECTION = "Invalid selection."

ORIGINAL_2P_CODE_MAKER_GUIDE = "Welcome {code_maker_name}, you need to create a code that consists of {max_code_length} pegs. " \
                               "Each peg can be of the colour (R)ed, B(L)ue, (G)reen, (Y)ellow, (W)hite, " \
                               "or (B)lack. Specify the {max_code_length} by specifying four characters where each " \
                               "character indicates a colour as above. For example, WWRG represents the " \
                               "code White-White-Red-Green. You need to enter the code twice. No character " \
                               "is shown on the screen so {code_breaker_name} cannot see it."

ORIGINAL_1P_CODE_MAKER_GUIDE = 'Welcome to Mastermind! The computer will create the secret code that consists of four pegs. ' \
                               'Each peg can be of the colour (R)ed, B(L)ue, (G)reen, (Y)ellow, (W)hite, or (B)lack.'

MASTERMIND_CODE_MAKER_GUIDE = 'Welcome to Masermind44! The computer will create the secret code and reveal ' \
                              'four of the five positions one-by-one individually to each player. During ' \
                              'revealing each position only the requested player should look at the ' \
                              'screen. (R)ed, b(L)ue, (G)reen, (Y)ellow, (W)hite, or (B)lack'

REENTER_CODE_VALUES_NOT_MATCH = 'Re-enter code value does not match'


class MessageBankInterface(ABC):
    """ MessageBankInterface interface class for defining some messages to be used across different game type """

    @abstractmethod
    def _get_code_maker_guide_mssg(self, code_maker_name: Optional[str], code_breaker_name: Optional[str]) -> str:
        pass

    @abstractmethod
    def _get_attempt_start_mssg(self, player_name: str) -> str:
        pass

    @abstractmethod
    def _get_attempt_feedback_mssg(self, current_round: int, player_name: str) -> str:
        pass

    @staticmethod
    def get_unparsable_token_mssg(max_peg_length: int, allow_blank: bool) -> str:
        return UNPARSABLE_TOKEN.format(max_code_length=max_peg_length, with_blank='_, ' if allow_blank else '')
