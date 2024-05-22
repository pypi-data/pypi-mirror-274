from procedure_data_tool.utils.valve import Valve

class Valve3(Valve):
    directions = 3
    def __init__(self, ein, pit = None, jumper = None, jumperLabel = None, dvi = None):
        super().__init__(ein, pit= pit, jumper = jumper)
        self.directions = 3
        self.ein = ein
        self.connections = []
        self.show = True
        self.in_tank = False
        self.position
        self.dvi_credited = dvi

    def setPosition(self, route = None):
        for connection in self.connections:
            if connection in route:
                pass
            else:
                if connection.EIN():
                    self.position = "BLOCK " +  connection.EIN()
                else:
                    for next_connection in connection.connections:
                        if next_connection == self or next_connection in self.connections:
                            pass
                        else:
                            self.position = "BLOCK " + next_connection.EIN()

    def findDVI(self, route):
        self.dvi_used = self.dvi_credited #CORRECT. ALWAYS
        for connection in self.connections:
            if connection in route:
                pass
            else:
                if connection.EIN():
                    route.append(connection)
                else:
                    for next_connection in connection.connections:
                        if next_connection == self or next_connection in self.connections:
                            pass
                        else:
                            route.append(next_connection)
        return 
    
    def getColor(self):
        if (self.dvi_used == "YES"):
            self.color = "skyblue"
        elif (self.dvi_used == "POS"):
            self.color = "red"
        if (self.dvi_used == "NO"):
            self.color = "#A0A0A0"
        return self.color