import socket
import json
from game_state import GameState
from bot import Bot
import sys
from bot import Bot
import pandas as pd
import numpy as np
from mlp import predict_command
from keras.models import load_model
import joblib
from command import Command
import keyboard
import time
#"C:\Users\user\AppData\Local\Programs\Python\Python310\python.exe" -m venv gamebot-env
#gamebot-env\Scripts\activate
model = load_model('sf_model.h5')
scaler = joblib.load('scaler.save')

def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):    
    if hasattr(command, "object_to_dict"):
        z = command.object_to_dict()
    else:
        z = command
    pay_load = json.dumps(z).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    pay_load = client_socket.recv(4096)
    data = pay_load.decode()
    decoder = json.JSONDecoder()
    input_dict, index = decoder.raw_decode(data)
    game_state = GameState(input_dict)
    return game_state



def get_pressed_keys():
    keys = ['w', 'a', 's', 'd', 'x', 'c', 'v', 'b', 'n', 'm']
    return [key for key in keys if keyboard.is_pressed(key)]
    
def main():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [1 or 2]")
        return

    if sys.argv[1] == '1':
        client_socket = connect(9999)
    elif sys.argv[1] == '2':
        client_socket = connect(10000)
    else:
        print("Invalid argument. Use '1' or '2'.")
        return

    current_game_state = None
    bot = Bot()
    while (current_game_state is None) or (not current_game_state.is_round_over):
        current_game_state = receive(client_socket)
        current_game_state.player1.player_buttons.up=False
        current_game_state.player1.player_buttons.down=False
        current_game_state.player1.player_buttons.left=False
        current_game_state.player1.player_buttons.right=False
        current_game_state.player1.player_buttons.Y=False
        current_game_state.player1.player_buttons.B=False
        current_game_state.player1.player_buttons.X=False
        current_game_state.player1.player_buttons.A=False
        current_game_state.player1.player_buttons.L=False
        current_game_state.player1.player_buttons.R=False
        current_game_state.player1.player_buttons.select=False
        current_game_state.player1.player_buttons.start=False
        current_game_state.player1.is_jumping=False
        current_game_state.player1.is_crouching=False

        print("Current Game State timer: ", current_game_state.timer)
        pressed_keys = get_pressed_keys()
        command = Command()
        buttons = command.player_buttons
        # b=bot.fight(current_game_state,sys.argv[1])
        # send(client_socket, b)
        # for key in pressed_keys:
        #     if key == 'w':
        #         current_game_state.player1.player_buttons.up = True
        #     if key == 's':
        #         current_game_state.player1.player_buttons.down = True
        #     if key == 'a':
        #         current_game_state.player1.player_buttons.left = True
        #     if key == 'd':
        #         current_game_state.player1.player_buttons.right = True
        #     if key=='x':
        #         current_game_state.player1.player_buttons.Y= True
        #     if key=='c':
        #         current_game_state.player1.player_buttons.B= True
        #     if key=='v':
        #         current_game_state.player1.player_buttons.X= True
        #     if key=='b':
        #         current_game_state.player1.player_buttons.A= True
        #     if key=='n':
        #         current_game_state.player1.player_buttons.L= True
        #     if key=='m':
        #         current_game_state.player1.player_buttons.R= True
        # new_data = {
        #     "timer": [current_game_state.timer],
        #     "fight_result": [current_game_state.fight_result],
        #     "has_round_started": [current_game_state.has_round_started],
        #     "is_round_over": [current_game_state.is_round_over],
        #     "Player1_ID": [current_game_state.player1.player_id],
        #     "Player1_health": [current_game_state.player1.health],
        #     "Player1_x_coord": [current_game_state.player1.x_coord],
        #     "Player1_y_coord": [current_game_state.player1.y_coord],
        #     "Player1_is_jumping": [current_game_state.player1.is_jumping],
        #     "Player1_is_crouching": [current_game_state.player1.is_crouching],
        #     "Player1_is_in_move": [current_game_state.player1.is_player_in_move],
        #     "Player1_move_id": [current_game_state.player1.move_id],
        #     "Player1_button_up": [current_game_state.player1.player_buttons.up],
        #     "Player1_button_down": [current_game_state.player1.player_buttons.down],
        #     "Player1_button_right": [current_game_state.player1.player_buttons.right],
        #     "Player1_button_left": [current_game_state.player1.player_buttons.left],
        #     "Player1_button_Y": [current_game_state.player1.player_buttons.Y],
        #     "Player1_button_B": [current_game_state.player1.player_buttons.B],
        #     "Player1_button_X": [current_game_state.player1.player_buttons.X],
        #     "Player1_button_A": [current_game_state.player1.player_buttons.A],
        #     "Player1_button_L": [current_game_state.player1.player_buttons.L],
        #     "Player1_button_R": [current_game_state.player1.player_buttons.R],
        #     "Player1_button_select": [current_game_state.player1.player_buttons.select],
        #     "Player1_button_start": [current_game_state.player1.player_buttons.start],
        #     "Player1_ID": [current_game_state.player1.player_id],
        #     "Player2_ID": [current_game_state.player2.player_id],
        #     "Player2_x_coord": [current_game_state.player2.x_coord],
        #     "Player2_y_coord": [current_game_state.player2.y_coord],
        #     "Player2_is_jumping": [current_game_state.player2.is_jumping],
        #     "Player2_is_crouching": [current_game_state.player2.is_crouching],
        #     "Player2_is_in_move": [current_game_state.player2.is_player_in_move],
        #     "Player2_move_id": [current_game_state.player2.move_id],
        #     "Player2_button_up": [current_game_state.player2.player_buttons.up],
        #     "Player2_button_down": [current_game_state.player2.player_buttons.down],
        #     "Player2_button_right": [current_game_state.player2.player_buttons.right],
        #     "Player2_button_left": [current_game_state.player2.player_buttons.left],
        #     "Player2_button_Y": [current_game_state.player2.player_buttons.Y],
        #     "Player2_button_B": [current_game_state.player2.player_buttons.B],
        #     "Player2_button_X": [current_game_state.player2.player_buttons.X],
        #     "Player2_button_A": [current_game_state.player2.player_buttons.A],
        #     "Player2_button_L": [current_game_state.player2.player_buttons.L],
        #     "Player2_button_R": [current_game_state.player2.player_buttons.R],
        #     "Player2_button_select": [current_game_state.player2.player_buttons.select],
        #     "Player2_button_start": [current_game_state.player2.player_buttons.start],
        #     "Player2_health": [current_game_state.player2.health],
        # }
        # print(current_game_state.player2.health)
        # print(pressed_keys)
        # df_new = pd.DataFrame(new_data)
        # df_new.to_csv("game_data4.csv", mode='a', header=False, index=False)
        bot_command = predict_command(current_game_state, model, scaler)
        # print("Bot command:", bot_command)
        # # print("Bot command1:", bot_command.object_to_dict())
        # command.player_buttons = current_game_state.player1.player_buttons
        # command.player2_buttons = current_game_state.player2.player_buttons
        # send(client_socket, command)
        send(client_socket, bot_command)
        # print("Bot command2:", bot_command)
        # print(command.player_buttons.object_to_dict()) 
        # print(current_game_state.player1.player_buttons.object_to_dict())
if __name__ == '__main__':
   main()
