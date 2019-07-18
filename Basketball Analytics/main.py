import math
import numpy as np

def parse_plays(playfile):
	with open(playfile) as file:
		i=0
		for line in file:
			print(line.split()[0].strip("\""))
			i += 1
			if i == 2:
				break


if __name__ == "__main__" :
	playfile = "Play_by_Play.txt"
	lineupfile = "Game_Lineup.txt"
	codefile = "Event_Codes.txt"
	playdict = parse_plays(playfile)
