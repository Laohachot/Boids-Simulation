# Boids-Simulation
Boids simulation with Python and PyGame 

Setup:
    1. Install Python interpreter from https://www.python.org/downloads/
    
    2. Install Python modules: numpy and configparser  
       Windows: In cmd, enter: pip install numpy configparser
       Linux: In terminal, enter: pip3 install numpy configparser
       Mac: Probably like linux

Run:
    Run program by executing main.py with the python interpreter

Controls:
    Generally:
        - F4 to quit program
        - Backspace to go to previous state 

    In boids simulation:
        - Use mouse to select entity class. Spawn entities into simulation 
          area by clicking any mouse button. 

        - Holding LCTRL down while spawning enables continous spawning of 
          entites. 

    In particles simulation:
        - Use any mouse button to spawn particles. 

        - Holding right click causes a force that pulls all 
          particles towards mouse pointer.


Some settings can be configurated the the config.ini file.


Known bugs and problems:
    - Using backspace to get to previous state may bug out some times.
      A quick fix is to click with the mouse and then using the 
      shortcut. 

    - Have experienced very poor performance on MacOS Mojave.

    - In particle state: have experienced that right click action does 
      not register on a laptop running Ubuntu.
