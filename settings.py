from os import environ

SESSION_CONFIG_DEFAULTS = dict(participation_fee=0, real_world_currency_per_point= 1)

SESSION_CONFIGS = [dict(
        name='GBAT_group_treatment_timeout',
        display_name="Match players with timeout and randomise treatments at the group level",
        num_demo_participants=2,
        app_sequence=[
            'gbat_grp_trt_timeout_0',
            'gbat_grp_trt_timeout_1',
            'gbat_grp_trt_timeout_2',
        ]),
    dict(
        name='public_goods_bots_for_dropouts',
        display_name = "Simple public goods game where dropouts are replaced by bots",
        app_sequence=['public_goods_simple'],
        num_demo_participants=3
    )
                   ]

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'

DEMO_PAGE_INTRO_HTML = ''

PARTICIPANT_FIELDS = [    "treatment",
                          "wait_page_arrival"]
SESSION_FIELDS = ["treatments"]

ROOMS = [
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4577204011385'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
