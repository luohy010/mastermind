from models import GameRule

# all predefined game rules
ORIGINAL_1P_GAMERULE = GameRule(True, 1, 12, False, 4)
ORIGINAL_2P_GAMERULE = GameRule(False, 1, 12, False, 4)
MASTERMIND_GAMERULE = GameRule(True, 4, 5, True, 5)