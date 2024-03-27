from Funzioni import InserimentoComposizione, Colonna, AspenHYSYS
import numpy as np
import time
import math
import json
#### Chiamata alla funzione e recupero dei risultati
simulation_file = r"C:\Users\galloni\OneDrive - unibs.it\UNI\Articolo_energies\Articolo_energies.hsc"
aspen=AspenHYSYS(simulation_file)
HySolver, Stream, Blocchi, Simulazione = aspen.open_simulation() 
HySolver.CanSolve = False
if Stream is not None:  
    print("Apertura di Aspen HYSYS riuscita.")
else:
    print("Errore durante l'apertura di Aspen HYSYS.")

#! Definizione inziale delle variabili
i=1
data=[]
ComposizioneBottomV=[]
T=np.linspace(-50,-60,1)
RR=np.linspace(1.5,3,1)
NStadi =np.linspace(15,30,1)
Comp=Blocchi.Item("CompressoreBG")
Colonn=Blocchi.Item("T-100")
#! Definizione delle composizioni iniziali
IntialComposition = [[0.6,0.36,0.02,0.02],[0.5,0.46,0.02,0.02],[0.5,0.43,0.05,0.02],[0.5,0.43,0.02,0.05]]
for comp in IntialComposition:
    InserimentoComposizione(Stream).inserimento(comp)
    run_colonna=Colonna(Colonn,HySolver,Simulazione,Stream,Comp)
    for Temp in T:   
        for RRs in RR:
            run_colonna.RefluxRatio(RRs)
            Status=False
            while Status==False and Temp>(Temp-1):                                                       #* Sto valutando l'effetto della temperatura in maniera isolata
                run_colonna.Temp(Temp)
                Qreb, QCond, Status, Q_Comp_BG, W_Comp_BG =run_colonna.RunColonna()
                Temp=Temp-0.1
            if Status == False:
                    Composizione=None
                    Qreb=None
                    QCond=None
                    Distillato=None
                    T_in=None
                    ComposizioneBottom=None
                    Q_Comp_BG=None
                    W_Comp_BG=None
            else:
                Distillato=run_colonna.DistMoleFlow()   
                T_in=math.ceil(Temp)
                Composizione=run_colonna.CompDistillato()
                ComposizioneBottom=run_colonna.CompBottom()
                Q_Comp_BG=run_colonna.ConsumiReb()
                W_Comp_BG=run_colonna.ConsumiCond()
                
            data.append({"Q_Condenser": QCond,"Q_Reboiler":Qreb,"Composizioni Finali":Composizione, "Temperature":T_in,"Reflux Ratio":RRs, "Distillato":Distillato,"Comp iniziale":comp,"CompBott":ComposizioneBottom,"Q Comp":Q_Comp_BG,"W Comp":W_Comp_BG})
    with open("Dati Composizione"+str(i)+".json", "w") as json_file:
        for item in data:
            json.dump(item, json_file)
            json_file.write('\n')
    data=[]
    i+=1

