import math
import numpy as np

class Event(object):

	def __init__(self, infolist):
		self.event_num = int(infolist[0])
		self.event_type = int(infolist[1])
		self.period = int(infolist[2])
		self.wc_time = int(infolist[3])
		self.pc_time = int(infolist[4])
		self.action = int(infolist[5])
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


class ActiveSet(object):

	# active[team] = set(players)
	# playerteams[player] = team
	# lineup[period] = [player]
	def __init__(self, playerteams, game, lineupdict):
		active = dict()
		self.lineup = lineupdict[game]
		for player in playerteams[game]:
			team = playerteams[game][player]
			if team not in active:
				active[team] = set()
		self.active = active
		self.playerteams = playerteams[game]

	def start_period(self, period):
		for team in self.active:
			active[team].clear()
		for player in self.lineup[period]:
			team = self.playerteams[player]
			self.active[team].add(player)

	def substitution(self, subin, subout):
		self.active[self.playerteams[subout]].remove(subout)
		self.active[self.playerteams[subin]].add(subin)

	def get_players(self):
		return self.active

	def remove(self, remset):
		for player in remset:
			self.active[playerteams[player]].remove(player)

	def add(self, remset):
		for player in remset:
			self.active[playerteams[player]].add(player)


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

def parse_games(gamefile, gameset, playerteams):
	infodict = dict()
	first = True
	with open(gamefile) as file:
		for line in file:
			if first:
				first = False
				continue
			line = line.split()
			game = line[0].strip("\"")
			period = int(line[1])
			player = line[2].strip("\"")
			team = line[3].strip("\"")
			status = line[4].strip("\"")

			if game not in infodict:
				infodict[game] = dict()
			if 'A' in status.upper(): # active players only
				if period not in infodict[game]:
					infodict[game][period] = []
				infodict[game][period].append(player)

			#add info to data structures
			if game not in playerteams:
				playerteams[game] = dict()
			playerteams[game][player] = team
			gameset.add(game)
	return infodict

def parse_event_codes(codefile):
	codedict = dict()
	first = True
	with open(codefile) as file:
		for line in file:
			if first:
				first = False
				continue
			line = line.split()
			etype = int(line[0])
			action = int(line[1])
			msg = line[2].strip("\"")
			desc = line[3].strip("\"")
			if etype not in codedict:
				codedict[etype] = dict()
			codedict[etype][action] = msg
	return codedict


def calc_ratings(ratings, playdict, playerteams, lineupdict, event_codes):

	for game in playdict:
		period = -1
		oldposs = None
		newposs = None
		freethrow = False
		freethrowsubs = []
		activeset = ActiveSet(playerteams, game, lineupdict)
		for event in playdict[game]:
			if period < event.period:
				period = event.period
				activeset.start_period(period)
			event_msg = event_codes[event.event_type][event.action].lower()

			if freethrow and "free throw" not in event_msg:
				freethrow = False
				for subout, subin in freethrowsubs:
					activeset.substitution(subin, subout)

			if "jump ball" in event_msg:
				newposs = event.team_id
			if "made shot" in event_msg:



if __name__ == "__main__" :
	playfile = "Play_by_Play.txt"
	lineupfile = "Game_Lineup.txt"
	codefile = "Event_Codes.txt"
	playdict = parse_plays(playfile)
	for game in playdict:
		playdict[game].sort()
	gameset = set()
	playerteams = dict()
	lineupdict = parse_games(lineupfile, gameset, playerteams)
	event_codes = parse_event_codes(codefile)


	#Stats structure:
	# ratings[game][player] = [off pnts, def pnts, off poss, def poss]
	# lineupdict[game][period] = [players]
	# playdict[game] = [Events]
	# playerteams[game][player] = team
	# event_codes[type][action] = msg
	ratings = dict() #dict to hold all output info
	for game in gameset:
		ratings[game] = dict()
		for player in playerteams:
			ratings[game][player] = [0] * 4

	calc_ratings(ratings, playdict, playerteams, lineupdict)







