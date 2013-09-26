

class PlayerSchemaException(Exception): pass


STATS_TO_TRACK = {	'Player':'name',
					'Age':'age',
					'Tm':'team',
					'Pos':'pos', 
				  	'GP':'gp',
				  	'G':'g',
				  	'A':'a',
				  	'PTS':'pts',
				  	'GC':'glcreat',
				 	'+/-':'plsmin',
				 	'PIM':'pim',
				 	'EV':'evgl',
				 	'PP':'ppgl',
				 	'SH':'shgl',
				 	'GW':'gwgl',
				 	'S':'sh',
				 	'S%':'shpercent',
				 	'TOI':'toi',
				 	'ATOI':'atoi'
				 }



def get_value(str, sp1, sp2='', default=0):
	val = str.split(sp1)[-1]
	if sp2: val = val.split(sp2)[0]
	if val: return val
	return default

def to_mins(timestr):
	m, s = timestr.split(':')
	return float(m) + float(s) / 60


class Skater():

	def __init__(self, htmltxt, scheme):
		fields = htmltxt.split('</td>')
		try:
			keys = scheme.keys()

			# special cases
			case = 'name'
			self.__dict__[case] = get_value(fields[scheme[case]], 'csk="', '">')
			keys.remove(case)
			case = 'team'
			self.__dict__[case] = get_value(fields[scheme[case]], 'html">', '</a')
			keys.remove(case)
			case = 'pos'
			self.__dict__[case] = get_value(fields[scheme[case]], '">')
			keys.remove(case)
			case = 'shpercent'
			self.__dict__[case] = float( get_value(fields[scheme[case]], '">') )
			keys.remove(case)
			case = 'atoi'
			self.__dict__[case] = to_mins( get_value(fields[scheme[case]], '">') )
			keys.remove(case)

			# remaining cases should all be integers
			for k in keys:
				self.__dict__[k] = int( get_value(fields[scheme[k]], '">') )

			self.ptspg = self.pts / float( self.gp )
			self.valid = True
		except Exception, e:
			# print e
			# print fields
			self.valid = False

	def __str__(self):
		return str(self.__dict__)

	def printattr(self, attr):
		return '%s, %s' % (self.name, self.__dict__[attr])


class Goalie(Skater):

	def __init__(self, htmltxt):
		fields = htmltxt.splt('<td')
		try: 
			self.name = get_value(fields[2], 'csk="', '">')
			self.age = get_value(fields[3], '">', '</td')
			self.team = get_value(fields[4], '">', '</a')
			self.pos = 'G'
			self.gp = int( get_value(fields[6], '">', '</td') )
			self.w = int( get_value(fields[7], '">', '</td') )
			self.l = int( get_value(fields[8], '">', '</td') )
			self.otl = int( get_value(fields[9], '">', '</td') )
			self.ga = int( get_value(fields[10], '">', '</td') )
			self.sa = int( get_value(fields[11], '">', '</td') )
			self.sv = int( get_value(fields[12], '">', '</td') )
			self.svp = float( get_value(fields[13], '">', '</td', 0) )
			self.gaa = float( get_value(fields[13], '">', '</td', 0) )
			self.so = int( get_value(fields[12], '">', '</td') )
			self.min = int( get_value(fields[12], '">', '</td') )
		except Exception, e:
			# print e
			self.valid = False


def parse_stat_schema(htmllist):
	startstr = '<thead>'
	endstr = '</thead>'
	htmllen = len(htmllist)
	i = 0
	schemestr = None
	while i < htmllen:
		if startstr in htmllist[i]:
			j = i
			while endstr not in htmllist[i] and i < htmllen:
				i+= 1
			schemestr = ''.join(htmllist[j:i])
			break
		i += 1
	if not schemestr: 
		raise PlayerSchemaException('Unable to get player schema')
	schemelist = [ s.split('">')[-1] for s in schemestr.split('</th>')]
	scheme = {}
	i = len(schemelist) - 1
	# we go in reverse as the stat names are not unique, but
	#  the ones we want to track are at the from of the list.
	#  this way when we encounter a duplicate, we overwrite it
	while i > 0:
		val = STATS_TO_TRACK.get(schemelist[i])
		if val: scheme[val] = i
		i -= 1
	return scheme


def create_skater_list(htmllist, scheme):
	startstr = '<tr'
	endstr = '</tr>'
	htmllen = len(htmllist)

	# players = SkaterList(year)
	players = []
	i = 0
	while i < htmllen:
		if startstr in htmllist[i]:
			j = i
			while endstr not in htmllist[i]: i += 1
			p = Skater(''.join(htmllist[j:i]), scheme)
			# if p.valid: players.add_player(p)
			if p.valid: players.append(p)
		i += 1
	return players	


if __name__ == "__main__":
	text = open('alls13.txt').read().split()
	s = parse_stat_schema(text)
	pl = create_skater_list(text, s)
	print pl[0]
