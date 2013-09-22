

class PlayerSchemaException(Exception): pass


def get_value(str, sp1, sp2, default=''):
	val = str.split(sp1)[1].split(sp2)[0]
	if val: return val
	return default

def to_mins(timestr):
	m, s = timestr.split(':')
	return float(m) + float(s) / 60


class Skater():

	def __init__(self, htmltxt):
		fields = htmltxt.split('<td')
		try:
			self.name = get_value(fields[2], 'csk="', '">')
			self.age = get_value(fields[3], '">', '</td')
			self.team = get_value(fields[4], 'html">', '</a')
			self.pos = get_value(fields[5], '">', '</td')
			self.gp = int( get_value(fields[6], '">', '</td') )
			self.gl = int( get_value(fields[7], '">', '</td') )
			self.a = int( get_value(fields[8], '">', '</td') )
			self.pts = int( get_value(fields[9], '">', '</td') )
			self.ptspg = self.pts / float(self.gp)
			self.glcreat = int( get_value(fields[10], '">', '</td') )
			self.plsmin = int( get_value(fields[11], '">', '</td') )
			self.pim = int( get_value(fields[12], '">', '</td') )
			self.evgl = int( get_value(fields[13], '">', '</td') )
			self.ppgl = int( get_value(fields[14], '">', '</td') )
			self.shgl = int( get_value(fields[15], '">', '</td') )
			self.gwgl = int( get_value(fields[16], '">', '</td') )
			self.sh = int( get_value(fields[17], '">', '</td') )
			self.shpercent = float( get_value(fields[18], '">', '</td', 0) )
			self.toi = int( get_value(fields[19], '">', '</td') )
			self.atoi = to_mins( get_value(fields[20], '">', '</td') )
			self.valid = True
		except Exception, e:
			print e
			print fields
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
			print e
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
			while endstr not in htmllist[i]: i+= 1
			schemestr = ''.join(htmllist[j:i])
			break
	if not schemestr: 
		raise PlayerSchemaException('Unable to get player schema')
	schemelist = [ s.split('">')[-1] for s in schemestr.split('</th>')]
	print schemelist


def create_player_list(htmllist, year):
	startstr = '<tr'
	endstr = '</tr>'
	htmllen = len(html)

	players = SkaterList(year)
	i = 0
	while i < htmllen:
		if startstr in html[i]:
			j = i
			while endstr not in html[i]: i += 1
			p = Skater(''.join(html[j:i]))
			if p.valid: players.add_player(p)
		i += 1
	return players	


text = open('13s.txt').read().split()
parse_stat_schema(text)

