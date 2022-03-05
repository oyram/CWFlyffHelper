import pygetwindow as win
import PySimpleGUI as gui
import subprocess # used to launch game
import sys # used to launch game
# import os # used to launch game

import os.path

from screeninfo import get_monitors
 
for monitor in get_monitors():
    width = monitor.width
    height = monitor.height
 
    print(str(width) + 'x' + str(height))
    print(monitor.name)

# titles = win.getAllTitles()

# gui.Window(title="Window positioner", layout=[[]], margins=(100, 50)).read()


# ini saves:
# editor for all ini settings: on/off/value or keep whats in the file (do nothing/skip)
# save presets
# launch game with presets
# launch patcher (to update the game)

gui.theme("DarkGrey4")

launch_game_column = [
    [gui.Text("Game Folder Path")],
    [gui.InputText(size=(35,5), key="-GAME_PATH-", default_text="F:\Spiele\Installiert\ClockworksFlyff")],
    [gui.Button("Launch Game", key="-LAUNCH_NEUZ-"), gui.Button("Launch Patcher", key="-LAUNCH_PATCHER-")]
]

ini_change_column = [
    [gui.Text("Apply neuz.ini preset:")],
    [gui.Button("Low", key="-MIN_INI_SETTINGS-", size=(15,2)), gui.Button("Medium", key="-MED_INI_SETTINGS-", size=(15,2)), gui.Button("Main Window", key="-MAIN_INI_SETTINGS-", size=(15,2))]
]

window_list_column = [

    [

        gui.Text("Select Window:"),

        # gui.In(size=(25, 1), enable_events=True, key="-TITLES-"),
        gui.Button("Refresh", key="-REFRESH-")

    #     gui.FolderBrowse(),

    ],

    [

        gui.Listbox(

            values=[], enable_events=True, size=(40, 20), key="-WINDOW_LIST-"

        )

    ],

]

image_viewer_column = [

    # [gui.Text(size=(40, 1), key="-TOUT-")],

    # [gui.Image(key="-IMAGE-")],
    [gui.Text("Quick Snap (Main Monitor, 8 pixel offset):")],
    [gui.Button("Top Left", key="-TOPLEFT-", size=(20, 2)), gui.Button("Top Right", key="-TOPRIGHT-", size=(20, 2))],
    [gui.Button("Bottom Left", key="-BOTTOMLEFT-", size=(20, 2)), gui.Button("Bottom Right", key="-BOTTOMRIGHT-", size=(20, 2))],

    [gui.Text("Manually enter coordinates:")],

    [gui.InputText(size=(10,5), key="-XCOORD-"), gui.InputText(size=(10,5), key="-YCOORD-"),gui.Button("Move", key="-MOVE-")]

]

# third_column = [
#     [gui.Button("Top Right", key="-TOPRIGHT-")],
#     [gui.Button("Bottom Right", key="-BOTTOMRIGHT-")]

# ]

layout = [

    [

        gui.Column(window_list_column),

        gui.VSeperator(),

        gui.Column(image_viewer_column),

        gui.VSeperator(),
        
        gui.Column(launch_game_column),

        # gui.HSeperator(),

        # gui.Column(ini_change_column)

    ]

]

window = gui.Window("Window positioner", layout)


# Run the Event Loop

while True:

    event, values = window.read()

    if event == "Exit" or event == gui.WIN_CLOSED:

        break

    # Folder name was filled in, make a list of files in the folder

    if event == "-REFRESH-":

        titles = win.getAllTitles()
        fixedTitles = []
        for t in titles:
            if t != '':
                fixedTitles.append(t)
        window["-WINDOW_LIST-"].update(fixedTitles)

    elif event == "-TOPLEFT-":
        try:
            selectedWindowTitle = values["-WINDOW_LIST-"][0]
            selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
            w = selectedWindow.width
            h = selectedWindow.height
            # selectedWindow.moveTo(int("-XCOORD-")+1972, int("-YCOORD-"))
            # selectedWindow.moveTo(1972, 0)
            selectedWindow.moveTo(-8, 0)
        except:
            pass

    elif event == "-TOPRIGHT-":
        try:
            selectedWindowTitle = values["-WINDOW_LIST-"][0]
            selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
            w = selectedWindow.width
            h = selectedWindow.height
            selectedWindow.moveTo(2560-w+8, 0)
            print(w)
            print(2560-w)
        except:
            pass

    elif event == "-BOTTOMLEFT-":
        try:
            selectedWindowTitle = values["-WINDOW_LIST-"][0]
            selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
            w = selectedWindow.width
            h = selectedWindow.height
            selectedWindow.moveTo(-8, 1440-h-32)
        except:
            pass

    elif event == "-BOTTOMRIGHT-":
        try:
            selectedWindowTitle = values["-WINDOW_LIST-"][0]
            selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
            w = selectedWindow.width
            h = selectedWindow.height
            selectedWindow.moveTo(2560-w+8, 1440-h-32)
        except:
            pass

    elif event == "-MOVE-":

        try:
            selectedWindowTitle = values["-WINDOW_LIST-"][0]
            selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
            # selectedWindow.moveTo("-XCOORD-", "-YCOORD-")
            # selectedWindow.moveTo(int("-XCOORD-"), int("-YCOORD-"))
            selectedWindow.moveTo("1980", "608")
            print(selectedWindow)
        except:
            print("Could not move window.")

    elif event == "-LAUNCH_NEUZ-":
        try:
            print("Launching Neuz in Folder: ", values["-GAME_PATH-"])
            launchNeuzCommand = "cd /D " + values["-GAME_PATH-"] + " && start Neuz.exe"
            subprocess.run(launchNeuzCommand, shell=True)
        except:
            pass

    elif event == "-LAUNCH_PATCHER-":
        try:
            print("Launching Flyff Patcher in Folder: ", values["-GAME_PATH-"])
            launchFlyffCommand = "cd /D " + values["-GAME_PATH-"] + " && start Flyff.exe"
            subprocess.run(launchFlyffCommand, shell=True)
        except:
            pass

window.close()