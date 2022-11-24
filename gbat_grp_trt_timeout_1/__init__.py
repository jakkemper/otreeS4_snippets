from otree.api import *
import random

doc = """group_by_arrival_time timeout (continue with solo task) and balanced randomization of treatment at the group level"""

# This app builds on the group_by_arrival_time timeout (continue with solo task) in oTree Snippets:
# https://www.otreehub.com/code/

class C(BaseConstants):
    NAME_IN_URL = 'gbat_gtt1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    treatments = ["animal", "color"]
# The treatment in this app is whether the group has to answer a question on the favorite animal or favorite color


class Subsession(BaseSubsession):
    num_groups_created = models.IntegerField(initial=0)


def group_by_arrival_time_method(subsession, waiting_players):
    if len(waiting_players) >= 2:
        # If 2 players or more are waiting, make a group from the two players waiting the longest
        return waiting_players[:2]
    for player in waiting_players:
        if waiting_too_long(player):
            # make a single-player group.
            return [player]


class Group(BaseGroup):
    treatment = models.StringField()


class Player(BasePlayer):
    favorite_color = models.StringField(label= "What is your favorite color?")
    favorite_animal = models.StringField(label= "What is your favorite animal?")


def waiting_too_long(player: Player):
    participant = player.participant

    import time

    # assumes you set wait_page_arrival in PARTICIPANT_FIELDS.
    return time.time() - participant.wait_page_arrival > 15


class GBAT(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # if it's a solo group (1 player), skip this app
        # and go to the next app (which in this case is a
        # single-player task)
        if len(player.get_others_in_group()) == 0:
            return upcoming_apps[0]

    @staticmethod
    def after_all_players_arrive(group: Group):
        subsession = group.subsession
        # Randomise the order of treatments when the first group arrives on this page
        if subsession.num_groups_created == 0:
            subsession.session.treatments = random.sample(C.treatments, len(C.treatments))


        # % is the modulus operator.
        # so when num_groups_created exceeds the max list index,
        # we go back to 0, thus creating a cycle.
        idx = subsession.num_groups_created % len(subsession.session.treatments)

        group.treatment = subsession.session.treatments[idx]
        for p in group.get_players():
            # since we want the treatment to persist across apps and rounds, we need to assign it
            # in a participant field (which persists across rounds)
            # rather than a group field, which is specific to the round.
            p.participant.treatment = group.treatment

        subsession.num_groups_created += 1


class GroupTask_animal(Page):
    form_model = 'player'
    form_fields = ['favorite_animal']
    def is_displayed(player: Player):
        return player.participant.treatment == "animal"

class GroupTask_color(Page):
    form_model = 'player'
    form_fields = ['favorite_color']
    def is_displayed(player: Player):
        return player.participant.treatment == "color"



class MyWait(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [GBAT, GroupTask_animal, GroupTask_color, MyWait, Results]
