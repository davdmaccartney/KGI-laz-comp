import os
import numpy as np
from laspy.file import File
import time
import easygui
from imutils import paths
import fnmatch
import sys

MinGPS=0
MaxGPS=500000
MinClass=0
MaClass=2
D1 =0
D2 =0

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% ".format( "#"*block + "-"*(barLength-block), int(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()



dirname1 = easygui.diropenbox(msg=None, title="Please select the source directory", default=None )
total_con=len(fnmatch.filter(os.listdir(dirname1), '*.laz'))
D1 = str(total_con)
msg = str(total_con) +" files do you want to continue?"
title = "Please Confirm"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)

dirname2 = easygui.diropenbox(msg=None, title="Please select the folder to compare", default=None )
total_con=len(fnmatch.filter(os.listdir(dirname2), '*.laz'))
D2 = str(total_con)
msg = str(total_con) +" files do you want to continue?"
title = "Please Confirm"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)

if D1 != D2:
   easygui.msgbox('The process will end not the same number of files to compare')
   exit(0)
   
file_Dir1 = os.path.basename(dirname1)
file_Dir2 = os.path.basename(dirname2)

if dirname1 == dirname2:
   easygui.msgbox('The process will end same folder to compare')
   exit(0)

ci=0
cls()
eR=0

f = open(dirname1+"\Comp-result.txt", "w")

for filename in os.listdir(dirname1):
     if filename.endswith(".laz"):
        ci  += 1

        inFile1 = File(dirname1+'\\'+filename, mode='r')
        
        try:
           inFile2 = File(dirname2+'\\'+filename, mode='r')
        except OSError:
           easygui.msgbox('No file:'+filename+' in :'+dirname2+' the process will end')
           sys.exit(0) 

       
        scale1 = inFile1.header.scale
        scale2 = inFile2.header.scale

        offset1 = inFile1.header.offset
        offset2 = inFile2.header.offset
        

        points1 = inFile1.get_points()
        points_number1 = len(points1)

        points2 = inFile2.get_points()
        points_number2 = len(points2)

   
        pointmin1 = np.amin(inFile1.gps_time)
        pointmax1 = np.amax(inFile1.gps_time)

        pointmin2 = np.amin(inFile2.gps_time)
        pointmax2 = np.amax(inFile2.gps_time)


        classmin1 = np.amin(inFile1.classification)
        classmax1 = np.amax(inFile1.classification)

        classmin2 = np.amin(inFile2.classification)
        classmax2 = np.amax(inFile2.classification)

 #       compare what ever you want and write the result in a txt file
 #        bad = 1
        update_progress(ci/int(D1))

        if points_number1  !=  points_number2:
           eR=eR+1
           Nbrpoints = points_number2 - points_number1
           f.write(filename+' : '+str(Nbrpoints)+'\n')
           f.flush

        inFile1.close()
        inFile2.close()

cls()
f.close() 
if eR>0:
   print('Process finnihed :'+str(eR)+' errors read Comp-result.txt in the source folder')
else:
   print('Process finnihed with no errors')
   os.remove(dirname1+'\\Comp-result.txt')

exit(0)