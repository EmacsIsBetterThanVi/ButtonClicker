from PyWigit import *
import asyncio
class ImageTextButton():
  def __init__(self, text, image1, image2=None, LeftClick=None, RightClick=None, Mouse=None):
    self.text = text
    self.image1 = image1
    self.image2 = image2
    self.image = False
    self.LeftClick=LeftClick
    self.RightClick=RightClick
    self.Mouse=Mouse
    self.rect = self.image1.get_rect()
  def draw(self, screen, loc):
    self.rect = screen.blit(self.image2 if self.image else self.image1, loc)
    screen.blit(self.text, (loc[0]+self.image1.get_width(), loc[1]))
  def Click(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        if event.button == 1 and self.LeftClick:
          self.LeftClick(self, False)
        elif event.button == 3 and self.RightClick:
          self.RightClick(self, False)
        elif event.button == 2 and self.Mouse:
          self.Mouse(self, False)
        return True
    elif event.type == pygame.MOUSEBUTTONUP:
      if self.rect.collidepoint(event.pos):
        if event.button == 1 and self.LeftClick:
          self.LeftClick(self, True)
        elif event.button == 3 and self.RightClick:
          self.RightClick(self, True)
        elif event.button == 2 and self.Mouse:
          self.Mouse(self, True)
        return True
    return False
import json
import os
import time
screen = NewScreen((800, 600))
Window = Screen(screen, FullScreen=True)
font = NewFont("timesnewroman", 20)
SetCaption("Button Clicker")
cash = 0
TotalCash = 0
Buttons = []
Time = [[0, 0]]
Achivements = []
PossibleAchivements = {
    "Starting Out":(2, 1), # based on button 1, click button 1, 1 time
    "First Upgrade":(3, 1),
    "Perstitance":(2, 1000),
    "Perstitance 2":(3, 100),
    "Perstitance 3":(4, 100),
    "Perstitance 4":(5, 100),
    "Perstitance 5":(6, 100),
    "Perstitance 6":(7, 100),
    "Perstitance 7":(8, 100),
    "Perstitance 8":(9, 100),
    "Perstitance 9":(10, 100),
    "Perstitance 10":(11, 100),
    "Perstitance 11":(12, 100),
    "Perstitance 12":(13, 100),
    "Perstitance 13":(14, 100),
    "Perstitance 14":(15, 100),
    "Perstitance 15":(16, 100),
    "Perstitance 16":(17, 100),
    "Perstitance 17":(18, 100),
    "Perstitance 18":(19, 100),
    "Perstitance 19":(20, 100),
    "Perstitance 20":(21, 100),
    "Perstitance 21":(22, 100),
    "Perstitance 22":(23, 100),
    "Perstitance 23":(24, 100),
    "Millionaire":(0, 10**6),
    "Billionaire":(0, 10**9),
    "All Lucky Sevens":(1, 7777777),
    "Surpasing Infinity":(0, 10**16), # based on cash, requires hiting infinity
    "True Infinity": (1, 10**100)
}
autoclick_active = False
autoclick_timer = 0
last_time = 0
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
            MessageQueue.append("************ Coleman ************")
            MessageQueue.append("************* David *************")
            MessageQueue.append("************ Raphael ************")
            MessageQueue.append("Now, go enjoy the rest of your life")
      elif PossibleAchivements[j][0] == 1:
        if PossibleAchivements[j][1] <= TotalCash:
          Achivements.append(j)
          MessageQueue.append(j)
      elif PossibleAchivements[j][0] >= 2:
        try:
          if PossibleAchivements[j][1] <= Buttons[PossibleAchivements[j][0]-2][3]:
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
        Buttons.append([ImageTextButton(font.render("Button: .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button1.png"), pygame.image.load(os.path.dirname(__file__)+"/Button1P.png"), LeftClick=Button0Click), 0, 1, 0, 0, 0])
        NewUpgrade()
    finally:
         f.close()
def LoadVersion2SaveData(data):
    global TotalCash, Buttons, cash, i
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
        Buttons.append([ImageTextButton(font.render("Button: .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button1.png"), pygame.image.load(os.path.dirname(__file__)+"/Button1P.png"), LeftClick=Button0Click), 0, 1, 0, 0, 0])
        NewUpgrade()
def LoadVersion3SaveData(data):
  global Time, Buttons, cash ,i, AutoclickTime, AutoclickCost, autoclick_active
  try:
    LoadVersion2SaveData(data)
    for j in range(0, len(data["buttons"])):
      Buttons[j][4] = data["buttons"][j][3]
      Buttons[j][5] = data["buttons"][j][4]
    for j in range(0, len(data["time"])):
      Time[j][1] = data["time"][j]
    AutoclickTime = data["autotime"]
    if AutoclickTime != 2/0.9:
      autoclick_active = True
    AutoclickCost = data["autocost"]
  except Exception as e:
        if isinstance(e, KeyError):
            print("Reading Game Data failed: Save Data is from an old version which does not have key: ", e)
        else:
            print("Reading Game Data failed:", e)
        Buttons = []
        Time = [[0,0]]
        cash = 0
        i = 1
        Buttons.append([ImageTextButton(font.render("Button: .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button1.png"), pygame.image.load(os.path.dirname(__file__)+"/Button1P.png"), LeftClick=Button0Click), 0, 1, 0, 0, 0])
        NewUpgrade()
load = [LoadVersion1SaveData, LoadVersion2SaveData, LoadVersion3SaveData]
def SaveGame():
    f = open("ButtonClicker.save", "w")
    data = []
    data2 = []
    for j in Buttons:
        data.append([j[1], j[2], j[3], j[4], j[5]])
    for j in Time:
      data2.append(j[1])
    f.write(json.dumps({"version":3, "buttons":data, "cash":cash, "achivements": Achivements, "TotalCash": TotalCash, "time":data2, "autocost": AutoclickCost, "autotime":AutoclickTime}))
    f.close()
def Button0Click(self, UP: bool, isAuto=False):
    global cash, TotalCash
    if not UP:
      self.image = True
      cash += Buttons[0][2]
      TotalCash += Buttons[0][2]
      Buttons[0][3] += 1
    else:
      self.image = False
i = 1
def update_autoclick():
    global autoclick_timer, autoclick_active, last_time, cash
    
    if autoclick_active:
        current_time = time.time()
        if last_time == 0:
            last_time = current_time
            
        dt = current_time - last_time
        last_time = current_time
        
        autoclick_timer += dt
        
        if autoclick_timer >= AutoclickTime:
        
            if Buttons[0][1] <= cash:
                cash -= Buttons[0][1]
                cash += Buttons[0][2]
                Buttons[0][3] += 1
            autoclick_timer = 0

autoclick_active = False
MessageTicks = 0
def NewUpgrade():
    global i
    exec(f"""def Button{i}Click(self, UP, isAuto=False):
    global cash
    if not UP:
      if Buttons[{i}][1] <= cash and (Buttons[{i}][4] <= 0 or isAuto):
        cash -= Buttons[{i}][1]
        Buttons[{i-1}][2] += Buttons[{i}][2]
        if Buttons[{i}][3] == 0:
            Buttons[{i}][1] = 0
            NewUpgrade()
        Buttons[{i}][4] = Buttons[{i}][5]
        Buttons[{i}][3] += 1
        self.image = True
    else:
      self.image = False
def Button{i}Upgrade(self, UP):
    global cash
    if not UP:
      if Time[{i}][1] <= cash:
        cash -= Time[{i}][1]
        Buttons[{i}][5] *= 0.9
        Time[{i}][1] = int(Time[{i}][1] * 1.1)
        self.image = True
    else:
      self.image = False
Buttons.append([ImageTextButton(font.render("Button {i+1}($.): .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button{i+1}.png"), pygame.image.load(os.path.dirname(__file__)+"/Button{i+1}P.png"), LeftClick=Button{i}Click), 10**(i+1), 1, 0, 0, {i*2}])
Time.append([ImageTextButton(font.render("Button {i+1}($.): .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button{i+1}.png"), pygame.image.load(os.path.dirname(__file__)+"/Button{i+1}P.png"), LeftClick=Button{i}Upgrade), 10**(i+1)])
""")
    i+=1
Save = Button(font.render("Save", True, White), LeftClick=SaveGame)
AchivmentsButton = Button(font.render("Achievments", True, Green), LeftClick=lambda : Window.ChangeScrn(2))
UpgradesButton = Button(font.render("Upgrades", True, Green), LeftClick=lambda : Window.ChangeScrn(1))
def AutoClickHandle(self, UP):
  if not UP:
    global AutoclickCost, AutoclickTime, cash, autoclick_active
    if cash >= AutoclickCost:
      cash -= AutoclickCost
      AutoclickCost = int(AutoclickCost * 1.5)
      AutoclickTime *= 0.9
      autoclick_active = True
      self.image = True
  else:
    self.image = False
Buttons.append([ImageTextButton(font.render("Button: .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button1.png"), pygame.image.load(os.path.dirname(__file__)+"/Button1P.png"), LeftClick=Button0Click), 0, 1, 0, 0, 0])
AutoclickButton = ImageTextButton(font.render("Button: .", True, White), pygame.image.load(os.path.dirname(__file__)+"/Button1.png"), pygame.image.load(os.path.dirname(__file__)+"/Button1P.png"), LeftClick=AutoClickHandle)
CooldownImageBoarder = pygame.image.load(os.path.dirname(__file__)+"/CooldownOutside.png")
CooldownImageInside = pygame.image.load(os.path.dirname(__file__)+"/CooldownInside.png")
Cooldown = ProgressBar(CooldownImageInside, (4,4), CooldownImageBoarder)
AutoclickCost = 100
AutoclickTime = 2/0.9
if os.path.exists("ButtonClicker.save"):
    f = open("ButtonClicker.save")
    data = json.loads(f.read())
    load[data["version"]-1](data)
else:
    NewUpgrade()
    MessageQueue.append("Welcome to Button Clicker!")
    MessageQueue.append("We hope you enjoy the \"game\"")
def DrawGame(screen):
    checkAchivements()
    update_autoclick()
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
    Buttons[0][0].text = font.render(f": {Buttons[0][2]:,}", True, White)
    Buttons[0][0].draw(screen, (20, 24))
    if autoclick_active:
      AutoclickButton.text = font.render(f"(${AutoclickCost}): {Buttons[0][2]:,}/{AutoclickTime:.4f}s", True, White)
    else:
      AutoclickButton.text = font.render(f"(${AutoclickCost}): Autoclick", True, White)
    AutoclickButton.draw(screen, (550, 24))
    Buttons[1][0].text = font.render(f"(${Buttons[1][1]:,}): {Buttons[1][2]:,}", True, White)
    Buttons[1][0].draw(screen, (20, 49))
    Time[1][0].text = font.render(f"(${Time[1][1]:,}): {Buttons[1][5]:.4f}s", True, White)
    Time[1][0].draw(screen, (550, 49))
    for j in range(2, len(Buttons)):
        Buttons[j][0].text = font.render(f"(${Buttons[j][1]:,}): {Buttons[j][2]:,}", True, White)
        Buttons[j][0].draw(screen, (20, 24+25*j))
        Time[j][0].text = font.render(f"(${Time[j][1]:,}): {Buttons[j][5]:.4f}s", True, White)
        Time[j][0].draw(screen, (550, 24+25*j))
    for j in range(1, len(Buttons)):
        if Buttons[j][4]>0:
          Cooldown.draw(screen, (400, 24+25*j), Buttons[j][4], Buttons[j][5])
          Buttons[j][4] -= 1/60
def InputGame(event):
    if Save.Click(event):
        return True
    if AchivmentsButton.Click(event):
        return True
    if AutoclickButton.Click(event):
      return True
    for j in range(len(Buttons)):
        if Buttons[j][0].Click(event):
            return True
    for j in range(1, len(Time)):
      if Time[j][0].Click(event):
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
           if a == "True Infinity":
             screen.blit(font.render(f"?????????????", True, Black), (20 + 200*(j%4), 20+24*int(j/4)))
           else:
             screen.blit(font.render(f"{a}", True, Red), (20 + 200*(j%4), 20+24*int(j/4)))
def AchivementsInput(event):
    if Save.Click(event):
        return True
    if UpgradesButton.Click(event):
        return True
CreateScrn(AchivementsDraw, AchivementsInput, Black)
async def main():
  while Status():
    MainLoop(screen)
    await asyncio.sleep(0)
  SaveGame()
  pygame.quit()
asyncio.run(main())
