class Action:
    def __init__(self, name, prec, eff):
        self.name = name
        self.prec = prec
        self.eff = eff
    def __str__(self):
        return "name: %s, prec: %s, eff: %s" % (self.name, self.prec, self.eff)
    def __hash__(self):
        return hash(self.name)
