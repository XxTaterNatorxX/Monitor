class area():
    id = "common"
    easy_tasks = 0
    med_tasks = 0
    hard_tasks = 0
    units = []
    bodies = []
    items = []
    #tripwire
    sensor = False
    #monitor ppl bodies and items
    camera = False
    progress = 0
    needed = 0
    easy_limit = 0

    def __init__(self, id):
        self.id = id
        self.items = []
        self.units = []
        self.bodies = []
        self.items = []
        self.easy_tasks = 0
        self.med_tasks = 0
        self.hard_tasks = 0
        self.sensor = False
        self.camera = False
        self.progress = 0
        self.easy_limit = 0
        self.needed = 0