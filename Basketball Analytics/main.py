import math
import numpy as np
import csv

def parse_plays(playfile):
	with open(playfile) as file:
		reader = csv.DictReader(file)
		for row in reader:
			print(row)


if __name__ == "__main__" :
	playfile = "Play_by_Play.txt"
	lineupfile = "Game_Lineup.txt"
	codefile = "Event_Codes.txt"
	playdict = parse_plays(playfile)