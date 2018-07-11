import os
from enum import Enum, unique


NONE_ENUM = str(None)


@unique
class Rule(Enum):
    BEST_64 = "best64.rule"

    def get_path(self):
        return os.path.join("rules", self.value)


@unique
class WordList(Enum):
    ROCKYOU = "rockyou.txt"
    PHPBB = "phpbb.txt"
    DIGITS_8 = "digits_8.txt"
    DIGITS_APPEND = "digits_append.txt"
    WEAK = "conficker_elitehacker_john_riskypass_top1000.txt"
    ESSID = "essid.txt"

    def get_path(self):
        return os.path.join("wordlists", self.value)
