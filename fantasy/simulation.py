import csv
import copy
import config as cfg
from picks import greedy_pick, smart_pick, update
from teams import Roster, Player


def read_file(file_name):
    roster_list = [Roster() for _ in xrange(cfg.num_teams)]
    player_dict = {}
    position_dict = dict((el[0], []) for el in cfg.player_type.values())
    num_players = 0
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            position_num = cfg.player_type[row['position']][0]
            x = Player(row['name'], row['position'], position_num, row['points'])
            player_dict[num_players] = x
            position_dict[position_num].append(num_players)
            num_players += 1
    return roster_list, player_dict, position_dict, num_players


def run_simulation(file_name):
    picked_dict = {}
    for team in range(cfg.num_teams+1):
        strategy_list = [1]*cfg.num_teams
        if team < cfg.num_teams:
            strategy_list[team] = 2

        # Read in player info from csv
        roster_list, player_dict, position_dict, num_players = read_file(file_name)

        for spot in xrange(cfg.num_picks):
            p = cfg.pick_order[spot]
            strategy = strategy_list[p]

            if strategy == 2:
                roster_list_copy = copy.deepcopy(roster_list)
                player_dict_copy = copy.deepcopy(player_dict)
                position_dict_copy = copy.deepcopy(position_dict)

                pick = smart_pick(spot, player_dict_copy, position_dict_copy, roster_list_copy, p, num_players)

            else:  # strategy == 1:
                pick = greedy_pick(p, num_players, player_dict, roster_list)

            # alter roster for picked play
            position_dict, roster_list, player_dict = update(position_dict, roster_list, player_dict, pick, p)
            player_dict[pick].round_taken = (spot/cfg.num_teams)+1

        for i in range(cfg.num_teams):
            print roster_list[i].points, ", ",
        print " "

        if team < cfg.num_teams:
            for i in roster_list[team].picked_team:
                if i in picked_dict:
                    picked_dict[i][0] += 1
                else:
                    picked_dict[i] = [1]
                picked_dict[i].append(player_dict[i].round_taken)

    for i in picked_dict.keys():
        if picked_dict[i][0] < 3:
            picked_dict.pop(i)
#    print picked_dict
    for i in picked_dict:
        print player_dict[i].name, picked_dict[i]


def main():
    run_simulation()


if __name__ == '__main__':
    main()
