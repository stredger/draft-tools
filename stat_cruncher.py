import requests
import player_sort
import players

class PlayerListException(Exception): pass


DEFENCE = ['D']
FORWARD = ['C', 'LW', 'RW']
GOAL = ['G']
ALL = DEFENCE + FORWARD + GOAL



class Player():

	def __init__(self, name):
		self.name = name
		self.score = 0

	def __str__(self):
		return '%s %s' % (self.name, self.score)


class SkaterList():

	def __init__(self, htmllist, year):
		self.year = year
		scheme = players.parse_stat_schema(htmllist)
		self.skaters = players.create_skater_list(htmllist, scheme)
		self.last_sorted = ''

	def add_player(self, player):
		self.skaters.append(player)

	def sort_players(self, attr):
		if self.last_sorted == attr: return
		self.last_sorted = attr
		player_sort.quicksort(self.skaters, attr)

	def trim_by_pos_and_gp(self, n, pos, mingp):
		l = []
		i = 0
		while len(l) < n and i < len(self.skaters):
			if self.skaters[i].gp >= mingp and self.skaters[i].pos in pos:
				l.append(self.skaters[i])
			i += 1
		return l

	def get_top(self, attr, n, pos=ALL, mingp=1):
		self.sort_players(attr)
		return self.trim_by_pos_and_gp(n, pos, mingp)


	def all_top_pts(self, n=50):
		return self.get_top('pts', n)

	def all_top_ptspg(self, n=50):
		return self.get_top('ptspg', n)

	def all_top_ptspg_with_min_gp(self, n=50, mingp=30):
		return self.get_top('ptspg', n, mingp=mingp)

	def d_top_pts(self, n=50):
		return self.get_top('pts', n, pos=DEFENCE)

	def d_top_ptspg(self, n=50):
		return self.get_top('ptspg', n, pos=DEFENCE)

	def d_top_ptspg_with_min_gp(self, n=50, mingp=30):
		return self.get_top('ptspg', n, pos=DEFENCE, mingp=mingp)

	def f_top_pts(self, n=50):
		return self.get_top('pts', n, pos=FORWARD)

	def f_top_ptspg(self, n=50):
		return self.get_top('ptspg', n, pos=FORWARD)

	def f_top_ptspg_with_min_gp(self, n=50, mingp=30):
		return self.get_top('ptspg', n, pos=FORWARD, mingp=mingp)



class StatList():

	def __init__(self):
		self.skater_lists = {}

	def add_skater_list(self, plist):
		self.skater_lists[plist.year] = plist	




def get_stat_html_page(host):

	req = requests.get(host)

	f = open('alls13.txt', 'w')
	f.write(req.text)
	f.close()

	if req.status_code != 200:
		raise PlayerListException('Unable to get web page: %s' % (host))
	return req.text.split()



if __name__ == "__main__":

	host13 = 'http://www.hockey-reference.com/leagues/NHL_2013_skaters.html'
	host12 = 'http://www.hockey-reference.com/leagues/NHL_2012_skaters.html'
	host11 = 'http://www.hockey-reference.com/leagues/NHL_2011_skaters.html'

	fpicks = {}
	dpicks = {}

	text = get_stat_html_page(host13)
	players = SkaterList(text, '')

	for p in players.d_top_pts(n=30):
		print p.printattr('pts')

	print '\nd ppg'
	for p in players.d_top_ptspg(n=30):
		print p.printattr('ptspg')

	print '\nd ppg min gp'
	for p in players.d_top_ptspg_with_min_gp(n=30, mingp=10):
		print p.printattr('ptspg')

	# st = StatList()
	# st.add_player_list(players12)
	# st.add_player_list(players13)
