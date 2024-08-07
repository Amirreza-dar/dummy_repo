from flask_socketio import SocketIO
import time
import csv
import datetime
from flask import Flask, request, session, jsonify
import os

# socketio = SocketIO(message_queue='redis://')
socketio = SocketIO()

# Given list of tuples
rows = [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)]

# We will create a new list following the pattern specified
new_rows = []

# Loop through each tuple in the original list
for row in rows:
    for suffix in ['a', 'b', 'c', 'd']:
        # For each element in the tuple, add the suffix and create a new tuple
        new_row = tuple(f"{num}{suffix}" for num in row)
        new_rows.append(new_row)

# new_rows

def trigger_lights():
    socketio.emit('get_ready', {'message' : 'Get ready for practice jumps!', 'countdown' : ''})
    socketio.sleep(3)
    for s in [3,2,1]:
        socketio.emit('get_ready', {'message': 'Practice starts in', 'countdown' : s})
        socketio.sleep(1.0)
    i = 1
    while i<4:
        # rows = [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)]
        for row in new_rows:
            socketio.sleep(0.5)  # Delay between each row
            socketio.emit('light_row', {'row': row, 'count': i,  'message': 'practicing'})
        i += 1

    socketio.emit('get_ready', {'message' : 'Get ready for real game jumps!', 'countdown' : ''})
    socketio.sleep(3)
    for s in [3,2,1]:
        socketio.emit('get_ready', {'message': 'Game starts in', 'countdown' : s})
        socketio.sleep(1.0)
    i = 1
    socketio.emit('')
    socketio.sleep(3.0)
    while i<11:
        # rows = [(1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)]
        for row in new_rows:
            socketio.sleep(0.3)  # Delay between each row
            socketio.emit('light_row', {'row': row, 'count': i,  'message': 'JUMP!'})
        i += 1

    

@socketio.on('start_game')
def handle_start_game():
    # print('Event has been triggered on server-siie')
    trigger_lights()





# Logic for creating a .csv file and store it in some directory



def generate_csv():


    def generate_time_string(difficulty_level, number_of_sets):
      interval_pyramid = [[[3,3,3,3,3,3],[3,3,3,3,3,3],[3,3,3,3,3,3]]
                          ,[[3,1,3,1,1,3,1,1,3,1,3],[3,1,3,1,1,3,1,1,3,1,3],[3,1,3,1,1,3,1,1,3,1,3]]
                          ,[[3,1,3,1,1,3,1,1,3,1,3],[3,1,3,1,1,3,1,1,3,1,3],[3,1,3,1,1,3,1,1,3,1,3]]]
      interval_between_set = [20,20,20]
      time = 0
      time += 5 # 5 seconds before the game starts
      string = []
      for i,set_index in enumerate(interval_pyramid[difficulty_level][:number_of_sets]):
        string.append(time)      
        for elem in set_index:
          time += elem
          string.append(time)
        time += interval_between_set[i]
      return string


    
# Initialization
    number_of_sets = 2  # sets per session
    # Lighting configuration

    # Set the difficulty of the choosen game (0,1,2)

    if session['game'] == 'easy' : game_difficulty = 0
    elif session['game'] == 'medium' : game_difficulty = 1
    elif session['game'] == 'hard' : game_difficulty = 2

  


    
    # Writing to CSVreport
    # try: 
    print(session["email"])
    # os.makedirs(session['email'])
    directory = session['email']
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(directory + '/' + 'exercise_session_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['Line Travel Time', 'Line Intervals', 'Number of Lines', 'Number of Sets', 'String of input', 'Lighting']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            
            'String of input':  generate_time_string(game_difficulty , number_of_sets),
            # 'Tile Input Data': str(playground),  # Convert the 3D array to string to store in CSV
        })
    print("CSV file 'exercise_session_data.csv' has been generated.")
