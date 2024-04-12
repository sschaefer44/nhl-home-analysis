#This code never got used in the finished product as I implimented Pandas. Origionally, I was planning to write this program
#only using standard python libraries, but it became ineficient so I decided to utilize Pandas instead.


#Reads csv and fills array
import numpy as np
import pandas as pd
import csv
import math
def read_csvfile(file):
    team = []
    date = []
    win = []
    loss = []
    ot = []
    points = []
    RW = []
    ROW = []
    SOW = []
    goals = []
    goals_against = []
    power_play = []
    penalty_kill = []
    net_ppp = []
    net_pkp = []
    shots = []
    shots_against = []
    FOWp = []

    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Append each value to its respective list
            team.append(row['team'])
            date.append(row['date'])
            win.append(int(row['win']))
            loss.append(int(row['loss']))
            ot.append(int(row['ot']))
            points.append(int(row['points']))
            RW.append(int(row['RW']))
            ROW.append(int(row['ROW']))
            SOW.append(int(row['SOW']))
            goals.append(int(row['goals']))
            goals_against.append(int(row['goals_against']))
            
            # Handling float conversion with error handling

            try:
                power_play.append(float(row['power_play']))
            except ValueError:
                power_play.append(None)
            
            try:
                penalty_kill.append(float(row['penalty_kill']))
            except ValueError:
                penalty_kill.append(None)
            
            try:
                net_ppp.append(float(row['net_ppp']))
            except ValueError:
                net_ppp.append(None)
            
            try:
                net_pkp.append(float(row['net_pkp']))
            except ValueError:
                net_pkp.append(None)
            
            try:
                shots.append(float(row['shots']))
            except ValueError:
                shots.append(None)
            
            try:
                shots_against.append(float(row['shots_against']))
            except ValueError:
                shots_against.append(None)
            
            try:
                FOWp.append(float(row['FOWp']))
            except ValueError:
                FOWp.append(None)

    return team, date, points, win, loss, ot, RW, ROW, SOW, goals, goals_against, power_play, penalty_kill, net_ppp, net_pkp, shots, shots_against, FOWp

#Determine if a game is home or away - Puts every home index into an array and the same for away
def home_or_away(team_arr, date_arr, team_name):
    home_inds = []
    away_inds = []
    for i in range(len(team_arr)):
         if team_arr[i] == team_name:
            if "@" in date_arr[i]:
                away_inds.append(i)
            else:
                home_inds.append(i)
    return home_inds, away_inds

#Calculate total wins, losses, and overtime losses. Returns wins, losses, overtime, and the total points the team earned.
def calcRecord(haGameArr, lossList, otList):
    wins = 0
    losses = 0
    OTL = 0
    totPoints = 0
    for i in range(len(haGameArr)):
        if lossList[haGameArr[i]] == 1:
            losses += 1
        elif otList[haGameArr[i]] == 1:
            wins += 1
            totPoints += 2
        else:
            OTL += 1
            totPoints += 1

    return wins, losses, OTL, totPoints

#Calculates the mean of a statistic
def mean_of_stat(stat_Array, gameArray):
    mean = 0
    sum = 0
    n = len(gameArray)
    for i in range(n):
        sum += stat_Array[gameArray[i]]
    mean = sum/n
    return mean

#Sums an array
def sum_array(stat_Array, gameArray):
    sum = 0
    for i in range(len(gameArray)):
        sum += stat_Array[gameArray[i]]
    return sum

def standard_dev_of_stat(stat_Array, gameArray):
    arr = []
    sum = 0
    count = 0
    mean = mean_of_stat(stat_Array, gameArray)
    for i in range(len(gameArray)):
        sum += math.pow(stat_Array[gameArray[i]] - mean, 2)
        count += 1
    return(math.sqrt(sum/count))

#Stat1 will be mean of stat at home using gameArray1, stat2 will be mean of stat at away using gameArray2
def calc_linear_regression(stat_Array, gameArray1, gameArray2):
    sumX = sumY = sumXX = sumXY = 0
    n = min(len(gameArray1), len(gameArray2))

    for i in range(n):
        hValue = stat_Array[gameArray1[i]]
        aValue = stat_Array[gameArray2[i]]
        sumX += hValue
        sumY += aValue
        sumXX += hValue ** 2
        sumXY += hValue * aValue

    hMean = sumX / n
    aMean = sumY / n

    b = (sumXY - n * hMean * aMean) / (sumXX - n * hMean ** 2)
    a = aMean - b * hMean
    return a, b 


# Determine if a game is home or away
def home_or_away(df, team_name):
    home_games = df[df['team'] == team_name].loc[~df['date'].str.contains('@')]
    away_games = df[df['team'] == team_name].loc[df['date'].str.contains('@')]
    return home_games, away_games

# Calculate statistics for a given set of games
def calculate_statistics(df):
    # Convert non-numeric values to NaN
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    
    # Calculate mean for each column
    mean_stats = df_numeric.mean()
    
    return mean_stats

def main():
    print("Empty")
        
main()
