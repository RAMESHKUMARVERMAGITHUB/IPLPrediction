from flask import Flask, render_template
import pandas as pd  
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Read data
    files = pd.read_csv('probability.csv')
    cp = pd.read_csv('cp1.csv')
    ip = pd.read_csv('lineup.csv')

    # Process data
    # Your data processing logic here

    # Prepare data to display on the webpage
    runs1, wickets1 = 0, 0  # Replace with your actual data
    runs2, wickets2 = 0, 0  # Replace with your actual data

    return render_template('index.html', runs1=runs1, wickets1=wickets1, runs2=runs2, wickets2=wickets2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
