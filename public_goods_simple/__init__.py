from otree.api import *


#This is a simple public goods game where dropouts are replaced by bots. Players who remained in the
#experiment are not aware that they are playing with bots.

class Constants(BaseConstants):
    name_in_url = 'public_goods_simple'
    players_per_group = 3
    num_rounds = 1
    endowment = cu(100)
    multiplier = 1.8


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )
    #we create a dropout dummy variable so we can locate dropouts in the dataset after data colllection.
    is_dropout = models.BooleanField(initial=False)


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
    #we set a reasonable timeout time for whcih we believe all participants, if active, would be able to finish
    #the page task. This can be based on a pilot study. Here it is 20 seconds for demonstration purposes.

    #Timeout on the "Contribute" page is visible while it is hidden on the "Results" page. See .html page
    # files for CSS code.
    timeout_seconds = 20

    @staticmethod
# If the player is unresponsive after 20 seconds, a bot plays instead of the
# player and contributes 100 points. Other players do not know that a bot plays instead of the
# dropout player.
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.is_dropout = True
            player.contribution = 100

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    #we set another timeout to streamline the dropouts moving to the last page. This is espeically usefull
    #if multiple pages depend on player interactions/decisions.
    @staticmethod
    def get_timeout_seconds(player):
        if player.is_dropout:
            return 5  # instant timeout of 5 seconds (for visibility when manually testing,
            # it can be even shorter), if not regular timeout applies.
        else:
            return 20
    #A dropout can happen at any page. We apply the same for the "Results" page.
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.is_dropout = True

class EndPage(Page):
    @staticmethod
    def get_timeout_seconds(player):
        if player.is_dropout:
            return 5  # instant timeout of 5 seconds (for visibility, it can be even shorter),
            # if not regular timeout applies
        else:
            return 100


page_sequence = [Contribute, ResultsWaitPage, Results, EndPage]
