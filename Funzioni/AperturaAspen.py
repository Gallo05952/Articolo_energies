import win32com.client

class AspenHYSYS:
    def __init__(self,simulation_file):
        self.hysys_app = None
        self.hysys_sim = None
        self.HySolver = None
        self.Stream = None
        self.Blocchi = None
        self.SimulationFile = simulation_file


    def open_simulation(self):
        try:
            self.hysys_app = win32com.client.Dispatch("HYSYS.Application")
            self.hysys_sim = self.hysys_app.SimulationCases.Open(self.SimulationFile)
            self.HySolver = self.hysys_sim.Solver
            self.Stream = self.hysys_sim.Flowsheet.Streams
            self.Blocchi = self.hysys_sim.Flowsheet.Operations
            # self.hysys_sim.Visible=1
            return self.HySolver, self.Stream, self.Blocchi, self.hysys_sim
        except Exception as e:
            return False
        

class InserimentoComposizione:
    def __init__(self,Strem):
        self.Stream = Strem
    
    def inserimento(self,Composizione):
        biogas=self.Stream.Item("BG")
        biogas.ComponentMolarFraction.Values=Composizione
        print("Cambio composizione effettuato")