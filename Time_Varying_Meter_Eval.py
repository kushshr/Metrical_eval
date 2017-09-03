import os
import re
import numpy as np
from string import maketrans

SIZE = 200
NUM_METER = 3
#Copy in madmom/bin and run
Annotation_Grid_numOccurences = np.zeros((SIZE, NUM_METER))
Annotation_Grid_TIMES = np.zeros((SIZE, NUM_METER))
Annotation_Grid_Total_Times = np.zeros(SIZE)
Output_Grid_numOccurences = np.zeros((SIZE, NUM_METER))
Output_Grid_TIMES = {}
Output_Grid_END_TIMES ={}
Output_Grid_Total_Times = np.zeros(SIZE)
METER_ARR= [0, 0, 0]
ncorrectBars =0

def count_patterns_from_array(meter,array):

# Calculate times of meter and changes
	kFlag = 0
	nOccurences =0;	
	idx =[]
	nOccurences = 0
	for i in range(0,len(array)):
		#if i ==0:
		#	if int(array[i]) == 1 and int(array[i+int(meter)]) == 1:
		#		nOccurences += 1
		#		idx.insert(len(idx), i)
		if i > 0 and i<(len(array)-1):
			if int(array[i]) == int(meter) and int(array[i+1]) == 1:
				nOccurences += 1
				idx.insert(len(idx), i + 1 - meter )
		if i == len(array) - 1:
			if int(array[i]) == int(meter):
				nOccurences += 1
				idx.insert(len(idx), i + 1 - meter)

	return idx,nOccurences



AllMeters = [7,5,4]

