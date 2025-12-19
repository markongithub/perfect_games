#!/usr/bin/env python

import datetime
import json
import sys

utc = datetime.timezone.utc

def other_side(side_id):
    if side_id == "away":
        return "home"
    else:
        return "away"

# The dict comes from e.g. https://statsapi.mlb.com/api/v1/game/715749/boxscore
def perfect_games_in_box_score(box_score_dict):
    teams_getting_perfectoed = []
    for team_id in ['away', 'home']:
        plate_appearances = box_score_dict['teams'][team_id]['teamStats']['batting']['plateAppearances']
        if plate_appearances == 0:
            # print(f"The {team_id} team has not batted yet.")
            continue
        if box_score_dict['teams'][team_id]['teamStats']['batting']['obp'] == '.000':
            # print(f"The {team_id} team is getting PERFECTOED!")
            teams_getting_perfectoed.append(team_id)
        else:
            # print(f"The {team_id} team has had at least one baserunner or I fucked up.")
            pass
    output = []
    for team_id in teams_getting_perfectoed:
        team_name = box_score_dict['teams'][team_id]['team']['name']
        team_throwing_perfecto = other_side(team_id)
        pitcher_ids = box_score_dict['teams'][team_throwing_perfecto]['pitchers']
        if len(pitcher_ids) == 1:
            # .teams.away.players.ID622554.person.fullName
            pitcher_name = box_score_dict['teams'][team_throwing_perfecto]['players'][f"ID{pitcher_ids[0]}"]['person']['fullName']
            pitcher_team_name = box_score_dict['teams'][team_throwing_perfecto]['team']['name']
            output.append((pitcher_name, pitcher_team_name, team_name))
        else:
            raise Exception("I fucked up the pitcher name logic.")
    return output

def announce_perfect_games(box_score_dict):
    for (pitcher, team, victim) in perfect_games_in_box_score(box_score_dict):
        print(f"{pitcher} has a PERFECT GAME in progress for the {team} against the {victim}!")

def potential_perfectos(schedule_dict):
    output = []
    for schedule_date in schedule_dict['dates']:
        for game in schedule_date['games']:
            game_pee_kay = game['gamePk']
            parsed_time = datetime.datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ')
            now_how_is_this_so_difficult = datetime.datetime.utcnow()
            if parsed_time > now_how_is_this_so_difficult:
                print("This game is in the future.")
                continue


            either_team_has_score_0 = False
            for team_id in ['home', 'away']:
                if game['teams'][team_id].get('score', 999) == 0:
                    print(f"The {game['teams'][team_id]['team']['name']} have score 0 so this could be a perfecto in progress.")
                    either_team_has_score_0 = True
            if either_team_has_score_0:
                # print(f"This game between the {game['teams']['away']['team']['name']} and the  {game['teams']['away']['team']['name']}
                output.append(game_pee_kay)
    return output

if __name__ == "__main__":
    # announce_perfect_games(json.load(open(sys.argv[1])))
    print(potential_perfectos(json.load(open(sys.argv[1]))))
