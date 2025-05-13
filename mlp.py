import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import pickle
from command import Command

data_file = 'game_data4.csv'
model_file = 'sf_model.h5'
scaler_file = 'scaler.save'

def prepare_data(csv_path):
    df = pd.read_csv(csv_path).dropna()
    # features for our multi layer perceptron
    df['distance'] = abs(df['Player1_x_coord'] - df['Player2_x_coord'])
    df['health_diff'] = df['Player1_health'] - df['Player2_health']
    df['health_ratio'] = df['Player1_health'] / (df['Player2_health'] + 1e-5)  
    df['height_diff'] = df['Player1_y_coord'] - df['Player2_y_coord']
    df['facing_right'] = (df['Player1_x_coord'] < df['Player2_x_coord']).astype(int)
    df['opponent_attacking'] = df['Player2_is_in_move'].astype(int)
    df['timer']=df['timer'].astype(int)
    scaler = MinMaxScaler()
    num_features = [
        'distance', 'Player1_health', 'Player2_health',
        'Player1_x_coord', 'Player1_y_coord',
        'Player2_x_coord', 'Player2_y_coord',
        'health_ratio', 'height_diff',
        'timer'
    ]
    df[num_features] = scaler.fit_transform(df[num_features])
    features = [
        'distance', 'health_diff', 'health_ratio', 'height_diff',  
        'facing_right', 'opponent_attacking',  
        'Player1_is_jumping', 'Player1_is_crouching',
        'Player2_health', 'Player2_is_jumping',
        'Player2_is_crouching', 'Player2_is_in_move',
        'timer'
    ]
    # features that model will predict
    targets = [
        'Player1_button_up', 'Player1_button_down',
        'Player1_button_right', 'Player1_button_left',
        'Player1_button_Y', 'Player1_button_B',
        'Player1_button_X', 'Player1_button_A',
        'Player1_button_L', 'Player1_button_R'
    ]
    
    return df[features].values, df[targets].values, scaler, features

def create_model(input_shape, num_outputs):
    model = Sequential([
        Dense(256, activation='relu', input_shape=input_shape),
        Dropout(0.4),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(num_outputs, activation='sigmoid')
    ])
    model.compile(
        optimizer=Adam(learning_rate=0.0005),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model

def create_command_from_prediction(prediction, mthreshold=0.014,attack=0.01):
    cmd = Command()
    buttons = cmd.player_buttons
    # print(f"Prediction: {prediction}")
    if(buttons.up == True):
        prediction[0] = 0
    if(buttons.down == True):
        prediction[1] = 0
    if(buttons.right == True):
        prediction[2] = 0
    if(buttons.left == True):
        prediction[3] = 0
    if(buttons.B == True):
        prediction[4] = 0
    if(buttons.Y == True):
        prediction[5] = 0
    if(buttons.X == True):
        prediction[6] = 0
    if(buttons.A == True):
        prediction[7] = 0
    if(buttons.L == True):
        prediction[8] = 0
    if(buttons.R == True):
        prediction[9] = 0
    buttons.up = bool(prediction[0] > mthreshold) 
    buttons.down = bool(prediction[1] > mthreshold) 
    buttons.right = bool(prediction[2] > mthreshold) 
    buttons.left = bool(prediction[3] > mthreshold) 
    buttons.B = bool(prediction[4] > attack)
    buttons.Y = bool(prediction[5] > attack)
    buttons.X = bool(prediction[6] > attack) 
    buttons.A = bool(prediction[7] > attack)
    buttons.L = bool(prediction[8] > attack)
    buttons.R = bool(prediction[9] > attack)
    return cmd.object_to_dict()

def predict_command(game_state, model, scaler):
    num_feature_vector = np.array([[
        abs(game_state.player1.x_coord - game_state.player2.x_coord),
        float(game_state.player1.health),
        float(game_state.player2.health),
        float(game_state.player1.x_coord),
        float(game_state.player1.y_coord),
        float(game_state.player2.x_coord),
        float(game_state.player2.y_coord),
        game_state.player1.health / (game_state.player2.health + 1e-5),
        game_state.player1.y_coord - game_state.player2.y_coord,
        float(game_state.timer),
    ]], dtype=np.float32)
    normalized = scaler.transform(num_feature_vector)[0]
    feature_vector = np.array([
        normalized[0],  
        normalized[1] - normalized[2], 
        normalized[7], 
        int(game_state.player1.x_coord < game_state.player2.x_coord),  
        normalized[8],  
        int(game_state.player2.is_player_in_move),  
        int(game_state.player1.is_jumping),
        int(game_state.player1.is_crouching),
        normalized[2],  
        int(game_state.player2.is_jumping),
        int(game_state.player2.is_crouching),
        int(game_state.player2.is_player_in_move),
        normalized[9] 
    ], dtype=np.float32).reshape(1, -1)
    prediction = model.predict(feature_vector, verbose=0)[0]
    return create_command_from_prediction(prediction)

def train_and_save(csv_path, model_path, scaler_path):
    X, y, scaler, feature_names = prepare_data(csv_path)
    X = X.astype(np.float32)
    y = y.astype(np.float32)
    with open('feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = create_model((X.shape[1],), y.shape[1])
    model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=64,
        validation_data=(X_test, y_test),
        callbacks=[EarlyStopping(patience=10)]
    )
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path}, scaler to {scaler_path}")


if __name__ == '__main__':
    train_and_save(
        csv_path=data_file,
        model_path=model_file,
        scaler_path=scaler_file
    )