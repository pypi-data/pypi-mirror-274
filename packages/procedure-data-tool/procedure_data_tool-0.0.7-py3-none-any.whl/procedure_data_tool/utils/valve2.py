from procedure_data_tool.utils.valve import Valve

class Valve2(Valve):
    directions = 2
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper) 
        self.ein = ein
        self.directions = 2 
        self.connections = []
        self.show = True
        self.in_tank = False
        self.position = "CLOSED"
        self.dvi_credited = dvi

    def setPosition(self, route = None):
            self.position = "OPEN"
    
    def findDVI(self, route):
        self.dvi_used = "YES"
        self.color = "#A0A0A0"
        return 
    
