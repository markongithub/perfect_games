#!/usr/bin/env python

import datetime
import json
import sys

#? 2060  cat test_data/live_746175.json | jq ".gameData.gameInfo.firstPitch | keys"
#?  2061  cat test_data/live_746175.json | jq ".gameData.gameInfo.firstPitch"
#?   2062  cat test_data/live_746175.json | jq ".gameData.status | keys"
#?    2063  cat test_data/live_746175.json | jq | less
#?     2064  cat test_data/live_746175.json | jq ".gameData.status | keys"
#?      2065  cat test_data/live_746175.json | jq ".gameData.status.detailedState | keys"
#?       2066  cat test_data/live_746175.json | jq ".gameData"
#?        2067  cat test_data/live_746175.json | jq ".gameData"| less
#?         2068  cat test_data/live_746175.json | jq keys
#?          2069  cat test_data/live_746175.json | jq ".liveData | keys"
#?           2070  cat test_data/live_746175.json | jq ".liveData.linescore | keys"
#?            2071  cat test_data/live_746175.json | jq ".liveData.linescore.currentInning | keys"
#?             2072  cat test_data/live_746175.json | jq ".liveData.linescore.currentInning"
#?              2073  cat test_data/live_746175.json | jq ".liveData.linescore.isTopInning"
#?               2074  cat test_data/live_746175.json | jq ".liveData.linescore.outs"
#?                2075  cat test_data/live_746175.json | jq ".liveData | keys"
#?                 2076  cat test_data/live_746175.json | jq ".gameData"| less
#?                  2077  cat test_data/live_746175.json | jq ".gameData.status.detailedState"| less

utc = datetime.timezone.utc

def parse_mlb_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

def project_game_length(game_feed_dict):
    first_pitch = parse_mlb_timestamp(game_feed_dict['gameData']['gameInfo']['firstPitch'])
    current_inning = game_feed_dict['liveData']['linescore']['currentInning']
    is_top_inning = game_feed_dict['liveData']['linescore']['isTopInning']
    outs_this_inning = game_feed_dict['liveData']['linescore']['outs']
    outs_before_this_inning = 6 * (current_inning - 1)
    outs_from_top_inning = 0 if is_top_inning else 3
    outs_so_far = outs_before_this_inning + outs_from_top_inning + outs_this_inning
    last_play_time = parse_mlb_timestamp(game_feed_dict['liveData']['plays']['allPlays'][-1]['playEndTime'])
    duration = last_play_time - first_pitch
    print(f"From {first_pitch} to {last_play_time} ({duration}) there were {outs_so_far} outs.")
    duration_51 = duration * 51.0 / outs_so_far
    duration_54 = duration * 54.0 / outs_so_far
    end_time_51 = first_pitch + duration_51
    end_time_54 = first_pitch + duration_54
    print(f"If we skip the bottom of the 9th this game will be {duration_51} and end at {end_time_51}, and if we play it it will be {duration_54} and end at {end_time_54}")

if __name__ == "__main__":
    # announce_perfect_games(json.load(open(sys.argv[1])))
    print(project_game_length(json.load(open(sys.argv[1]))))
