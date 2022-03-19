# from turtle import bgcolor
import pygetwindow as win
# import PySimpleGUI as gui
import subprocess # used to launch game
import sys # used to launch game
# import os # used to launch game
import configparser

import os.path

# from screeninfo import get_monitors
 
# for monitor in get_monitors():
#     width = monitor.width
#     height = monitor.height
 
#     print(str(width) + 'x' + str(height))
#     print(monitor.name)

# titles = win.getAllTitles()

# gui.Window(title="Window positioner", layout=[[]], margins=(100, 50)).read()

# ini saves:
# editor for all ini settings: on/off/value or keep whats in the file (do nothing/skip)
# save presets
# launch game with presets
# launch patcher (to update the game)

# import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput

# PROJECT_PATH = pathlib.Path(__file__).parent
# PROJECT_UI = PROJECT_PATH / "CWFlyffHelper.ui"

#incomplete. 3rd column in treeview with suggestions / min and max values; i.e. tooltips
# iniValues = ["1920 1080", "0=no,1=yes", "2=low, 1=mid, 0=high", "2=low, 1=mid, 0=high",
            # "2=low, 1=mid, 0=high", "2=low, 1=mid, 0=high", "2=low, 1=mid, 0=high", 
            # "0=off?", "255", "???"]

# os.getpid()
# os.setpriority()

class CwflyffhelperApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        # icon = tk.PhotoImage(file = 'E:\GitHub\CWFlyffHelper\source\CWFlyff.ico')
        # self.toplevel.iconphoto(False, icon)
        self.frameWindowMover = ttk.Frame(self.toplevel)
        self.listboxOpenWindows = tk.Listbox(self.frameWindowMover, width='35', height='14', selectmode=tk.SINGLE)
        self.listboxOpenWindows.grid(column='0', columnspan='2', padx='10', pady='10', row='0')
        self.listboxOpenWindows.bind('<<ListboxSelext>>', self.refreshlistboxOpenWindows)
        self.entryFilterOpenWindows = ttk.Entry(self.frameWindowMover, width='35')
        self.entryFilterOpenWindows.grid(column='0', columnspan='2', padx='5', pady='5', row='1')
        self.buttonRefreshlistboxOpenWindows = ttk.Button(self.frameWindowMover, command=self.refreshlistboxOpenWindows)
        self.buttonRefreshlistboxOpenWindows.configure(text='Refresh List', width='35')
        self.buttonRefreshlistboxOpenWindows.grid(column='0', padx='5', pady='5', row='2', columnspan='2')
        self.buttonTopLeft = ttk.Button(self.frameWindowMover, command=self.buttonTopLeft)
        self.buttonTopLeft.configure(text='Top Left', width='15')
        self.buttonTopLeft.grid(column='0', padx='5', pady='5', row='3')
        self.buttonTopRight = ttk.Button(self.frameWindowMover, command=self.buttonTopRight)
        self.buttonTopRight.configure(text='Top Right', width='15')
        self.buttonTopRight.grid(column='1', padx='5', pady='5', row='3')
        self.buttonBottomLeft = ttk.Button(self.frameWindowMover, command=self.buttonBottomLeft)
        self.buttonBottomLeft.configure(text='Bottom Left', width='15')
        self.buttonBottomLeft.grid(column='0', padx='5', pady='5', row='4')
        self.buttonBottomRight = ttk.Button(self.frameWindowMover, command=self.buttonBottomRight)
        self.buttonBottomRight.configure(text='Bottom Right', width='15')
        self.buttonBottomRight.grid(column='1', padx='5', pady='5', row='4')
        self.frameWindowMover.configure(height='200', padding='10', width='200')
        self.frameWindowMover.grid(column='0', row='0', columnspan='2')
        self.frameIniSettings = ttk.Frame(self.toplevel)
        self.treeviewIniSettings = ttk.Treeview(self.frameIniSettings, column=("c1", "c2"), show='headings', selectmode='browse')
        self.treeviewIniSettings.column("# 1", anchor=tk.CENTER, stretch=tk.NO)#, width=35)
        self.treeviewIniSettings.heading("# 1", text="Setting")
        self.treeviewIniSettings.column("# 2", anchor=tk.CENTER, stretch=tk.NO)#, width=10)
        self.treeviewIniSettings.heading("# 2", text="Value")
        self.scrollbarTreeView = ttk.Scrollbar(self.frameIniSettings, orient ="vertical", command = self.treeviewIniSettings.yview)
        # self.scrollbarTreeView.configure(command=self.treeviewIniSettings.yview) 
        # self.scrollbarTreeView.pack(side ='right', fill ='x')
        self.scrollbarTreeView.grid(column='4', row='0', sticky='nsew')
        self.treeviewIniSettings.configure(yscrollcommand=self.scrollbarTreeView.set) 
        self.treeviewIniSettings.grid(column='2', columnspan='2', padx='5', pady='5', row='0')
        self.treeviewIniSettings.bind('<<TreeviewSelect>>', self.event_treeviewIniSettings)
        self.entryIniSetting = ttk.Entry(self.frameIniSettings)
        self.entryIniSetting.grid(column='2', padx='5', pady='5', row='1')
        self.entryIniSetting.bind('<Return>', self.edittreeviewIniSettings)
        # self.buttonEditIniSetting = ttk.Button(self.frameIniSettings)
        # self.buttonEditIniSetting.configure(text='Edit Row', command=self.edittreeviewIniSettings)
        # self.buttonEditIniSetting.grid(column='3', padx='5', pady='5', row='4')
        self.buttonSaveIniPreset = ttk.Button(self.frameIniSettings)
        self.buttonSaveIniPreset.configure(text='Save Preset', command=self.savePreset)
        self.buttonSaveIniPreset.grid(column='3', padx='5', pady='5', row='2')
        self.buttonApplyIniPreset = ttk.Button(self.frameIniSettings, command=self.copyTreeviewToIni)
        self.buttonApplyIniPreset.configure(text='Apply (without saving)')
        self.buttonApplyIniPreset.grid(column='2', columnspan='2', padx='5', pady='5', row='1', sticky='e')
        self.buttonLoadIniPreset = ttk.Button(self.frameIniSettings)
        self.buttonLoadIniPreset.configure(text='Load Preset', command=self.loadPreset)
        self.buttonLoadIniPreset.grid(column='3', padx='5', pady='5', row='3')
        self.comboboxLoadIniPreset = ttk.Combobox(self.frameIniSettings)
        self.comboboxLoadIniPreset.grid(column='2', padx='5', pady='5', row='3')
        self.comboboxSaveIniPreset = ttk.Combobox(self.frameIniSettings)
        self.comboboxSaveIniPreset.grid(column='2', padx='5', pady='5', row='2')
        self.frameIniSettings.configure(height='200', padding='10', width='200')
        self.frameIniSettings.grid(column='2', columnspan='2', padx='10', pady='10', row='0')
        self.frameLauncher = ttk.Frame(self.toplevel)
        self.pathchooserinputGameFolder = PathChooserInput(self.frameLauncher) # seems like you can't change the width of the ttk.entry within this pygubu.widgets.pathchooserinput :( maybe find a solution in tk instead
        self.pathchooserinputGameFolder.configure(initialdir='', path='', type='directory')
        self.pathchooserinputGameFolder.grid(column='5', columnspan='2', row='0')
        self.pathchooserinputGameFolder.bind('<<PathChooserPathChanged>>', self.event_pathChanged)
        self.buttonLaunchGame = ttk.Button(self.frameLauncher, command=self.launchGame)
        self.buttonLaunchGame.configure(text='Launch Game')
        self.buttonLaunchGame.grid(column='5', padx='5', pady='5', row='1')
        self.buttonLaunchPatcher = ttk.Button(self.frameLauncher, command=self.buttonLaunchPatcher)
        self.buttonLaunchPatcher.configure(text='Launch Patcher')
        self.buttonLaunchPatcher.grid(column='6', padx='5', pady='5', row='1')
        self.buttonLowIniPreset = ttk.Button(self.frameLauncher, command=self.setLowIniPreset)
        self.buttonLowIniPreset.configure(text='Low Settings')
        self.buttonLowIniPreset.grid(column='5', padx='5', pady='5', row='2')
        self.buttonMidIniPreset = ttk.Button(self.frameLauncher, command=self.setMidIniPreset)
        self.buttonMidIniPreset.configure(text='Mid Settings')
        self.buttonMidIniPreset.grid(column='5', padx='5', pady='5', row='3')
        self.buttonHighIniPreset = ttk.Button(self.frameLauncher, command=self.setHighIniPreset)
        self.buttonHighIniPreset.configure(text='High Settings')
        self.buttonHighIniPreset.grid(column='5', padx='5', pady='5', row='4')
        self.frameLauncher.configure(height='200', padding='10', width='200')
        self.frameLauncher.grid(column='5', padx='10', pady='10', row='0', columnspan='2')
        self.toplevel.geometry('1000x400')
        self.toplevel.maxsize(1000, 400)
        self.toplevel.minsize(1000, 400)
        self.toplevel.resizable(False, False)
        self.toplevel.title('CWFlyffHelper')
        self.config = configparser.ConfigParser(allow_no_value=True,delimiters=(' ',), comment_prefixes=('//')) # set space as delimiter instead of =; set // as comments because neuz.ini requires these comments/headers
        self.config.optionxform = str # fix for case-(in)sensitivity

        self.configCWFlyffHelper = configparser.ConfigParser(allow_no_value=True)
        self.config.optionxform = str # fix for case-(in)sensitivity # probably needed to be compatible with neuz.ini

        # Main widget
        self.mainwindow = self.toplevel

    def buttonTopLeft(self):
        selectedWindowTitle = app.listboxOpenWindows.get(app.listboxOpenWindows.curselection())
        # print(app.listboxOpenWindows.focus())
        selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
        w = selectedWindow.width
        h = selectedWindow.height
        selectedWindow.moveTo(-8, 0)
    
    def buttonTopRight(self):
        selectedWindowTitle = app.listboxOpenWindows.get(app.listboxOpenWindows.curselection())
        # print(app.listboxOpenWindows.focus())
        selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
        w = selectedWindow.width
        h = selectedWindow.height
        selectedWindow.moveTo(2560-w+8, 0)

    def buttonBottomLeft(self):
        selectedWindowTitle = app.listboxOpenWindows.get(app.listboxOpenWindows.curselection())
        # print(app.listboxOpenWindows.focus())
        selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
        w = selectedWindow.width
        h = selectedWindow.height
        selectedWindow.moveTo(-8, 1440-h-32)

    def buttonBottomRight(self):
        selectedWindowTitle = app.listboxOpenWindows.get(app.listboxOpenWindows.curselection())
        # print(app.listboxOpenWindows.focus())
        selectedWindow = win.getWindowsWithTitle(selectedWindowTitle)[0]
        w = selectedWindow.width
        h = selectedWindow.height
        selectedWindow.moveTo(2560-w+8, 1440-h-32)

    def launchGame(self):
        launchNeuzCommand = "cd /D " + self.pathchooserinputGameFolder.cget('path') + " && start Neuz.exe"
        subprocess.run(launchNeuzCommand, shell=True)

    def buttonLaunchPatcher(self):
        launchFlyffCommand = "cd /D " + self.pathchooserinputGameFolder.cget('path') + " && start Flyff.exe"
        subprocess.run(launchFlyffCommand, shell=True)

    def refreshlistboxOpenWindows(self):
        self.listboxOpenWindows.delete(0,tk.END)
        filtertext = self.entryFilterOpenWindows.get()
        titles = win.getAllTitles()
        titles.sort()
        if(filtertext == ''):
            for t in titles:
                if t.__contains__("Clockworks Flyff"):
                    self.listboxOpenWindows.insert('end', t)
        else:
            for t in titles:
                if t.__contains__(filtertext):
                    self.listboxOpenWindows.insert('end', t)
    
    def event_pathChanged(self, event):
        self.configCWFlyffHelper.set("OPTIONS", "game_path", self.pathchooserinputGameFolder.cget('path'))
        with open('cwflyffhelper.ini', 'w') as cwflyffhelperIni:
            self.configCWFlyffHelper.write(cwflyffhelperIni, True)
        cwflyffhelperIni.close()
        self.parseNeuzIni()

    def event_treeviewIniSettings(self, event):
        self.entryIniSetting.delete(0, 'end')
        self.entryIniSetting.insert(0, self.treeviewIniSettings.item(self.treeviewIniSettings.focus())['values'][1])

    def edittreeviewIniSettings(self, event):
        selected_item = self.treeviewIniSettings.selection()[0]
        self.treeviewIniSettings.item(selected_item, values=[self.treeviewIniSettings.item(selected_item)['values'][0], self.entryIniSetting.get()]) # keep left column the same and edit the second column
    
    def parseNeuzIni(self):
        neuzIniPath = self.pathchooserinputGameFolder.cget('path') + r'\neuz.ini' # maybe have as a class variable instead that updates whenever the path is changed
        with open(neuzIniPath) as stream:
            self.config.read_string('[SECTION_FOR_CONFIGPARSER]\n' + stream.read())
        # print(self.config.items)
        for item in self.treeviewIniSettings.get_children():
            self.treeviewIniSettings.delete(item)
        counter = 0
        for key in self.config["SECTION_FOR_CONFIGPARSER"]:
            self.treeviewIniSettings.insert(parent = '', index=counter, values=[key, self.config["SECTION_FOR_CONFIGPARSER"][key]])
            # print(key + ", " + self.config["SECTION_FOR_CONFIGPARSER"][key])
            counter += 1
        self.treeviewIniSettings.update()

    def copyTreeviewToIni(self):
        for item in self.treeviewIniSettings.get_children():
            self.config.set("SECTION_FOR_CONFIGPARSER", self.treeviewIniSettings.item(item)['values'][0], str(self.treeviewIniSettings.item(item)['values'][1]))
        self.writeIni()

    def setLowIniPreset(self):
        # self.parseNeuzIni()
        #SETTING 0
        self.config.set("SECTION_FOR_CONFIGPARSER", "resolution", "800 600")
        self.config.set("SECTION_FOR_CONFIGPARSER", "fullscreen", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "texture", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "view", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "detail", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "distant", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "shadow", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DamageRender", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "BuffTimeRender", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXRenderOff", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "PRenderName", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "OPRenderName", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "NRenderName", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "POWERUPICONSPERROW", "5")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DisableBuff", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "HideOwnPet", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXLEVEL", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WEATHEREFFECT", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WeaponGlow", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SetGlow", "1")
        self.writeIni()
        self.launchGame()
    def setMidIniPreset(self):
        # self.parseNeuzIni()
        #SETTING 1
        self.config.set("SECTION_FOR_CONFIGPARSER", "resolution", "1280 800")
        self.config.set("SECTION_FOR_CONFIGPARSER", "fullscreen", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "texture", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "view", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "detail", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "distant", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "shadow", "2")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DamageRender", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "BuffTimeRender", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXRenderOff", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "PRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "OPRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "NRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "POWERUPICONSPERROW", "12")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DisableBuff", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "HideOwnPet", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXLEVEL", "5")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WEATHEREFFECT", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WeaponGlow", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SetGlow", "0")
        self.writeIni()
        self.launchGame()
    def setHighIniPreset(self):
        # self.parseNeuzIni()
        #SETTING 2 - for now this is not fullscreen anymore because of the new monitor
        self.config.set("SECTION_FOR_CONFIGPARSER", "resolution", "1920 1080")
        self.config.set("SECTION_FOR_CONFIGPARSER", "fullscreen", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "texture", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "view", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "detail", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "distant", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "shadow", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DamageRender", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "BuffTimeRender", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXRenderOff", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "PRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "OPRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "NRenderName", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "POWERUPICONSPERROW", "18")
        self.config.set("SECTION_FOR_CONFIGPARSER", "DisableBuff", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "HideOwnPet", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SFXLEVEL", "5")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WEATHEREFFECT", "1")
        self.config.set("SECTION_FOR_CONFIGPARSER", "WeaponGlow", "0")
        self.config.set("SECTION_FOR_CONFIGPARSER", "SetGlow", "0")
        self.writeIni()
        self.launchGame()
    
    def popupHandler(self, message):
        popup = tk.Toplevel(self.toplevel)
        popup.geometry("400x100")
        popupLabel = tk.Label(popup, text=message) #, font= ('Helvetica 12'))
        popupLabel.pack(pady=30)

    def savePreset(self):
        if self.comboboxSaveIniPreset.get() == '':
            self.popupHandler("Preset needs to be named before saving (in box to the left).")
        else:
            sectionPreset = "PRESET_" + self.comboboxSaveIniPreset.get()#.capitalize()
            if(self.configCWFlyffHelper.has_section(sectionPreset) == False): # could also use try/except but whatever
                self.configCWFlyffHelper.add_section(sectionPreset)
            self.configCWFlyffHelper.set(sectionPreset, "preset_name", self.comboboxSaveIniPreset.get())
            # for now, it will just save all settings. In the future I want to change it so that it only saves what has been changed
            # that way, other settings not part of the preset arent overwritten every time and can be changed ingame still
            for item in self.treeviewIniSettings.get_children():
                self.configCWFlyffHelper.set(sectionPreset, self.treeviewIniSettings.item(item)['values'][0], str(self.treeviewIniSettings.item(item)['values'][1]))
            with open('cwflyffhelper.ini', 'w') as cwflyffhelperIni:
                self.configCWFlyffHelper.write(cwflyffhelperIni, True)
            cwflyffhelperIni.close()
            self.readCWFlyffHelperIni()
            self.addPresetsToComboboxes()
            
    def loadPreset(self):
        sectionPreset = "PRESET_" + self.comboboxLoadIniPreset.get()
        for itemPreset in self.configCWFlyffHelper.items(sectionPreset):
            #replace items in treeviewIniSettings
            for itemTreeview in self.treeviewIniSettings.get_children():
                if self.treeviewIniSettings.item(itemTreeview)['values'][0] == itemPreset[0]:
                    self.treeviewIniSettings.item(itemTreeview, values=[self.treeviewIniSettings.item(itemTreeview)['values'][0], itemPreset[1]])

    def addPresetsToComboboxes(self):
        # self.comboboxLoadIniPreset['values'], self.comboboxSaveIniPreset['values'] = self.configCWFlyffHelper.sections()[1,'end']
        try:
            presetNames = []
            for section in self.configCWFlyffHelper.sections():
                if section.__contains__("PRESET_"):
                    presetNames.append(self.configCWFlyffHelper.get(section, "preset_name"))
            self.comboboxLoadIniPreset['values'] = presetNames
            self.comboboxSaveIniPreset['values'] = presetNames
            #maybe automatically select first item? how?
        except:
            print("Couldn't load presets.")

    def writeIni(self):
        neuzIniPath = self.pathchooserinputGameFolder.cget('path') + r'\neuz.ini' # maybe have as a class variable instead that updates whenever the path is changed
        with open(neuzIniPath, 'w') as config_file:
            self.config.write(config_file,False)
        config_file.close()

        # remove the section that configparser requires and add the comments/headers that neuz.ini requires back in
        with open(neuzIniPath, 'r+') as neuz:
            old = neuz.read()
            old = old[26:] # remove [SECTION_FOR_CONFIGPARSER] line (could probably be done with neuz.readlines() but honestly, it's working right now and I don't care)
            neuz.seek(0) # rewind?
            neuz.write('// neuz browser ini file\n \n//option' + old)
        neuz.close()
        self.parseNeuzIni() #after saving, load the new ini and put it into treeview

    def readCWFlyffHelperIni(self):
        self.configCWFlyffHelper.read("cwflyffhelper.ini")
        self.pathchooserinputGameFolder['path'] = self.configCWFlyffHelper.get("OPTIONS", "game_path")
        self.addPresetsToComboboxes()

    def run(self):
        if self.pathchooserinputGameFolder.cget('path') != '':
            self.parseNeuzIni()

        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = CwflyffhelperApp()
    app.refreshlistboxOpenWindows()
    app.readCWFlyffHelperIni()
    # app.treeviewIniSettings.insert(parent='', index=0, iid=0, text='', values=('Vineet','Alpha'))
    app.run()

# ini reader: either button or whenever folder path is changed