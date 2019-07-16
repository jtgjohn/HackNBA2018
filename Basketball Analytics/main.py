import math
import numpy as np


def parse_games(games_data, games_dict):
    
    first = False
    with open(games_data) as data:
        for line in data:
            if not first:
                first = True
                continue            
            line = line.strip().split("\t")
            if line[0] not in games_dict.keys():
                games_dict[line[0]] = dict()
            if line[1] not in games_dict[line[0]].keys():
                games_dict[line[0]][line[1]] = dict()
            if line[3] not in games_dict[line[0]][line[1]]:
                games_dict[line[0]][line[1]] = dict()
            games_dict[line[0]][line[1]][line[3]] = line[2]
            
def parse_plays(plays_data, plays_dict):
    
    first = False
    with open(plays_data) as data:
        for line in data:
            if not first:
                first = True
                continue
            line = line.strip().split("\t")
            if line[0] not in plays_dict.keys():
                plays_dict[line[0]] = dict()
            
        

if __name__ == "__main__":
    
    games_dict = dict()
    parse_games("NBA Hackathon - Game Lineup Data Sample (50 Games).txt", games_dict)
    for game in games_dict:
        for period in games_dict[game]:
            for team in games_dict[game][period]:
                print(game, period, games_dict[game][period][team], team)
    
    