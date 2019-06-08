# deepsalsa.py a bunch of funcitons to analyze the data of the deel salsa experiment

from os import listdir

def get_all_songnames(dir):
#get the songs on the directory
#make a dictionary with song names as keys and annotators as subjects
	name_list=listdir(dir)
	song_annotator_dictionary={}
	for name in name_list:
		if name.split("-")[0] not in song_annotator_dictionary: #check if key is already in dict
			song_annotator_dictionary[name.split("-")[0]]=[name.split("-")[1].split(".")[0]]
		else:
			song_annotator_dictionary[name.split("-")[0]].append(name.split("-")[1].split(".")[0])

	#print song_annotator_dictionary # this dict contains songnames and annotator ids
	return song_annotator_dictionary


def extract_annotations_from_song(song_name, name_list):
	song_annotations=[]
	for annotator in name_list[song_name]:
		
		annotation_file=song_name+"-"+annotator+".txt"
		annotation=[]
		annotation.append(int(annotator))
		print annotation_file
		with open("data/"+annotation_file) as timeline:
			for line in timeline:
				line=line.split(" ")
			for time in line:
				#print float(time)
				timefloat=float(time)
				annotation.append(float(timefloat))
		song_annotations.append(annotation)
	triad_list=[]
	minimum_list=min(len(song_annotations[0]),len(song_annotations[1]), len(song_annotations[2]))
	for data1 in range(minimum_list):
		for data2 in range(minimum_list):
			for data3 in range(minimum_list):

				#find if all three annotations are closer by less than 500ms
				if abs(song_annotations[0][data1]-song_annotations[1][data2])<0.5 and abs(song_annotations[0][data1]-song_annotations[2][data3])<0.5: 
					dispersion=max([song_annotations[0][data1],song_annotations[1][data2], song_annotations[2][data3]])-min([song_annotations[0][data1],song_annotations[1][data2], song_annotations[2][data3]])
					if dispersion<0.2:
						triad_list.append([song_annotations[0][data1],song_annotations[1][data2], song_annotations[2][data3]])
	for triad in triad_list:
		dispersion=max(triad)-min(triad)
		print triad, "dispersion:", dispersion



name_list=get_all_songnames("data") #process all annotated songs in data folder
extract_annotations_from_song("1", name_list)#extract annotations from song 1