from django.shortcuts import render
from assassins.models import GameRules, KillAction
from collections import OrderedDict


def gamerules_details(request, gamerules_id):
    rules = GameRules.objects.get(id=gamerules_id)
    min_total_players = 0
    max_total_players = 0

    for faction in rules.factions.all():
        min_total_players += faction.min_starting_players
        if faction.max_starting_players > 0:
            if not max_total_players is None:
                max_total_players += faction.max_starting_players
        else:
            max_total_players = None

    kill_actions = KillAction.find_subclass_objects(rules=rules)
    kill_actions_tree = dict()

    for action in kill_actions:
        subtree = kill_actions_tree
        for condition in action.precondition_list:
            condition_text = 'If %s, then ...' % (condition,)
            if not condition_text in subtree.keys():
                d = OrderedDict()
                d[''] = []
                subtree[condition_text] = d
            subtree = subtree[condition_text]
        for condition in action.postcondition_list:
            subtree[''].append(condition)

    return render(request, 'gamerules_details.html', locals())