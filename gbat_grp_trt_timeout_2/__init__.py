from otree.api import *

doc = """Solo task that player complete after the game (or if they had to wait too long)"""

class C(BaseConstants):
    NAME_IN_URL = 'gbat_gtt2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class SoloTask(Page):
    pass


page_sequence = [SoloTask]
