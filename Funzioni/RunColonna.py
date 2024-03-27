import time

class Colonna:
    def __init__(self, Blocco, HySolver,Simulazione,Streams,Comp):
        self.Blocco = Blocco
        self.HySolver = HySolver
        self.Simulazione = Simulazione
        self.Streams = Streams
        self.Comp=Comp

    def RunColonna(self):
    #    self.Blocco.ColumnFlowsheet.Reset()
        self.HySolver.CanSolve = True
        self.Blocco.ColumnFlowsheet.Specifications.Item("Comp Fraction - 2").IsActive=False
        self.Blocco.ColumnFlowsheet.Specifications.Item("Comp Fraction").IsActive=False
        self.Blocco.ColumnFlowsheet.Specifications.Item("Reflux Ratio").IsActive=True
        # self.Blocco.ColumnFlowsheet.Specifications.Item("Reflux Ratio").Goal.Value=2
        self.Blocco.ColumnFlowsheet.Specifications.Item('Temperature').IsActive=True
        self.Blocco.ColumnFlowsheet.Run()
        esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus
        
        while esecuzione:
            time.sleep(0.5)
            esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus
        
        Status=self.Blocco.ColumnFlowsheet.CfsConverged
            
        if Status:
            T_dis_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-Dist@COL1").FormationFlag
            T_reflx_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-Reflux@COL1").FormationFlag
            T_2cond_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-To Condenser@COL1").FormationFlag
            if T_dis_calc == 1 or T_reflx_calc==1 or T_2cond_calc==1:
                print("Si forma del Ghiaccio")
                QReb=None
                QCond=None 
                Status = False 
                Q_Comp_BG=None
                W_Comp_BG=None
            else:
                print("Tutto lisio  ")
                QReb=self.ConsumiReb()
                QCond=self.ConsumiCond()
                Q_Comp_BG=self.QCompBG()
                W_Comp_BG=self.WCompBG()
        else:
            print("La colonna non è arrivata a convergenza")
            QReb=None
            QCond=None
            Q_Comp_BG=None
            W_Comp_BG=None
        return QReb, QCond, Status, Q_Comp_BG, W_Comp_BG

    def Temp(self, Temperatura):
        T = self.Blocco.ColumnFlowsheet.Specifications.Item('Temperature')
        T.IsActive=True
        T.GoalValue = Temperatura

    def RefluxRatio(self, RR):
        RefRatio = self.Blocco.ColumnFlowsheet.Specifications.Item('Reflux Ratio')
        RefRatio.IsActive=True
        RefRatio.Goal = RR

    def ConsumiReb(self):
        QReb = self.Blocco.ColumnFlowsheet.Streams.Item("Q_Reb").HeatFlow.Value #kW
        return QReb
    
    def ConsumiCond(self):
        QCond = self.Blocco.ColumnFlowsheet.Streams.Item("Q_Cond").HeatFlow.Value #kW
        return QCond
    
    def ConsumiPreCool(self,PreCool):
        QPreCool = PreCool.HeatFlow.Value
        return QPreCool
    
    def CompDistillato(self):
        DistillatoMolarFraction=self.Streams.Item("Dist").ComponentMolarFractionValue
        Composizione={
            "CH4":DistillatoMolarFraction[0],
            "CO2":DistillatoMolarFraction[1],
            "N2":DistillatoMolarFraction[2],
            "O2":DistillatoMolarFraction[3]
        }
        return Composizione
    
    def CompBottom(self):
        DistillatoMolarFraction=self.Streams.Item("Bott").ComponentMolarFractionValue
        Composizione={
            "CH4":DistillatoMolarFraction[0],
            "CO2":DistillatoMolarFraction[1],
            "N2":DistillatoMolarFraction[2],
            "O2":DistillatoMolarFraction[3]
        }
        return Composizione
    
    def RunSemplice(self):
        self.Blocco.ColumnFlowsheet.Reset()
        self.HySolver.CanSolve = True
        self.Blocco.ColumnFlowsheet.Run()
        esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus
        
        while esecuzione:
            time.sleep(0.5)
            esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus

    def DistMoleFlow(self):
        MolarFlow=(self.Streams.Item("Dist").MolarFlow.Value)/0.00027780
        return MolarFlow

    def TDisti(self):
        T=self.Streams.Item("Dist").Temperature.Value
        return T
    
    def QCompBG(self):
        Q1=self.Comp.OwnedFlowsheet.Streams.Item("Q_S1").HeatFlow.Value
        Q2=self.Comp.OwnedFlowsheet.Streams.Item("Q_S2").HeatFlow.Value
        Q3=self.Comp.OwnedFlowsheet.Streams.Item("Q_S3").HeatFlow.Value
        Q=Q1+Q2+Q3
        return Q
    
    def WCompBG(self):
        W1=self.Comp.OwnedFlowsheet.Streams.Item("W_C1").Power.Value
        W2=self.Comp.OwnedFlowsheet.Streams.Item("W_C2").Power.Value
        W3=self.Comp.OwnedFlowsheet.Streams.Item("W_C3").Power.Value
        W=W1+W2+W3
        return W
    
    def RunRR(self,RR):
        self.HySolver.CanSolve = False
        self.Blocco.ColumnFlowsheet.Reset()
        self.Blocco.ColumnFlowsheet.Specifications.Item("Reflux Ratio").IsActive=True
        self.Blocco.ColumnFlowsheet.Specifications.Item("Comp Fraction - 2").IsActive=True
        self.Blocco.ColumnFlowsheet.Specifications.Item("Temperature").IsActive=False
        self.Blocco.ColumnFlowsheet.Specifications.Item("Reflux Ratio").Goal.Value=RR
        self.HySolver.CanSolve = True
        self.Blocco.ColumnFlowsheet.Run()
        esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus 
        while esecuzione:
            time.sleep(0.5)
            esecuzione = self.Blocco.ColumnFlowsheet.SolvingStatus
        Status=self.Blocco.ColumnFlowsheet.CfsConverged
        if Status == True:
            T_dis_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-Dist@COL1").FormationFlag
            T_reflx_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-Reflux@COL1").FormationFlag
            T_2cond_calc=self.Simulazione.UtilityObjects.Item("CO2 Freeze Out-To Condenser@COL1").FormationFlag
            if T_dis_calc == 1 or T_reflx_calc==1 or T_2cond_calc==1:
                Status=False
        return Status
