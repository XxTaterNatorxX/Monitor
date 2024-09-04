class unit():
    id = 0
    role = 0 #0 for crew 1 for traitor
    work = 0
    search = 0
    independence = 0
    trust = 10
    items = []
    hidden_items = []
    opinions = []
    location = None
    lastArea = None
    alive = True
    knownDead = False
    directive = 0 #0 is work, 1 is search

    def __init__(self, id, role, work, search, independence):
        self.id = id
        self.role = role
        self.work = work
        self.search = search
        self.independence = independence
        self.opinions = []
        self.items = []
        self.hidden_items = []
        self.trust = 10
        self.location = None
        self.lastArea = None
        self.alive = True
        self.knownDead = False
        self.directive = 0