class CambioStadi:

    def __init__(self,Blocchi,Solver):
        self.Blocchi=Blocchi
        self.col=self.Blocchi.Item("T-100")
        self.Solver=Solver

    def CambioStadio(self, Stadio):
        self.Solver.CanSolve = True
        self.col.ColumnFlowsheet.Operations.Item("Main Tower").NumberOfTrays=Stadio

    
    def FeedStage(self):
        output=str(self.col.ColumnFlowsheet.Operations.Item("Main Tower").FeedStages.Item(0))
        number = int(output.split("__")[0])
        return number