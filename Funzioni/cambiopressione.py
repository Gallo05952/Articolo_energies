class CambioPressione:

    def __init__(self, Blocchi):
        self.Blocchi = Blocchi

    def CambioP(self, p):
        cella=self.Blocchi.Item("Comp_BG").Cell(1,1)
        cella.cellValue=p