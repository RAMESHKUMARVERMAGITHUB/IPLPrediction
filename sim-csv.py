import pandas as pd  
import random
import glob

files = pd.read_csv('probability.csv')  #Reading from the probability file 
DBat = {}
DBall = {}
for i in range(len(files)):
    batname = files.loc[i].BatName.strip()     #Keys of dictionary are batsman name and values are cluster number
    DBat[batname] = files.loc[i].BatclustNo
    bowlname = files.loc[i].BowlName.strip()   #Keys of dictionary are bowler name and values are cluster number
    DBall[bowlname] = files.loc[i].BowlclustNo

ip = pd.read_csv('lineup.csv')                      #Has the player names for both team 1 and team 2
team1 = [];team2 = []
for i in ip.Team1:
    team1.append(i)
for i in ip.Team2:
    team2.append(i)

runs1=0
runs2=0
wickets1=0
wickets2=0

cp = pd.read_csv('cp1.csv')       #Contains the cluster probabilities
cm = pd.DataFrame(columns=['BatclustNo','BowlclustNo','0s', '1s', '2s', '3s', '4s',  '6s','Out']) #Creating a copy of cp dataframe
# for i in range(len(cp)):
#     cm.loc[i] = [None for n in range(9)]
#     cm.loc[i].BatclustNo = cp.loc[i].BatclustNo	       
#     cm.loc[i].BowlclustNo = cp.loc[i].BowlclustNo
#     cm.loc[i]['0s'] = float(cp.loc[i]['0s'])                            #Finding cumulative probabilities
#     cm.loc[i]['1s'] = float(cp.loc[i]['1s']) + float(cp.loc[i]['0s'])
#     cm.loc[i]['2s'] = float(cp.loc[i]['2s']) + float(cm.loc[i]['1s'])
#     cm.loc[i]['3s'] = float(cp.loc[i]['3s']) + float(cm.loc[i]['2s'])
#     cm.loc[i]['4s'] = float(cp.loc[i]['4s']) + float(cm.loc[i]['3s'])
#     cm.loc[i]['6s'] = float(cp.loc[i]['6s']) + float(cm.loc[i]['4s'])
#     cm.loc[i].Out = 1
for i in range(len(cp)):
    cm.loc[i, 'BatclustNo'] = cp.loc[i, 'BatclustNo']
    cm.loc[i, 'BowlclustNo'] = cp.loc[i, 'BowlclustNo']
    cm.loc[i, '0s'] = float(cp.loc[i, '0s'])
    cm.loc[i, '1s'] = float(cp.loc[i, '1s']) + float(cp.loc[i, '0s'])
    cm.loc[i, '2s'] = float(cp.loc[i, '2s']) + float(cm.loc[i, '1s'])
    cm.loc[i, '3s'] = float(cp.loc[i, '3s']) + float(cm.loc[i, '2s'])
    cm.loc[i, '4s'] = float(cp.loc[i, '4s']) + float(cm.loc[i, '3s'])
    cm.loc[i, '6s'] = float(cp.loc[i, '6s']) + float(cm.loc[i, '4s'])
    cm.loc[i, 'Out'] = 1


def getScore(batsman,bowler):
    ptr = random.random()          #Generating random number between 0.0 and 1
    prob = cm.loc[cm['BatclustNo'] == batsman].loc[cm['BowlclustNo'] == bowler]
    if ptr <= float(prob['0s']):                         #Checking if the random number is less than or equal to
        return 0				     #the cumulative probability,If yes then return the runs
    elif  ptr <= float(prob['1s']):                      #Thus the runs scored for that ball is returned
        return 1
    elif ptr <= float(prob['2s']):
        return 2
    elif ptr <= float(prob['3s']):
        return 3
    elif  ptr <= float(prob['4s']):
        return 4
    elif ptr <= float(prob['6s']):
        return 6
    else:
        return -1	

def clusterBat(batsman):
    return DBat.get(batsman,2)                 #Get cluster number for batsman
def clusterBowl(bowler):                                             
    return DBall.get(bowler,0)                 #Get cluster number for bowler

