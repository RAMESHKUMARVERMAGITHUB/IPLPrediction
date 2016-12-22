import pandas as pd
import glob
final = pd.DataFrame(columns=['BatName','BowlName', '0s', '1s', '2s', '3s', '4s',  '6s','Out','BatclustNo','BowlclustNo','clustno'])
batfiles = sorted(glob.glob("BattingCluster/*.csv"))
bowlfiles = sorted(glob.glob("BowlingCluster/*.csv"))
prob_df = pd.read_csv('probability.csv') #or probability.csv

prob_df = prob_df.loc[prob_df['BatName']  != 'AN Ahmed']
prob_df = prob_df.loc[prob_df['BowlName']  != 'AN Ahmed']

dicbat = {}
dicball = {}
for i in range(len(batfiles)):
	dfbat = pd.read_csv(batfiles[i])           #Keys of dictionary are batsman name and values are cluster number
	dfbowl = pd.read_csv(bowlfiles[i])
	for j in range(len(dfbat)):
		batname = dfbat.loc[j].Name.strip()
		dicbat[batname] = i
	for j in range(len(dfbowl)):
		bowlname = dfbowl.loc[j].Name.strip()    #Keys of dictionary are bowler name and values are cluster number
		dicball[bowlname] = i
BatmanNames = list(dicbat.keys())
BowlerNames = list(dicball.keys())

c=0
print(prob_df.index)
for l in range(len(prob_df)):
	batname = prob_df.loc[l].BatName.strip()
	batlastname = batname.split()[-1]
	for lbat in range(len(BatmanNames)):
		if batlastname in BatmanNames[lbat] and (batname[0] == BatmanNames[lbat][0] or batname[1] == BatmanNames[lbat][0]):
			batname = BatmanNames[lbat]    #Check if the names in cluster and names in probability.csv file match
	bowlname =  prob_df.loc[l].BowlName.strip()    #For batmsan
	bowlastname = bowlname.split()[-1]
	for lbowl in range(len(BowlerNames)):
		if bowlastname in BowlerNames[lbowl] and (bowlname[0] == BowlerNames[lbowl][0] or bowlname[1] == BowlerNames[lbowl][0]):
			bowlname = BowlerNames[lbowl]   #Check if the names in cluster and names in probability.csv file match 
	final.loc[c] = [None for n in range(12)]         #For bowler
	final.loc[c].BatName = batname
	final.loc[c].BowlName = bowlname
	final.loc[c]['0s'] = prob_df.loc[l]['0s']
	final.loc[c]['1s'] = prob_df.loc[l]['1s']
	final.loc[c]['2s'] = prob_df.loc[l]['2s']
	final.loc[c]['3s'] = prob_df.loc[l]['3s']
	final.loc[c]['4s'] = prob_df.loc[l]['4s']
	#final.loc[c]['5s'] = prob_df.loc[l]['5s']
	final.loc[c]['6s'] = prob_df.loc[l]['6s']
	#final.loc[c]['7+'] = prob_df.loc[l]['7+']
	final.loc[c].Out = prob_df.loc[l].Out
	print dicbat[batname],dicball[bowlname],c 
	final.loc[c].BatclustNo = dicbat[batname]
	final.loc[c].BowlclustNo = dicball[bowlname]
	if(dicbat[batname] == dicball[bowlname]):
	 	print('Yes')
	 	final.loc[c].clustno = dicbat[batname]#dfbat.loc[j].clustNo
	else:
	 	print('Oops')
	 	final.loc[c].clustno = -1
	c += 1


# c = 0
# for i in range(len(batfiles)):
# 	dfbat = pd.read_csv(batfiles[i])
# 	dfbowl = pd.read_csv(bowlfiles[i])
# 	for j in range(len(dfbat)):
# 		batname = dfbat.loc[j].Name
# 		for k in range(len(dfbowl)):
# 			bowlname = dfbowl.loc[k].Name
# 			print(batname,bowlname)
# 			for l in range(len(prob_df)):
# 				if(prob_df.loc[l].BatName == batname and prob_df.loc[l].BowlName == bowlname):
# 					print('Yes')
# 					final.loc[c].BatName = batname
# 					final.loc[c].BowlName = bowlname
# 					final.loc[c].clustNo = dfbat.loc[j].clustNo
# 					final.loc[c]['0s'] = prob_df.loc[l]['0s']
# 					final.loc[c]['1s'] = prob_df.loc[l]['1s']
# 					final.loc[c]['2s'] = prob_df.loc[l]['2s']
# 					final.loc[c]['3s'] = prob_df.loc[l]['3s']
# 					final.loc[c]['4s'] = prob_df.loc[l]['4s']
# 					final.loc[c]['5s'] = prob_df.loc[l]['5s']
# 					final.loc[c]['6s'] = prob_df.loc[l]['6s']
# 					final.loc[c]['7+'] = prob_df.loc[l]['7+']
# 					c += 1
final.to_csv('cluster_pairs1.csv')
