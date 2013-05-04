
"""
Stephen Tredger, May 2013

order_picker.py - generates a random n round draft order for m teams

Usage: order_picker.py <draft_type> <rounds> <team_1> .. <team_N>
    draft_type = [r | s] for r(andom) or s(erpentine) drafts
    rounds = number of rounds in draft
    team_i = team name (quote names with spaces!)
"""

# minimalist import for some reason
from random import shuffle
from sys import argv, exit


class random_draft:
    """ random_draft(team_names, num_rounds)
    team_names = a list of strings naming the teams
    num_rounds = number of rounds in the draft

    Creates a random draft order where each round is independent
    of the previous. 
    """
    
    def __init__(self, team_names, num_rounds):
        self.teams = {}
        self.team_names = team_names
        self.num_teams = len(team_names)
        self.num_rounds = num_rounds
        for i in xrange(self.num_teams):
            self.teams[i] = []
        self.create_draft()

    def random_order(self):
        """ Returns a list with a random permutation over [1 .. num_teams] """
        ord = [i for i in xrange(self.num_teams)]
        shuffle(ord)
        return ord

    def append_round(self, order):
        """ Appends the draft position for each team in order
        to the team dictionary """
        for i in xrange(len(order)):
            self.teams[order[i]].append(i+1)

    def create_draft(self):
        """ Creates a draft order filling in the teams dictionary """
        for i in xrange(self.num_rounds):
            ord = self.random_order()
            self.append_round(ord)

    def print_draft(self):
        """ Prints the team dictionary as a tab separated table """
        s = "Rnd"
        for team in self.team_names:
            s += "\t" + str(team)
        s += "\n"
        for i in xrange(self.num_rounds):
            s += str(i+1) + "\t"
            for j in xrange(self.num_teams):
                s += str(self.teams[j][i]) + "\t"
            s += "\n"
        print s
            


class serpentine_draft(random_draft):
    """ serpentine_draft(team_names, num_rounds)
    team_names = a list of strings naming the teams
    num_rounds = number of rounds in the draft

    Creates a random draft order where the last pick in
    the previous round gets first pick in the next. 
    """
    
    def serpentine_order(self, last_pick):
        """ Returns a non random permutation over [1 .. num_teams]
        where last_pick always appears as the first element"""
        ord = [i for i in xrange(self.num_teams)]
        shuffle(ord)
        ord.remove(last_pick)
        ord.insert(0, last_pick)
        return ord

    def create_draft(self):
        """ Creates a draft order filling in the teams dictionary """
        ord = self.random_order()
        self.append_round(ord)
        last_pick = ord[-1]
        for i in xrange(self.num_rounds - 1):
            ord = self.serpentine_order(last_pick)
            self.append_round(ord)
            last_pick = ord[-1]



def print_help():
    print "Generates an n round draft order for m teams!\nUsage:"
    print "order_picker.py <draft_type> <rounds> <team_1> .. <team_N>"
    print "\tdraft_type = [r | s] for r(andom) or s(erpentine) drafts"
    print "\trounds = number of rounds in draft"
    print "\tteam_i = team name (quote names with spaces!)"

# For command line usage
if __name__ == "__main__":

    if len(argv) < 3:
        print_help()
        exit()

    draft_type = argv[1]
    teams = argv[3:]
    try:
        rounds = int(argv[2])
    except ValueError:
        print_help()
        exit()
        
    if draft_type == "r":
        draft = random_draft(teams, rounds)
    elif draft_type == "s":
        draft = serpentine_draft(teams, rounds)
    else:
        print_help()
        exit()
        
    draft.print_draft()