def innings1(team1, team2):
    f = open("team1.csv", 'w')                #Outputting Team1's innings
    f.write('overs')
    f.write(',')
    f.write('score')
    f.write(',')
    f.write('Batsman')
    f.write(',')
    f.write('Non-Strike Batsman')
    f.write(',')
    f.write('Bowler')
    f.write(',')
    f.write('Runs')
    f.write('\n')

    striker = team1[0]
    runner = team1[1]
    bowler = team2[len(team2)-1]                   #Bowlers are always the last players of the team
    count = 2
    nextBatsman = 2
    wickets = 0
    over = 0
    runs = 0
    while over < 20 and wickets < 10:
        ball = 1
        over += 1
        f.write(str(over)+'.'+str(ball))
        f.write(',')
        f.write(str(runs)+'/'+str(wickets))
        f.write(',')
        f.write(str(striker))
        f.write(',')
        f.write(str(runner))
        f.write(',')
        f.write(str(bowler))
        f.write(',')
        while ball < 6 and wickets < 10:
            score = getScore(clusterBat(striker), clusterBowl(bowler))    #Get runs scored for that ball
            if score == 99:
                runs += 1
            else:
                ball += 1
                if score == -1:                                  #Score = -1 if batsman is out
                    wickets += 1
                    striker = team1[nextBatsman]
                    nextBatsman = (nextBatsman + 1) % 11       #Getting next batsman as the new striker
                    f.write(str(runs))
                else:
                    runs += score
                    f.write('out')
                    if score == 1 or score == 3:
                        striker, runner = runner, striker
        f.write('\n')
        striker, runner = runner, striker                 #Interchange striker and runner after end of over
        bowler = team2[len(team2)-count]                      #Getting next bowler
        count = (count + 1) % 5 + 1          
    f.close()
    return runs, wickets

def innings2(team1, team2, runs1):
    f = open("team2.csv", 'w')                          #Outputting Team2's innings
    f.write('overs')
    f.write(',')
    f.write('score')
    f.write(',')
    f.write('Batsman')
    f.write(',')
    f.write('Non-Strike Batsman')
    f.write(',')
    f.write('Bowler')
    f.write(',')
    f.write('Runs')
    f.write('\n')
    striker = team1[0]
    runner = team1[1]
    bowler = team2[len(team2)-1]                       #Bowlers are always the last players of the team
    count = 2
    nextBatsman = 2
    wickets = 0
    over = 0
    runs = 0
    while wickets < 10 and over < 20:
        ball = 1
        over += 1
        f.write(str(over)+'.'+str(ball))
        f.write(',')
        f.write(str(runs)+'/'+str(wickets))
        f.write(',')
        f.write(str(striker))
        f.write(',')
        f.write(str(runner))
        f.write(',')
        f.write(str(bowler))
        f.write(',')
        while ball < 6 and runs <= runs1 and  wickets < 10:
            score = getScore(clusterBat(striker), clusterBowl(bowler))    #Get runs scored for that ball
            if score == 99:
                runs += 1
            else:
                ball += 1
                if score == -1:                                  #Score = -1 if batsman is out
                    wickets += 1
                    striker = team1[nextBatsman]
                    nextBatsman = (nextBatsman + 1) % 11        #Getting next batsman as the new striker
                    f.write(str(runs))
                else:
                    runs += score
                    f.write('out')
                    if score == 1 or score == 3:
                        striker, runner = runner, striker
        f.write('\n')
        striker, runner = runner, striker                                  #Interchange striker and runner after end of over
        bowler = team2[len(team2)-count]                                     #Getting next bowler
        count = (count + 1) % 5 + 1
    f.close()
    return runs, wickets

def result(runs1, runs2, wickets2):
    if runs1 == runs2:
        print('Match was a tie!')
    elif runs1 > runs2:
        print('Team1 won by '+str(runs1-runs2)+' runs')
    else:
        print('Team2 won by '+str(10-wickets2)+' wickets')

runs1, wickets1 = innings1(team1, team2)
runs2, wickets2 = innings2(team2, team1, runs1)
print('Team1 : '+str(runs1)+'/'+str(wickets1))
print('Team2 : '+str(runs2)+'/'+str(wickets2))
result(runs1, runs2, wickets2)
