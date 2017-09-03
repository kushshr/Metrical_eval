import os
import re
import numpy as np

SIZE = 500
#Copy in madmom/bin and run
idx1 = np.zeros(SIZE)
time1 = np.zeros(SIZE)
idx2= np.zeros(SIZE)
time2=np.zeros(SIZE)
TotalTime=np.zeros(SIZE)

command = "/home/kushagra/new/MetricalLevel"
for root, dirs, files in os.walk(str(command)):
	for f in files:
		x = f.strip('.meterlevel')
		xx = x.strip('percussion_')
		array1 = []
		array2 = []
		array3 = []
		#with open(str(command) + "/" + str(f), 'r') as foo:
		foo = open(str(command) + "/" + str(f), 'r')
		for line in foo:
			spl = line.split("   ")
			array1.insert(len(array1),line[-2:])
			array2.insert(len(array2),line[0:6])

		for i in range(0,len(array1)):
			if (array1[i] == '1\n'):
				zz = array2[i].strip('\t')

				array3.insert(len(array3),i)
				
				
		for	root, dirs, files in os.walk(str("/home/kushagra/new/Beat")):
			for xxxx in files:
				if xxxx.strip('.beats') == x:
					print xxxx
					array4 = []
					array5 = []
					foo1 = open(str("/home/kushagra/new/Beat") + "/" + str(xxxx), 'r')
					for line in foo1:
						spl = line.split("   ")
						array4.insert(len(array4),line[-2:])
						array5.insert(len(array4),line[0:6])
						

					thefile = open('temp/test_'+ str(x) + ".txt"  , 'wb')

					for item in array3:
						zzz = array5[int(item)].strip('\n')
						thefile.write("%s \n" % zzz )
					thefile.close()		


"""		
		xx = int(xx)
		idx1[xx-1] = int(i)
		time1[xx-1] = array2[i]
		print i, array2[i]
"""
		

		#xy =  "./beat_eval.py -o Eval/result_" + str(x) + ".json " + "Ballroom_Results/" + str(x) +".beats " + "Tempp/test_" + str(x) + ".txt " 
	
		#os.system(xy)

"""
#./beat_eval.py -o 3.txt test_Albums-AnaBelen_Veneo-01.txt Albums-AnaBelen_Veneo-01.wav.txt

#./beat_eval.py -o Eval/result_Albums-AnaBelen_Veneo-01.json Temp/test_Albums-AnaBelen_Veneo-01.txt Ballroom_Results/Albums-AnaBelen_Veneo-01.wav.txt
""
command = "/home/kushagra/Cuidado/Master/Drums/TestAnnotations"
for root, dirs, files in os.walk(str(command)):
	for f in files:
		x = f.strip('.txt')
		array1 = []
		array2 = []
		xx = x.strip('percussion_')
		#with open(str(command) + "/" + str(f), 'r') as foo:
		foo = open(str(command) + "/" + str(f), 'r')
		for line in foo:
			spl = line.split("   ")
			array1.insert(len(array1),line[10])
			array2.insert(len(array2),line[0:6])
		for i in range(0,len(array1)-5):
			if (array1[i] == '1' and array1[i+1] == '2' and array1[i+2] == '3' and array1[i+3] == '4' and array1[i+4] == '5'):
				break;
		print array1
		xx = int(xx)
		idx2[xx-1] = int(i)
		time2[xx-1] = array2[i]
		TotalTime[xx-1] = array2[-1]
		#print i, array2[i], array2[-1]
		#print array2[-1]
		
		thefile = open('Tempp/test_'+ str(x) + ".txt"  , 'wb')
		for item in array1:
			thefile.write("%s" % item)
		thefile.close()


sumPerc = 0; 
for i in range(0,500):
	TIME1 = float(time1[i])
	TIME2 = float(time2[i])
	TOTAL = float(TotalTime[i])
	sumPerc = sumPerc + (abs(TIME1 - TIME2)/TOTAL)
	#print i, (abs(TIME1 - TIME2)/TOTAL)
xxx= time1 - time2
print xxx
print sumPerc / 500 
"""