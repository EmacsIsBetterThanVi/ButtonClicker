from PyWigit import *
import json
import os
screen = NewScreen((800, 600))
Window = Screen(screen, FullScreen=True)
font = NewFont("timesnewroman", 20)
SetCaption("Button Clicker")
cash = 0
TotalCash = 0
Buttons = []
Achivements = []
PossibleAchivements = {
    "Starting Out":(1, 1), # based on button 1, click button 1, 1 time
    "Perstitance":(1, 1000),
    "Millionaire":(0, 10**6),
    "Billionaire":(0, 10**9),
    "Surpasing Infinity":(0, 10**16) # based on cash, requires hiting infinity
}
MessageQueue = []
def checkAchivements():
  for j in PossibleAchivements:
    if not j in Achivements:
      if PossibleAchivements[j][0] == 0:
        if PossibleAchivements[j][1] <= cash:
          Achivements.append(j)
          MessageQueue.append(j)
          if j == "Surpasing Infinity":
            MessageQueue.append("Congratulations, you have won.")
            MessageQueue.append("We hope you enjoyed the \"game\"")
            MessageQueue.append("Button Clicker was developed by:")
            MessageQueue.append("************ Colman *************")
            MessageQueue.append("************* David *************")
            MessageQueue.append("************ Raphael ************")
            MessageQueue.append("Now, go enjoy the rest of your life")
      elif PossibleAchivements[j][0] >= 1:
        try:
          if PossibleAchivements[j][1] <= Buttons[PossibleAchivements[j][0]-1][3]:
            Achivements.append(j)
            MessageQueue.append(j)
        except Exception as e:
           pass
def LoadVersion1SaveData(data):
    global Buttons, cash, i
    try:
        cash = data["cash"]
        Buttons[0][2] = data["buttons"][0][1]
        Buttons[0][3] = data["buttons"][0][2]
        for j in range(1,len(data["buttons"])):
            NewUpgrade()
            Buttons[j][1] = data["buttons"][j][0]
            Buttons[j][2] = data["buttons"][j][1]
            Buttons[j][3] = data["buttons"][j][2]
    except Exception as e:
        if isinstance(e, KeyError):
            print("Reading Game Data failed: Save Data is from an old version which does not have key: ", e)
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
    global TotalCash
    try:
      LoadVersion1SaveData(data)
      for j in range(0, len(data["achivements"])):
        Achivements.append(data["achivements"][j])
      TotalCash = data["TotalCash"]
    except Exception as e:
        if isinstance(e, KeyError):
            print("Reading Game Data failed: Save Data is from an old version which does not have key: ", e)
        else:
            print("Reading Game Data failed:", e)
        Buttons = []
        cash = 0
        i = 1
        Buttons.append([Button(font.render("Button: .", True, White), LeftClick=Button0Click), 0, 1, 0])
        NewUpgrade()
load = [LoadVersion1SaveData, LoadVersion2SaveData]
def SaveGame():
    f = open("ButtonClicker.save", "w")
    data = []
    for j in Buttons:
        data.append([j[1], j[2], j[3]])
    f.write(json.dumps({"version":2, "buttons":data, "cash":cash, "achivements": Achivements, "TotalCash": TotalCash}))
    f.close()
def Button0Click():
    global cash
    if Buttons[0][1] <= cash:
        cash -= Buttons[0][1]
        cash += Buttons[0][2]
        Buttons[0][3] += 1
i = 1
MessageTicks = 0
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
AchivmentsButton = Button(font.render("Achivments", True, Green), LeftClick=lambda : Window.ChangeScrn(2))
UpgradesButton = Button(font.render("Upgrades", True, Green), LeftClick=lambda : Window.ChangeScrn(1))
Buttons.append([Button(font.render("Button: .", True, White), LeftClick=Button0Click), 0, 1, 0])
if os.path.exists("ButtonClicker.save"):
    f = open("ButtonClicker.save")
    data = json.loads(f.read())
    load[data["version"]-1](data)
else:
    NewUpgrade()
    MessageQueue.append("Welcome to Button Clicker!")
    MessageQueue.append("Anything that says Button...")
    MessageQueue.append("is a button for you to click.")
    MessageQueue.append("We hope you enjoy the \"game\"")
def DrawGame(screen):
    checkAchivements()
    global MessageTicks, cash
    if len(MessageQueue)>0:
      MessageTicks+=1
      screen.blit(font.render(f"{MessageQueue[0]}", True, Yellow), (520, 0))
      if MessageTicks == 90:
        MessageTicks = 0
        MessageQueue.pop(0)
    if cash >= 10**16:
        screen.blit(font.render(f"CASH: Infinity", True, White), (20, 0))
        cash = 10**30
    else:
        screen.blit(font.render(f"CASH: {cash:,}", True, White), (20, 0))
    Save.draw(screen, (300, 0))
    AchivmentsButton.draw(screen, (400, 0))
    Buttons[0][0].display = font.render(f"Button: {Buttons[0][3]:,}, Increase Cash by {Buttons[0][2]:,} per click", True, White)
    Buttons[0][0].draw(screen, (20, 24))
    Buttons[1][0].display = font.render(f"Button 2(${Buttons[1][1]:,}): {Buttons[1][3]:,}, Increase Button value by {Buttons[1][2]:,} per click", True, White)
    Buttons[1][0].draw(screen, (20, 48))
    for j in range(2, len(Buttons)):
        Buttons[j][0].display = font.render(f"Button {j+1}(${Buttons[j][1]:,}): {Buttons[j][3]:,}, Increase Button {j} value by {Buttons[j][2]:,} per click", True, White)
        Buttons[j][0].draw(screen, (20, 24+24*j))
def InputGame(event):
    if Save.Click(event):
        return True
    if AchivmentsButton.Click(event):
        return True
    for j in range(len(Buttons)):
        if Buttons[j][0].Click(event):
            return True
CreateScrn(DrawGame, InputGame, Black)
def AchivementsDraw(screen):
    global cash
    if cash >= 10**16:
        screen.blit(font.render(f"CASH: Infinity", True, White), (20, 0))
        cash = 10**30
    else:
        screen.blit(font.render(f"CASH: {cash:,}", True, White), (20, 0))
    Save.draw(screen, (300, 0))
    UpgradesButton.draw(screen, (400, 0))
    for j in range(len(PossibleAchivements)):
         a= list(PossibleAchivements.keys())[j]
         if a in Achivements:
             screen.blit(font.render(f"{a}", True, White), (20 + 200*(j%4), 20+24*int(j/4)))
         else: 
             screen.blit(font.render(f"{a}", True, Red), (20 + 200*(j%4), 20+24*int(j/4)))
def AchivementsInput(event):
    if Save.Click(event):
        return True
    if UpgradesButton.Click(event):
        return True
CreateScrn(AchivementsDraw, AchivementsInput, Black)
while Status():
    MainLoop(screen)
SaveGame()
pygame.quit()
