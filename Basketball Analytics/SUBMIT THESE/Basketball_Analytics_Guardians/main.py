import csv



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
			self.active[team].clear() #clearing the previous periods active set 
		for player in self.lineup[period]:
			team = self.playerteams[player]
			self.active[team].add(player)

	def substitution(self, subin, subout):
		self.active[self.playerteams[subout]].remove(subout)
		self.active[self.playerteams[subin]].add(subin)

	def get_players(self): 
		return self.active 

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
			if 'A' in status.upper(): 
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
			line = line.split('\t') 
			etype = int(line[0])
			action = int(line[1])
			msg = line[2].strip().strip("\"")
			desc = line[3].strip().strip("\"")
			if etype not in codedict:
				codedict[etype] = dict()
			codedict[etype][action] = (msg, desc)
	return codedict

def getposs(playerteams, game, player, event):
	if game not in playerteams:
		playerteams[game] = dict()
	if player not in playerteams[game]:
		playerteams[game][player] = event.team_id
	return playerteams[game][player]


def addrtg(ratings, game, player, pts, off):
	if game not in ratings:
		ratings[game] = dict()
	if player not in ratings[game]:
		ratings[game][player] = [0] * 4
	if off:
		ratings[game][player][0] += pts
	else:
		ratings[game][player][1] += pts

def addposs(ratings, game, player, off):
	if game not in ratings:
		ratings[game] = dict()
	if player not in ratings[game]:
		ratings[game][player] = [0] * 4
	if off:
		ratings[game][player][2] += 1
	else:
		ratings[game][player][3] += 1


def calc_ratings(ratings, playdict, playerteams, lineupdict, event_codes):

	for game in playdict:
		period = -1
		oldposs = None
		newposs = None
		freethrow = False
		freethrowsubs = []
		activeset = ActiveSet(playerteams, game, lineupdict)

		# set up 2 way dict to easily get one team by knowing the other
		oppteams = dict()
		for team in activeset.get_players():
			for t in activeset.get_players():
				if t != team : oppteams[team] = t

		for event in playdict[game]:
			if period < event.period:
				oldposs = None
				period = event.period
				activeset.start_period(period)
			event_msg, event_desc = event_codes[event.event_type][event.action]
			event_msg = event_msg.lower()
			event_desc = event_desc.lower()
			print(event_msg)

			if "jump ball" in event_msg:
				newposs = event.team_id
			elif "made shot" in event_msg:
				pts = event.option1
				team = getposs(playerteams, game, event.person1, event)
				for t in activeset.get_players():
					for player in activeset.get_players()[t]:
						if t == team:
							addrtg(ratings, game, player, pts, True)
						else:
							addrtg(ratings, game, player, pts, False)
							newposs = t
			elif "free throw" in event_msg:
				freethrow = True
				if event.option1 == 1:
					team = getposs(playerteams, game, event.person1, event)
					for t in activeset.get_players():
						for player in activeset.get_players()[t]:
							addrtg(ratings, game, player, 1, t == team)
			elif "substitution" in event_msg:
				if freethrow:
					freethrowsubs.append((event.person1, event.person2))
				else:
					activeset.substitution(event.person2, event.person1)
			elif "rebound" in event_msg:
				newposs = getposs(playerteams, game, event.person1, event)
			elif "turnover" in event_msg:
				newposs = oppteams[getposs(playerteams, game, event.person1, event)]

			if oldposs != None and oldposs != newposs:
				for team in activeset.get_players():
					for player in activeset.get_players()[team]:
						addposs(ratings, game, player, team == oldposs)
			oldposs = newposs

			if freethrow and "free throw" in event_msg and ("1 of 2" not in event_desc or "1 of 3" not in event_desc or "2 of 3" not in event_desc):
				freethrow = False
				for subout, subin in freethrowsubs:
					activeset.substitution(subin, subout)


def write_csv(ratings, filename):
	with open(filename, "w") as file:
		fieldnames = ["Game_ID", "Player_ID", "OffRtg", "DefRtg"]
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		writer.writeheader()
		for game in ratings:
			for player in ratings[game]:
				offrtg = 0
				if ratings[game][player][2] != 0:
					offrtg = (ratings[game][player][0]/ratings[game][player][2])*100
				defrtg = 0
				if ratings[game][player][3] != 0:
					defrtg = (ratings[game][player][1]/ratings[game][player][3])*100
				writer.writerow({"Game_ID":game, "Player_ID":player, "OffRtg":offrtg, "DefRtg":defrtg})


if __name__ == "__main__" :
	playfile = "Play_by_Play.txt"
	lineupfile = "Game_Lineup.txt"
	codefile = "Event_Codes.txt"
	outfile = "Guardians_Q1_BBALL.csv"
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
	# event_codes[type][action] = (msg, desc)
	ratings = dict() #dict to hold all output info
	for game in gameset:
		ratings[game] = dict()
		for player in playerteams[game]:
			ratings[game][player] = [0] * 4

	calc_ratings(ratings, playdict, playerteams, lineupdict, event_codes)
	print(ratings)
	write_csv(ratings, outfile)







