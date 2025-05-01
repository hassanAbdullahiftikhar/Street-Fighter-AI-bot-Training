import socket
import json
from game_state import GameState
#from bot import fight
import sys
from bot import Bot
import pandas as pd
def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

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
        print("Current Game State timer: ", current_game_state.timer)
        new_data = {
            "timer": [current_game_state.timer],
            "fight_result": [current_game_state.fight_result],
            "has_round_started": [current_game_state.has_round_started],
            "is_round_over": [current_game_state.is_round_over],
            "Player1_ID": [current_game_state.player1.player_id],
            "Player1_health": [current_game_state.player1.health],
            "Player1_x_coord": [current_game_state.player1.x_coord],
            "Player1_y_coord": [current_game_state.player1.y_coord],
            "Player1_is_jumping": [current_game_state.player1.is_jumping],
            "Player1_is_crouching": [current_game_state.player1.is_crouching],
            "Player1_is_in_move": [current_game_state.player1.is_player_in_move],
            "Player1_move_id": [current_game_state.player1.move_id],
            "Player1_button_up": [current_game_state.player1.player_buttons.up],
            "Player1_button_down": [current_game_state.player1.player_buttons.down],
            "Player1_button_right": [current_game_state.player1.player_buttons.right],
            "Player1_button_left": [current_game_state.player1.player_buttons.left],
            "Player2_ID": [current_game_state.player2.player_id],
            "Player2_health": [current_game_state.player2.health],
            "Player2_x_coord": [current_game_state.player2.x_coord],
            "Player2_y_coord": [current_game_state.player2.y_coord],
            "Player2_is_jumping": [current_game_state.player2.is_jumping],
            "Player2_is_crouching": [current_game_state.player2.is_crouching],
            "Player2_is_in_move": [current_game_state.player2.is_player_in_move],
            "Player2_move_id": [current_game_state.player2.move_id],
            "Player2_button_up": [current_game_state.player2.player_buttons.up],
            "Player2_button_down": [current_game_state.player2.player_buttons.down],
            "Player2_button_right": [current_game_state.player2.player_buttons.right],
            "Player2_button_left": [current_game_state.player2.player_buttons.left]
        }
        df_new = pd.DataFrame(new_data)
        df_new.to_csv("game_log_template.csv", mode='a', header=False, index=False)
        bot_command = bot.fight(current_game_state, sys.argv[1])
        send(client_socket, bot_command)
if __name__ == '__main__':
   main()
