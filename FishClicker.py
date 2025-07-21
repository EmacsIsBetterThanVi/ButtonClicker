from PyWigit import *
import json
import os
screen = NewScreen((720, 400))
font = NewFont("timesnewroman", 20)
SetCaption("Button Clicker")
cash = 0
Buttons = []
Achivements = []
PosibleAchivements = {}
def LoadVersion1SaveData(data):
    global Buttons, cash, i
    try:
        cash = data["cash"]
        print("Data loaded:", data)
        Buttons[0][2] = data["buttons"][0][1]
        Buttons[0][3] = data["buttons"][0][2]
        for j in range(1,len(data["buttons"])):
            NewUpgrade()
            Buttons[j][1] = data["buttons"][j][0]
            Buttons[j][2] = data["buttons"][j][1]
            Buttons[j][3] = data["buttons"][j][2]
    except Exception as e:
        if isinstance(e, KeyError):
            print("Reading Game 1Data failed: Save Data is from an old version which does not have key: ", e)
        else:
            print("Reading Game Data failed:", e)
        Buttons = []
        cash = 0
        i = 1
        Buttons.append([Button(font.render("Button: .", True, White), LeftClick=Button0Click), 0, 1, 0])
        NewUpgrade()
    finally:
         f.close()
def LoadVersion2SaveData(data):
    LoadVersion1SaveData(data)
    for j in range(1, len(data["achivements"])):
        Achivements.append(data["achivements"][j])
load = [LoadVersion1SaveData, LoadVersion2SaveData]
def SaveGame():
    f = open("ButtonClicker.save", "w")
    print("Saving Game")
    data = []
    for j in Buttons:
        data.append([j[1], j[2], j[3]])
    print("Data Constructed: ", data)
    f.write(json.dumps({"version":1, "buttons":data, "cash":cash}))
    f.close()
def Button0Click():
    global cash
    if Buttons[0][1] <= cash:
        cash -= Buttons[0][1]
        cash += Buttons[0][2]
        Buttons[0][3] += 1
i = 1
def NewUpgrade():
    global i
    exec(f"""def Button{i}Click():
    global cash
    if Buttons[{i}][1] <= cash:
        cash -= Buttons[{i}][1]
        Buttons[{i-1}][2] += Buttons[{i}][2]
        Buttons[{i}][1] = int(Buttons[{i}][1] * 1.1)
        if Buttons[{i}][3] == 0:
            NewUpgrade()
        Buttons[{i}][3] += 1
Buttons.append([Button(font.render("Button {i+1}($.): .", True, White), LeftClick=Button{i}Click), 10**(i+1), 1, 0])
""")
    i+=1
Save = Button(font.render("Save", True, White), LeftClick=SaveGame)
Buttons.append([Button(font.render("Button: .", True, White), LeftClick=Button0Click), 0, 1, 0])
if os.path.exists("ButtonClicker.save"):
    f = open("ButtonClicker.save")
    print("Reading Game Data")
    data = json.loads(f.read())
    load[data["version"]-1](data)
else:
    NewUpgrade()
def DrawGame(screen):
    global cash
    if cash >= 10**16:
        screen.blit(font.render(f"CASH: Infinity", True, White), (20, 0))
        cash = 10**30
    else:
        screen.blit(font.render(f"CASH: {cash:,}", True, White), (20, 0))
    Save.draw(screen, (300, 0))
    Buttons[0][0].display = font.render(f"Button: {Buttons[0][3]:,}, Increase Cash by {Buttons[0][2]:,} per click", True, White)
    Buttons[0][0].draw(screen, (20, 24))
    Buttons[1][0].display = font.render(f"Button 2(${Buttons[1][1]:,}): {Buttons[1][3]:,}, Increase Button value by {Buttons[1][2]:,} per click", True, White)
    Buttons[1][0].draw(screen, (20, 48))
    for j in range(2, len(Buttons)):
        Buttons[j][0].display = font.render(f"Button {j+1}(${Buttons[j][1]:,}): {Buttons[j][3]:,}, Increase Button {j} value by {Buttons[j][2]:,} per click", True, White)
        Buttons[j][0].draw(screen, (20, 24+24*j))
def InputGame(event):
    if Save.Click():
        return True
    for j in range(len(Buttons)):
        if Buttons[j][0].Click(event):
            return True
def AchivementsDraw(screen):
    pass
def AchivementsInput(event):
    pass
CreateScrn(DrawGame, InputGame, Black)
Screen(screen, FullScreen=True)
while Status():
    MainLoop(screen)
SaveGame()
pygame.quit()
