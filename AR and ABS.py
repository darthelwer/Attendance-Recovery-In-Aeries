
import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
stu_id_list=[]
stu_list=[]

root=tk.Tk()
root.withdraw()

class Student(object):
    def __init__(self,ID,SCL,SN):
        self.name = self
        self.ID = ID
        self.SCL = SCL
        self.SN = SN
        self.AR_Days = []
        self.ATT_Days=[]

    def add_AR(self,DT,TM,PG):
        self.AR_Days.append([DT,TM,PG[:-1]])
    def add_ATT(self,DY):
        self.ATT_Days.append(DY)

    def printdata(self):
        print (self.ID)
        for item in self.AR_Days:
            print(item)
        print("\n")
    
def buildoutput():
    
    directory = os.path.expanduser("~/Desktop")
    filename = asksaveasfilename(
        initialdir= directory,
        filetypes=(("Comma Seperated Values", "*.csv"),("Text Files","*.txt")),
        title = "Choose where your output will be stored"
    )
    if filename[-3:].lower() == "csv":
        pass
    else:
        filename += ".csv"

    outputCSV = open(filename,"w")
    outputCSV.write("STU.ID, STU.SC, STU.SN, ATT.DY, ATT.ADA, ATT.ADT, ATT.ACO\n")
    global stu_id_list, stu_list
    prog_dict = {
        "1":"Super Summer Camp:",
        "2":"ELOP Genius Hour:",
        "100":"Saturday School",
        "200": "ELOP Genius Hour:",
        "":"Unknown:"}
    for stu in stu_list:
        if len(stu.AR_Days) > 0 and len(stu.ATT_Days) > 0:
        #checks to make sure theres data in both lists, no need to create output otherwise
            FullARDays = []
            PartialARDays =[]
            for AR in stu.AR_Days:
                #this is to turn partial days into full 4 hour days
                if int(AR[1]) >= 240:
                    FullARDays.append(["M",AR[0],prog_dict[AR[2]]+AR[0]])
                else:
                    PartialARDays.append([AR[0],AR[1],AR[2]])
                    tempmin = 0
                    for partial in PartialARDays:
                        tempmin += int(partial[1])
                    if tempmin >=240:
                        datestring = ""
                        for partial in PartialARDays:
                            datestring = datestring + partial[0] +" "
                            lastdate = partial[0]
                        FullARDays.append(["M",lastdate,prog_dict[AR[2]]+datestring])
                        PartialARDays = []
            if len(FullARDays) >= len(stu.ATT_Days):
                for i in range(len(stu.ATT_Days)):
                    outputCSV.write(str(stu.ID)+","+str(stu.SCL)+","+str(stu.SN)+","+str(stu.ATT_Days[i])+","+",".join(FullARDays[i])+"\n")
            else:
                for i in range(len(FullARDays)):
                    outputCSV.write(str(stu.ID)+","+str(stu.SCL)+","+str(stu.SN)+","+str(stu.ATT_Days[i])+","+",".join(FullARDays[i])+"\n")
    outputCSV.close()

    
def openAR():
    ### RUN THIS QUERY IN AERIES AND THEN SAVE THE OUTPUT AS CSV
    ### LIST ATD STU ATD.ID ATD.SC STU.SN ATD.DT ATD.TM ATD.SE
    global stu_id_list, stu_list
    directory = os.path.expanduser("~/Desktop")
    filename = askopenfilename(
        initialdir= directory,
        filetypes=(("Comma Seperated Values", "*.csv"),("Text Files","*.txt")),
        title = "Choose where your AR Dates are stored"
    )
    ARData= open(filename,"r")
    ARLabels = ARData.readline().split(",")
    for line in ARData:
        SL = line.split(",")
        if SL[0] not in stu_id_list:
            stu_id_list.append(SL[0])
            stu_list.append(Student(SL[0],SL[1],SL[2]))
        idx = stu_id_list.index(SL[0])
        stu_list[idx].add_AR(SL[3],SL[4],SL[5])
    ARData.close()

def openATT():
    ### RUN THIS QUERY IN AERIES AND THEN SAVE THE OUTPUT AS CSV
    ### LIST ATT STU STU.ID ATT.DY ATT.DT ATT.AL ATT.ADA ATT.ADT ATT.ACO 
    ### IF ATT.AL = 2 OR ATT.AL = A OR ATT.AL = B OR ATT.AL = E OR ATT.AL = I OR ATT.AL = J OR ATT.AL = U
    
    global stu_id_list, stu_list
    directory = os.path.expanduser("~/Desktop")
    filename = askopenfilename(
        initialdir= directory,
        filetypes=(("Comma Seperated Values", "*.csv"),("Text Files","*.txt")),
        title = "Choose where your ATT Dates are stored"
    )
    ATTData= open(filename,"r")
    ATTLabels = ATTData.readline().split(",")
    for line in ATTData:
        SL = line.split(",")
        if SL[0] not in stu_id_list:
            pass
        else:
            idx = stu_id_list.index(SL[0])
            stu_list[idx].add_ATT(SL[1])
    ATTData.close()

openAR()
openATT()
buildoutput()