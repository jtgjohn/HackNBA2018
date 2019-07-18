import math
import numpy as np

class Event(object):

	def __init__(self, infolist):
		self.event_num = int(infolist[0])
		self.event_msg_type = int(infolist[1])
		self.period = int(infolist[2])
		self.wc_time = int(infolist[3])
		self.pc_time = int(infolist[4])
		self.action_type = int(infolist[5])
		self.option1 = int(infolist[6])
		self.option2 = int(infolist[7])
		self.option3 = int(infolist[8])
		self.team_id = infolist[9].strip("\"")
		self.person1 = infolist[10].strip("\"")
		self.person2 = infolist[11].strip("\"")
		self.person3 = infolist[12].strip("\"")
		self.team_id_type = int(infolist[13])
		self.person1_type = int(infolist[14])
		self.person2_type = int(infolist[15])
		self.person3_type = int(infolist[16])

	def __str__(self):
		return str(self.period) + ' ' + str(self.pc_time) + ' ' + str(self.wc_time) + ' ' + str(self.event_num)
	
	def __lt__(self, other):
		lhs = (self.period, other.pc_time, self.wc_time, self.event_num)
		rhs = (other.period, self.pc_time, other.wc_time, other.event_num)
		return lhs < rhs



def parse_plays(playfile):
	playdict = dict()
	first = True
	with open(playfile) as file:
		for line in file:
			if first:
				first = False
				continue
			line = line.split()
			game = line[0].strip("\"")
			if game not in playdict:
				playdict[game] = []
			playdict[game].append(Event(line[1:]))
	return playdict



if __name__ == "__main__" :
	playfile = "Play_by_Play.txt"
	lineupfile = "Game_Lineup.txt"
	codefile = "Event_Codes.txt"
	playdict = parse_plays(playfile)
	for game in playdict:
		playdict[game].sort()
		for event in playdict[game]:
			print(event)
		break
