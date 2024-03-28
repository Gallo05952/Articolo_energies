from Funzioni import InserimentoComposizione, Colonna, AspenHYSYS, CambioPressione, CambioStadi
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
T=np.linspace(-50,-70,21)
RR=np.linspace(1.4,3,9)
#RR=np.linspace(2.54,2.54,1)
NStadi =np.linspace(11,25,8)
Comp=Blocchi.Item("CompressoreBG")
Colonn=Blocchi.Item("T-100")
Pressure=np.linspace(5050,7050,5) #14
#! Definizione delle composizioni iniziali
IntialComposition = [[0.6,0.36,0.02,0.02],[0.5,0.46,0.02,0.02],[0.5,0.43,0.05,0.02],[0.5,0.43,0.02,0.05]]
for comp in IntialComposition:
    InserimentoComposizione(Stream).inserimento(comp)
    run_colonna=Colonna(Colonn,HySolver,Simulazione,Stream,Comp)
    for stadi in NStadi:
        CambioStadi(Blocchi,HySolver).CambioStadio(stadi)
        print("Cambio Stadi effettuato")
        for Temp in T:   
            limitT=Temp-1
            for RRs in RR:
                for p in Pressure:
                    CambioPressione(Blocchi).CambioP(p)
                    run_colonna.RefluxRatio(RRs)
                    Status=False
                    while Status==False and Temp>limitT:                                                       #* Sto valutando l'effetto della temperatura in maniera isolata
                        run_colonna.Temp(Temp)
                        Qreb, QCond, Status, Q_Comp_BG, W_Comp_BG =run_colonna.RunColonna()
                        print("Temperatura: ",Temp," Reflux Ratio: ",RRs," Pressione: ",p," Stadi: ",stadi," Status: ",Status)
                        if Status==False: Temp=Temp-0.1  
                        if Status==2: Status=True                
                    if Status == False or Status==2:
                            Composizione=None
                            Qreb=None
                            QCond=None
                            Distillato=None
                            T_in=None
                            ComposizioneBottom=None
                            Q_Comp_BG=None
                            W_Comp_BG=None
                            FeedStage=None
                    else:
                        Distillato=run_colonna.DistMoleFlow()   
                        T_in=math.ceil(Temp)
                        Composizione=run_colonna.CompDistillato()
                        ComposizioneBottom=run_colonna.CompBottom()
                        Q_Comp_BG=run_colonna.ConsumiReb()
                        W_Comp_BG=run_colonna.ConsumiCond()
                        FeedStage=CambioStadi(Blocchi,HySolver).FeedStage()
                
                    data.append({"Q_Condenser": QCond,"Q_Reboiler":Qreb,"Composizioni Finali":Composizione, "Temperature":T_in,"Reflux Ratio":RRs,"Pressione":p,"Numero di Sradi":stadi,"Feed Stage":FeedStage, "Distillato":Distillato,"Comp iniziale":comp,"CompBott":ComposizioneBottom,"Q Comp":Q_Comp_BG,"W Comp":W_Comp_BG})
                    time.sleep(1)
    with open("Dati Composizione1."+str(i)+".json", "w") as json_file:
        for item in data:
            json.dump(item, json_file)
            json_file.write('\n')
    data=[]
    i+=1

