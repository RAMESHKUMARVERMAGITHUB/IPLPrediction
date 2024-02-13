from flask import Flask, render_template
import pandas as pd  
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Read data
    files = pd.read_csv('probability.csv')
    DBat = {}
    DBall = {}
    for i in range(len(files)):
        batname = files.loc[i].BatName.strip()
        DBat[batname] = files.loc[i].BatclustNo
        bowlname = files.loc[i].BowlName.strip()
        DBall[bowlname] = files.loc[i].BowlclustNo
    
    ip = pd.read_csv('lineup.csv')
    team1 = list(ip.Team1)
    team2 = list(ip.Team2)

    # Simulate cricket match
    runs1, wickets1 = innings1(team1, team2)
    runs2, wickets2 = innings2(team2, team1, runs1)

    # Determine match result
    result_text = ""
    if runs1 == runs2:
        result_text = "Match was a tie!"
    elif runs1 > runs2:
        result_text = f"Team1 won by {runs1 - runs2} runs"
    else:
        result_text = f"Team2 won by {10 - wickets2} wickets"

    return render_template('index.html', runs1=runs1, wickets1=wickets1, runs2=runs2, wickets2=wickets2, result=result_text)

def innings1(team1, team2):
    # Your innings1 logic here
    pass

def innings2(team1, team2, runs1):
    # Your innings2 logic here
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
