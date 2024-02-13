from flask import Flask, render_template_string
import pandas as pd  
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Reading data from files
    files = pd.read_csv('probability.csv')
    ip = pd.read_csv('lineup.csv')
    cp = pd.read_csv('cp1.csv')

    # Initializing variables
    DBat = {files.loc[i].BatName.strip(): files.loc[i].BatclustNo for i in range(len(files))}
    DBall = {files.loc[i].BowlName.strip(): files.loc[i].BowlclustNo for i in range(len(files))}
    team1 = [ip.Team1[i] for i in range(len(ip.Team1))]
    team2 = [ip.Team2[i] for i in range(len(ip.Team2))]
    cm = pd.DataFrame(columns=['BatclustNo','BowlclustNo','0s', '1s', '2s', '3s', '4s',  '6s','Out'])
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

    # Function to get score
    def getScore(batsman, bowler):
        ptr = random.random()
        prob = cm.loc[cm['BatclustNo'] == batsman].loc[cm['BowlclustNo'] == bowler]
        if ptr <= float(prob['0s']):
            return 0
        elif ptr <= float(prob['1s']):
            return 1
        elif ptr <= float(prob['2s']):
            return 2
        elif ptr <= float(prob['3s']):
            return 3
        elif ptr <= float(prob['4s']):
            return 4
        elif ptr <= float(prob['6s']):
            return 6
        else:
            return -1	

    # Function to get cluster number for batsman
    def clusterBat(batsman):
        return DBat.get(batsman, 2)

    # Function to get cluster number for bowler
    def clusterBowl(bowler):
        return DBall.get(bowler, 0)

    # Function for Team 1 innings
    def innings1(team1, team2):
        f = open("team1.csv", 'w')
        f.write('overs,score,Batsman,Non-Strike Batsman,Bowler,Runs\n')

        striker = team1[0]
        runner = team1[1]
        bowler = team2[len(team2)-1]
        count = 2
        nextBatsman = 2
        wickets = 0
        over = 0
        runs = 0
        while over < 20 and wickets < 10:
            ball = 1
            over += 1
            f.write(f"{over}.{ball},{runs}/{wickets},{striker},{runner},{bowler},")
            while ball < 6 and wickets < 10:
                score = getScore(clusterBat(striker), clusterBowl(bowler))
                if score == 99:
                    runs += 1
                else:
                    ball += 1
                    if score == -1:
                        wickets += 1
                        striker = team1[nextBatsman]
                        nextBatsman = (nextBatsman + 1) % 11
                        f.write(f"{runs}\n")
                    else:
                        runs += score
                        f.write("out" if score == 1 or score == 3 else "")
                        if score == 1 or score == 3:
                            striker, runner = runner, striker
        f.close()
        return runs, wickets

    # Function for Team 2 innings
    def innings2(team1, team2, runs1):
        f = open("team2.csv", 'w')
        f.write('overs,score,Batsman,Non-Strike Batsman,Bowler,Runs\n')

        striker = team1[0]
        runner = team1[1]
        bowler = team2[len(team2)-1]
        count = 2
        nextBatsman = 2
        wickets = 0
        over = 0
        runs = 0
        while wickets < 10 and over < 20:
            ball = 1
            over += 1
            f.write(f"{over}.{ball},{runs}/{wickets},{striker},{runner},{bowler},")
            while ball < 6 and runs <= runs1 and wickets < 10:
                score = getScore(clusterBat(striker), clusterBowl(bowler))
                if score == 99:
                    runs += 1
                else:
                    ball += 1
                    if score == -1:
                        wickets += 1
                        striker = team1[nextBatsman]
                        nextBatsman = (nextBatsman + 1) % 11
                        f.write(f"{runs}\n")
                    else:
                        runs += score
                        f.write("out" if score == 1 or score == 3 else "")
                        if score == 1 or score == 3:
                            striker, runner = runner, striker
        f.close()
        return runs, wickets

    # Function to calculate result
    def result(runs1, runs2, wickets2):
        if runs1 == runs2:
            return 'Match was a tie!'
        elif runs1 > runs2:
            return f'Team1 won by {runs1 - runs2} runs'
        else:
            return f'Team2 won by {10 - wickets2} wickets'

    # Innings and match result
    runs1, wickets1 = innings1(team1, team2)
    runs2, wickets2 = innings2(team2, team1, runs1)
    match_result = result(runs1, runs2, wickets2)

    # Return HTML template with data
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>IPL Prediction</title>
        </head>
        <body>
            <h1>IPL Prediction Results</h1>
            <h2>Team 1</h2>
            <p>Runs: {{ runs1 }}</p>
            <p>Wickets: {{ wickets1 }}</p>
            <h2>Team 2</h2>
            <p>Runs: {{ runs2 }}</p>
            <p>Wickets: {{ wickets2 }}</p>
            <h2>Match Result</h2>
            <p>{{ match_result }}</p>
        </body>
        </html>
        """,
        runs1=runs1, wickets1=wickets1, runs2=runs2, wickets2=wickets2, match_result=match_result
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