Total_Bars_4 = 0 
Total_Bars_5 = 0
Total_Bars_7 = 0
Total_Bars = 0
out =0
command = "/home/kushagra/Cuidado/Master/Drums/TestAnnotations"
command_out = "/home/kushagra/Beats"
for root, dirs, files in os.walk(str(command)):
	for f in files:
		x = f.strip('.beats.txt')
		xx = x.strip('percussion_')
		
		dict_Input={}
		dict_Output = {}
		Output_Grid_TIMES[xx] ={} 
		Output_Grid_END_TIMES[xx] ={}

		#Everything to be done for annotations and output both together
		#Reading beat positions and metrical positions
		
		Input_Beats = []
		Input_Metrical = []
		
		fooIn = open(str(command) + "/" + str(f), 'r')
		for line in fooIn:
			spl = line.split("   ")
			Input_Metrical.insert(len(Input_Metrical),line[10])
			Input_Beats.insert(len(Input_Beats),line[0:6])

		Output_Beats = []
		Output_Metrical = []

		fooOut = open(str(command_out) + "/" + x + '.beats.txt', 'r') 
		print f , '##############################'
		for line in fooOut:
				spl = line.split("   ")
				Output_Metrical.insert(len(Output_Metrical),line[-2])
				Output_Beats.insert(len(Output_Beats),line[0:6])

		for numb in range(0,len(Output_Beats)):
			Output_Beats[numb] = Output_Beats[numb].replace("\t", "")

		

		xx = int(xx)

		#Reading occurences of each meter and saving indices bar beginning indices in dictionary 
		for metr in AllMeters:
			templist = []
			tempList, Input_NBars = count_patterns_from_array(metr,Input_Metrical)
			dict_Input[str(metr)] = tempList

		for metr in AllMeters:
			templist = []
			tempList, OutputNBars = count_patterns_from_array(metr,Output_Metrical)
			dict_Output[str(metr)] = tempList

		#Total number of bars corresponding to each time signature
		n_4_4 = len(dict_Input['4'])
		n_5_4 = len(dict_Input['5'])
		n_7_4 = len(dict_Input['7'])
		nBars = n_4_4 + n_5_4 + n_7_4

		#Total number of bars corresponding to each time signature in the dataset
		Total_Bars_4 = Total_Bars_4 + n_4_4
		Total_Bars_5 = Total_Bars_5 + n_5_4
		Total_Bars_7 = Total_Bars_7 + n_7_4
		Total_Bars = Total_Bars + n_4_4 + n_5_4 + n_7_4


		

		## MeterInferenceEval
		overlap_meter = [] 
		overlap = 0
		for metr in AllMeters:

			#Find time slices corresponding to each time signature and place them in Meter Times list adjacent to each other
			InputDiff = []
			if len(dict_Input[str(metr)]) > 1:
				InputDiff = [dict_Input[str(metr)][n]-dict_Input[str(metr)][n-1] for n in range(1,len(dict_Input[str(metr)]))]
			
			InputMeterTimesList = []

			if (InputDiff != []):
				n = 0
				InputMeterTimesList.insert(len(InputMeterTimesList),dict_Input[str(metr)][n])
				for n in range(0,len(InputDiff)):
					if (InputDiff[n] != int(metr)) and (n!=len(InputDiff)-1) and len(InputDiff) !=1:
						InputMeterTimesList.insert(len(InputMeterTimesList),dict_Input[str(metr)][n])
						InputMeterTimesList.insert(len(InputMeterTimesList),dict_Input[str(metr)][n+1])
					if n == len(InputDiff)-1 and len(InputDiff) !=1:
						InputMeterTimesList.insert(len(InputMeterTimesList),dict_Input[str(metr)][n+1])
					if len(InputDiff) == 1:
						InputMeterTimesList.insert(len(InputMeterTimesList),dict_Input[str(metr)][1])
					

			OutputDiff = []
			if len(dict_Input[str(metr)]) >= 1:
				OutputDiff = [dict_Output[str(metr)][n]-dict_Output[str(metr)][n-1] for n in range(1,len(dict_Output[str(metr)]))]
			
			
			OutputMeterTimesList = []

			if (OutputDiff != []):
				n = 0
				OutputMeterTimesList.insert(len(OutputMeterTimesList),dict_Output[str(metr)][n])
				for n in range(0,len(OutputDiff)):
					if OutputDiff[n] != int(metr) and  n!=len(OutputDiff)-1 and len(OutputDiff)!=1:
						OutputMeterTimesList.insert(len(OutputMeterTimesList),dict_Output[str(metr)][n])
						OutputMeterTimesList.insert(len(OutputMeterTimesList),dict_Output[str(metr)][n+1])
					if n == len(OutputDiff)-1 and len(OutputDiff)!=1:
						OutputMeterTimesList.insert(len(OutputMeterTimesList),dict_Output[str(metr)][n+1])
					if len(OutputDiff) == 1:
						OutputMeterTimesList.insert(len(OutputMeterTimesList),dict_Output[str(metr)][n])
			
			#print InputMeterTimesList
			#print OutputMeterTimesList
			#Find intersection among lines - do through time, not bars
			for k in range(0,len(OutputMeterTimesList),2): 
					for l in range(0,len(InputMeterTimesList),2):
						start1 = float(Input_Beats[int(InputMeterTimesList[l])])
						start2 = float(Output_Beats[int(OutputMeterTimesList[k])])
						end1 = float(Input_Beats[int(InputMeterTimesList[l+1])])
						end2 = float(Output_Beats[int(OutputMeterTimesList[k+1])])
						#print type(start1), start1, end1,  start2, end2 
						if (start2>end1) | (end2<start1):
							overlap = overlap + 0
						elif (start2>start1 and end2>end1): 
							overlap = overlap + end1 - start2
						elif (start2>start1 and end2<end1):
							overlap = end2 - start2
						elif (start1>start2 and end2>end1):
							overlap = overlap + end1 - start1
						elif (start1>start2 and end1>end2):
							overlap = overlap + end2 - start1
						
						 
						
			
			Input_Beats = map(float, Input_Beats)

			beat_distances = np.zeros(len(Input_Beats))
			
			#For bar inference eval
			correctBars = 0 

			for pos_beats in dict_Output[str(metr)]:
				print dict_Output[str(metr)]
				bar_success = 1;
				for metLevel in range(0,metr):
					yyy = Output_Beats[pos_beats + metLevel]
					new_list = [xxxx - float(yyy) for xxxx in Input_Beats]
					new_list = map(abs, new_list)
					nearest = new_list.index(min(new_list))
            		#min_difference = beat_differences[nearest]
	        		print metLevel, nearest, metr
	        		print  type(Input_Metrical[nearest]) , type(metLevel)
	        		if((int(Input_Metrical[nearest]) == metLevel+1)):# or absolute_error>0.07):
	        			bar_success = 1
	        			print 'gotch'
	        		else:
	        			bar_success = 0

	        	if bar_success == 1:
	        		correctBars = correctBars + 1

	        ncorrectBars = ncorrectBars + correctBars

		#Take FMEasure code from mir-eval

		#Confusion Matrix
		#Find overlap between bars of 4/4 identified as 5/4
		
		
		number_of_beats = len(Input_Beats)
		average_tempo = (float(Input_Beats[-1]) - float(Input_Beats[0])) / number_of_beats

		print overlap, correctBars
		overlap_bars = overlap / (average_tempo*int(metr))
		#print average_tempo, overlap_bars
		#print overlap_bars/nBars,nBars, correctBars
		out = out + (overlap_bars/nBars)
		#Fmeasure 
	
	ncorrectBars = ncorrectBars + correctBars


print 'lask', out	, ncorrectBars, Total_Bars




