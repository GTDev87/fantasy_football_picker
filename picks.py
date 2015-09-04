import config as cfg


def update(position_dict, roster_list, player_dict, pick, p):
    position_dict[player_dict[pick].position_num].pop(0)
    for j in range(cfg.num_roster_spots):
        if cfg.starter_num_list[j] % player_dict[pick].position_num == 0 and roster_list[p].picked_team[j] == -1:
            # there is an opening roster spot (important for filling flex last)
            roster_list[p].picked_team[j] = pick  # place the player here, i is player id
            player_dict[pick].taken = True        # mark the player as taken
            roster_list[p].product /= cfg.starter_num_list[j]
            
            # divide by roster spot (important to divide through for flex
            roster_list[p].points += player_dict[pick].points
            return position_dict, roster_list, player_dict


def greedy_pick(p, num_players, player_dict, roster_list):
    for i in range(num_players):
        if player_dict[i].taken:
            continue
        if roster_list[p].open(player_dict[i].position_num):  # if there is a position opening
            return i
    return -1


def smart_pick(spot, player_dict, position_dict, roster_list, p, num_players):
    # pick next available in greedy fashion
    greedy = greedy_pick(p, num_players, player_dict, roster_list)  # pick next available
    num2check = cfg.num_in_between[spot % cfg.num_teams]
    if num2check == 0:
        return greedy

    # initialize players_selected and best_players
    players_selected = {}
    best_players = {}

    for position_num, players in position_dict.iteritems():
        if roster_list[p].open(position_num):  # roster opening
            players_selected[position_num] = player_dict[players[0]].points
            best_players[position_num] = players[0]

    # wait until after setting player_selected and best player to update the rosters
    position_dict, roster_list, player_dict = update(position_dict, roster_list, player_dict, greedy, p)

    # if it's your last pick, just return
    if spot + num2check >= cfg.num_picks - 1:
        return greedy

    # other players make their picks
    for n in range(num2check):
        spot2 = spot + n
        p = cfg.pick_order[spot2]
        pick = greedy_pick(p, num_players, player_dict, roster_list)  # other players "hypothetically" picking
        position_dict, roster_list, player_dict = update(position_dict, roster_list, player_dict, pick, p)

    # fill players_selected
    for position_num, players in position_dict.iteritems():
        if position_num not in players_selected:
            continue
        if len(players) == 0 or players[0] not in player_dict:
            players_selected[position_num] = -1
            continue
        players_selected[position_num] -= player_dict[players[0]].points

    if len(players_selected) == 0:
        pick = greedy  # just pick best available
    else:
        position = max(players_selected, key=players_selected.get)  # returns key (player ID) with highest value (score)
        pick = best_players[position]

    return pick