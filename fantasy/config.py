# Inputs to change
num_teams = 16
starter_list = ['QB','QB','RB', 'RB', 'WR', 'WR', 'TE', 'D', 'K', 'F']
starter_num_list = [2, 2, 3, 3, 5, 5, 7, 11, 13, 105]

# ensure that starter_list matches start_num_list

num_roster_spots = len(starter_list)  # typically even
draftType = 'Snake'
player_type = {}
player_type['QB'] = [2, 1, 4]  # ID number, min/max spots on roster
player_type['RB'] = [3, 2, 4]
player_type['WR'] = [5, 2, 4]
player_type['TE'] = [7, 1, 4]
player_type['D'] = [11, 1, 2]
player_type['K'] = [13, 1, 1]

if draftType == 'Snake':
    pick_order = (range(num_teams) + range(num_teams - 1, -1, -1)) * (num_roster_spots / 2)
    if num_roster_spots % 2 == 1:  # correction for if num_roster_spots is not even
        pick_order += range(num_teams)

    num_in_between = [(2 * (num_teams - i - 1)) for i in range(num_teams)]

num_picks = num_teams * num_roster_spots

__author__ = 'Austin'
