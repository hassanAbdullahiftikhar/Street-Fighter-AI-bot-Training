# Street-Fighter-AI-bot-Training
### Prequisites/Dependencies

* Operating System: Windows 7 or above (64-bit)

* Ensure Python 3.10 or 3.11 is installed since tensorflow is not available as of now on python 3.12.

* Download the folder from google drive
* (Optional)
    * Create a virtual environment in the directory where the appropriate python version is installed along with tensorflow and joblib.
    * Activate the virtual environment.
* Open Single player folder
* Run EmuHawk.exe.
* From File drop down, choose Open ROM. (Shortcut: Ctrl+O)
* From the same single-player folder, choose the Street Fighter II Turbo (U).smc file.
* From Tools drop down, open the Tool Box. (Shortcut: Shift+T)
* Once you have performed the above steps, leave the emulator window and tool box open and open the command prompt in the directory of  the API with the virtual environment activated.
* Navigate to the extracted folder in Command Prompt and type the following command:"python controller.py "1" "
* Wait for the following to be printed on your terminal:
2025-05-09 20:37:35.418240: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: SSE SSE2 SSE3 SSE4.1 SSE4.2 AVX AVX2 FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
* After executing the code, go and select your character(s) in the game after choosing normal mode. Controls for selecting players can be set or seen from the controllers option in the config drop down of the emulator.
* Now click on the second icon in the top row (Gyroscope Bot). This will cause the emulator to establish a connection with the program you ran and you will see "Connected to the game!" or "CONNECTED SUCCESSFULLY" on the terminal.
* If you have completed all of these steps successfully then you have successfully run the starter code for the game bot AI trained using MLP.
* The program will stop once a single round is finished. Repeat this process for running the emulator and the code again.
